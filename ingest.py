import argparse
import json
import os
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


BASE_DIR = Path(__file__).resolve().parent
WIKI_DIR = BASE_DIR / "wiki"
SOURCES_DIR = WIKI_DIR / "sources"
ENTITIES_DIR = WIKI_DIR / "entities"
TOPICS_DIR = WIKI_DIR / "topics"
SYNTHESIS_DIR = WIKI_DIR / "synthesis"
INDEX_PATH = WIKI_DIR / "index.md"
LOG_PATH = WIKI_DIR / "log.md"
MANIFEST_PATH = WIKI_DIR / "ingested.json"
FAILURES_PATH = WIKI_DIR / "ingest_failures.json"

SKIP_DIRS = {
    ".cursor",
    "__pycache__",
    "wiki",
    ".git",
}


def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def slugify(value: str, fallback: str = "untitled") -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value[:90] or fallback


def ensure_dirs() -> None:
    for path in [WIKI_DIR, SOURCES_DIR, ENTITIES_DIR, TOPICS_DIR, SYNTHESIS_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def load_manifest() -> dict:
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {}


def save_manifest(manifest: dict) -> None:
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")


_failures_lock = threading.Lock()


def load_failures() -> list[dict]:
    if FAILURES_PATH.exists():
        try:
            return json.loads(FAILURES_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            return []
    return []


def save_failures(failures: list[dict]) -> None:
    FAILURES_PATH.write_text(json.dumps(failures, indent=2), encoding="utf-8")


def record_failure(video_id: str, path: str, error: str) -> None:
    with _failures_lock:
        failures = load_failures()
        existing = {f["video_id"] for f in failures}
        if video_id in existing:
            for f in failures:
                if f["video_id"] == video_id:
                    f["attempts"] = f.get("attempts", 1) + 1
                    f["last_error"] = error
                    f["last_attempt"] = timestamp()
                    break
        else:
            failures.append({
                "video_id": video_id,
                "source_file": path,
                "error": error,
                "attempts": 1,
                "first_failed": timestamp(),
                "last_attempt": timestamp(),
            })
        save_failures(failures)


def clear_failure(video_id: str) -> None:
    with _failures_lock:
        failures = load_failures()
        failures = [f for f in failures if f["video_id"] != video_id]
        save_failures(failures)


def append_log(kind: str, title: str, detail: str = "") -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as file:
        file.write(f"\n## [{today()}] {kind} | {title}\n")
        if detail:
            file.write(f"{detail}\n")


def parse_transcript_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    metadata: dict[str, str] = {}

    transcript_marker = "TRANSCRIPT"
    marker_index = text.find(transcript_marker)
    header_text = text[:marker_index] if marker_index != -1 else text[:2000]
    transcript_text = text[marker_index + len(transcript_marker):] if marker_index != -1 else text
    transcript_text = re.sub(r"^=+\s*", "", transcript_text.strip())

    for line in header_text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip().lower().replace(" ", "_")] = value.strip()

    video_id = metadata.get("video_id") or path.stem
    title = metadata.get("title") or path.stem
    return {
        "path": str(path),
        "video_id": video_id,
        "title": title,
        "metadata": metadata,
        "transcript": transcript_text,
    }


def configure_gemini():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your-gemini-api-key-here":
        raise RuntimeError("Set GEMINI_API_KEY in .env before running ingest.py")
    model_name = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
    return {"client": genai.Client(api_key=api_key), "model_name": model_name}


def extract_json(text: str) -> dict:
    if not text or not text.strip():
        raise ValueError("Gemini returned empty response")

    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)

    start = cleaned.find("{")
    if start == -1:
        raise ValueError("Gemini response did not contain JSON object")

    # Use raw_decode to parse first valid JSON object, ignoring trailing data
    decoder = json.JSONDecoder()
    try:
        obj, _ = decoder.raw_decode(cleaned, start)
        return obj
    except json.JSONDecodeError:
        pass

    # Fallback: extract between first { and last }
    end = cleaned.rfind("}")
    if end == -1:
        raise ValueError("No closing brace in Gemini response")
    raw = cleaned[start : end + 1]

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # Repair: trailing commas, unescaped newlines
    repaired = re.sub(r",\s*([}\]])", r"\1", raw)
    repaired = repaired.replace("\n", "\\n")
    try:
        return json.loads(repaired)
    except json.JSONDecodeError:
        pass

    # Last resort: try progressively shorter substrings
    for i in range(len(raw) - 1, 0, -1):
        if raw[i] == "}":
            try:
                return json.loads(raw[: i + 1])
            except json.JSONDecodeError:
                continue
    raise ValueError("Could not parse Gemini JSON response")


def analyze_transcript(gemini, record: dict, max_chars: int) -> dict:
    metadata = record["metadata"]
    transcript = record["transcript"][:max_chars]
    prompt = f"""
You maintain a markdown LLM wiki for YouTube transcripts.

Return ONLY valid JSON. Do not include markdown fences.

Analyze this transcript and produce:
- concise source summary
- key ideas
- entities (people, companies, products, organizations)
- topics
- notable claims
- useful quotes
- tags

JSON schema:
{{
  "summary": "string",
  "key_ideas": ["string"],
  "entities": [
    {{"name": "string", "type": "person|company|product|organization|project|other", "description": "string", "importance": "string"}}
  ],
  "topics": [
    {{"name": "string", "summary": "string"}}
  ],
  "claims": [
    {{"claim": "string", "evidence": "string"}}
  ],
  "quotes": ["string"],
  "tags": ["string"]
}}

Metadata:
Title: {record["title"]}
Video ID: {record["video_id"]}
Channel: {metadata.get("channel", metadata.get("channel_title", "Unknown"))}
Published: {metadata.get("published", metadata.get("published_at", "Unknown"))}
URL: {metadata.get("url", "")}

Transcript:
{transcript}
"""
    import time as _time
    for attempt in range(3):
        try:
            response = gemini["client"].models.generate_content(
                model=gemini["model_name"],
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2 + (attempt * 0.1),
                    response_mime_type="application/json",
                ),
            )
        except Exception as api_err:
            if attempt == 2:
                raise ValueError(f"Gemini API error after 3 attempts: {api_err}")
            _time.sleep(5 * (attempt + 1))
            continue
        try:
            return extract_json(response.text)
        except (ValueError, json.JSONDecodeError) as e:
            if attempt == 2:
                raise ValueError(f"Failed to parse Gemini JSON after 3 attempts: {e}")
            _time.sleep(3 * (attempt + 1))


def yaml_list(items: list[str]) -> str:
    if not items:
        return " []"
    return "\n" + "\n".join(f"  - {item}" for item in items)


def source_stem(record: dict) -> str:
    return f"{record['video_id']}-{slugify(record['title'])}"


def source_link(record: dict) -> str:
    return f"[[sources/{source_stem(record)}|{record['title']}]]"


def render_source_page(record: dict, analysis: dict) -> str:
    metadata = record["metadata"]
    tags = [slugify(tag) for tag in analysis.get("tags", [])[:12]]
    entities = analysis.get("entities", [])
    topics = analysis.get("topics", [])
    video_url = metadata.get("url", f"https://www.youtube.com/watch?v={record['video_id']}")

    lines = [
        "---",
        "type: source",
        f"title: {json.dumps(record['title'])[1:-1]}",
        f"created: {today()}",
        f"updated: {today()}",
        f"video_id: {record['video_id']}",
        f"url: {video_url}",
        f"channel: {metadata.get('channel', metadata.get('channel_title', 'Unknown'))}",
        f"published: {metadata.get('published', metadata.get('published_at', 'Unknown'))}",
        "tags:" + yaml_list(tags),
        "---",
        "",
        f"# {record['title']}",
        "",
        "## Metadata",
        "",
        f"- Video ID: `{record['video_id']}`",
        f"- Channel: {metadata.get('channel', metadata.get('channel_title', 'Unknown'))}",
        f"- Published: {metadata.get('published', metadata.get('published_at', 'Unknown'))}",
        f"- URL: {video_url}",
        "",
        "## Summary",
        "",
        analysis.get("summary", "No summary generated."),
        "",
        "## Key Ideas",
        "",
    ]
    lines.extend(f"- {idea}" for idea in analysis.get("key_ideas", []))
    lines.extend(["", "## Entities", ""])
    lines.extend(
        f"- [[entities/{slugify(entity.get('name', 'unknown'))}|{entity.get('name', 'Unknown')}]] ({entity.get('type', 'other')}): {entity.get('description', '')}"
        for entity in entities
    )
    lines.extend(["", "## Topics", ""])
    lines.extend(
        f"- [[topics/{slugify(topic.get('name', 'unknown'))}|{topic.get('name', 'Unknown')}]]: {topic.get('summary', '')}"
        for topic in topics
    )
    lines.extend(["", "## Notable Claims", ""])
    lines.extend(
        f"- {claim.get('claim', '')} Evidence: {claim.get('evidence', '')}"
        for claim in analysis.get("claims", [])
    )
    lines.extend(["", "## Quotes", ""])
    lines.extend(f"> {quote}" for quote in analysis.get("quotes", []))
    lines.append("")
    return "\n".join(lines)


def upsert_reference_page(path: Path, page_type: str, title: str, description: str, source: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    mention = f"- {source}: {description}".strip()

    if path.exists():
        content = path.read_text(encoding="utf-8")
        if source in content:
            return
        content = re.sub(r"updated: \d{4}-\d{2}-\d{2}", f"updated: {today()}", content)
        if "## Source Mentions" not in content:
            content += "\n## Source Mentions\n\n"
        content = content.rstrip() + f"\n{mention}\n"
        path.write_text(content, encoding="utf-8")
        return

    content = "\n".join(
        [
            "---",
            f"type: {page_type}",
            f"title: {json.dumps(title)[1:-1]}",
            f"created: {today()}",
            f"updated: {today()}",
            "sources: []",
            "tags: []",
            "---",
            "",
            f"# {title}",
            "",
            "## Overview",
            "",
            description or "Generated from transcript references.",
            "",
            "## Source Mentions",
            "",
            mention,
            "",
        ]
    )
    path.write_text(content, encoding="utf-8")


def update_reference_pages(record: dict, analysis: dict) -> None:
    link = source_link(record)
    for entity in analysis.get("entities", []):
        name = entity.get("name", "").strip()
        if not name:
            continue
        path = ENTITIES_DIR / f"{slugify(name)}.md"
        description = entity.get("description") or entity.get("importance", "")
        upsert_reference_page(path, "entity", name, description, link)

    for topic in analysis.get("topics", []):
        name = topic.get("name", "").strip()
        if not name:
            continue
        path = TOPICS_DIR / f"{slugify(name)}.md"
        upsert_reference_page(path, "topic", name, topic.get("summary", ""), link)


def read_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"^title:\s*(.+)$", text, re.MULTILINE)
    if match:
        return match.group(1).strip().strip('"')
    heading = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return heading.group(1).strip() if heading else path.stem


def rebuild_index() -> None:
    sections = [
        ("Sources", SOURCES_DIR),
        ("Entities", ENTITIES_DIR),
        ("Topics", TOPICS_DIR),
        ("Synthesis", SYNTHESIS_DIR),
    ]
    lines = [
        "# Wiki Index",
        "",
        f"Last updated: {timestamp()}",
        "",
        "This index is maintained by the LLM wiki scripts.",
        "",
    ]
    for label, directory in sections:
        lines.extend([f"## {label}", ""])
        pages = sorted(directory.glob("*.md"))
        if not pages:
            lines.extend([f"No {label.lower()} pages indexed yet.", ""])
            continue
        for page in pages:
            title = read_title(page)
            rel = page.relative_to(WIKI_DIR).with_suffix("")
            lines.append(f"- [[{rel}|{title}]]")
        lines.append("")
    INDEX_PATH.write_text("\n".join(lines), encoding="utf-8")


def discover_transcripts() -> list[Path]:
    paths: list[Path] = []
    for child in BASE_DIR.iterdir():
        if not child.is_dir() or child.name in SKIP_DIRS or child.name.startswith("."):
            continue
        for path in child.glob("*.txt"):
            if not path.name.startswith("_"):
                paths.append(path)
    return sorted(paths)


def ingest_path(path: Path, gemini, manifest: dict, force: bool, max_chars: int) -> bool:
    record = parse_transcript_file(path)
    stat = path.stat()
    manifest_key = record["video_id"]
    existing = manifest.get(manifest_key)
    if existing and not force and existing.get("mtime") == stat.st_mtime:
        print(f"SKIP {record['video_id']} already ingested")
        return False

    print(f"INGEST {record['video_id']} | {record['title'][:80]}")
    analysis = analyze_transcript(gemini, record, max_chars=max_chars)

    output_path = SOURCES_DIR / f"{source_stem(record)}.md"
    output_path.write_text(render_source_page(record, analysis), encoding="utf-8")
    update_reference_pages(record, analysis)

    manifest[manifest_key] = {
        "source_file": str(path.relative_to(BASE_DIR)),
        "wiki_page": str(output_path.relative_to(BASE_DIR)),
        "title": record["title"],
        "mtime": stat.st_mtime,
        "ingested_at": timestamp(),
    }
    append_log("ingest", record["title"], f"- Source: `{path.relative_to(BASE_DIR)}`\n- Wiki page: `{output_path.relative_to(BASE_DIR)}`")
    clear_failure(record["video_id"])
    return True


_manifest_lock = threading.Lock()
_index_lock = threading.Lock()


def ingest_worker(path: Path, gemini, manifest: dict, force: bool, max_chars: int) -> str:
    """Worker function for parallel ingestion. Returns 'processed', 'skipped', or 'failed'."""
    if not path.exists():
        print(f"Missing file: {path}", file=sys.stderr)
        return "skipped"
    try:
        record = parse_transcript_file(path)
        stat = path.stat()
        manifest_key = record["video_id"]

        with _manifest_lock:
            existing = manifest.get(manifest_key)
            if existing and not force and existing.get("mtime") == stat.st_mtime:
                print(f"SKIP {record['video_id']} already ingested")
                return "skipped"

        print(f"INGEST {record['video_id']} | {record['title'][:80]}")
        analysis = analyze_transcript(gemini, record, max_chars=max_chars)

        output_path = SOURCES_DIR / f"{source_stem(record)}.md"
        output_path.write_text(render_source_page(record, analysis), encoding="utf-8")

        with _index_lock:
            update_reference_pages(record, analysis)

        with _manifest_lock:
            manifest[manifest_key] = {
                "source_file": str(path.relative_to(BASE_DIR)),
                "wiki_page": str(output_path.relative_to(BASE_DIR)),
                "title": record["title"],
                "mtime": stat.st_mtime,
                "ingested_at": timestamp(),
            }
            save_manifest(manifest)

        with _index_lock:
            append_log("ingest", record["title"], f"- Source: `{path.relative_to(BASE_DIR)}`\n- Wiki page: `{output_path.relative_to(BASE_DIR)}`")

        clear_failure(record["video_id"])
        return "processed"

    except Exception as e:
        video_id = path.stem
        error_msg = str(e)[:200]
        print(f"ERROR {video_id}: {error_msg}", file=sys.stderr)
        record_failure(video_id, str(path.relative_to(BASE_DIR)), error_msg)
        return "failed"


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest transcripts into the LLM wiki (parallel).")
    parser.add_argument("--all", action="store_true", help="Ingest all transcript files in channel folders.")
    parser.add_argument("--file", type=Path, help="Ingest a single transcript file.")
    parser.add_argument("--limit", type=int, help="Limit number of files processed.")
    parser.add_argument("--force", action="store_true", help="Re-ingest even if already processed.")
    parser.add_argument("--max-chars", type=int, default=120_000, help="Maximum transcript characters sent to Gemini.")
    parser.add_argument("--workers", type=int, default=40, help="Parallel workers (default: 40, Tier 3 rate limits).")
    args = parser.parse_args()

    if not args.all and not args.file:
        parser.error("Use --all or --file")

    ensure_dirs()
    gemini = configure_gemini()
    manifest = load_manifest()

    paths = [args.file] if args.file else discover_transcripts()
    if args.limit:
        paths = paths[: args.limit]

    print(f"Starting ingestion: {len(paths)} files, {args.workers} workers")

    processed = 0
    failed = 0
    skipped = 0

    if args.workers <= 1 or args.file:
        for path in paths:
            result = ingest_worker(path.resolve(), gemini, manifest, args.force, args.max_chars)
            if result == "processed":
                processed += 1
            elif result == "failed":
                failed += 1
            else:
                skipped += 1
    else:
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {
                executor.submit(ingest_worker, path.resolve(), gemini, manifest, args.force, args.max_chars): path
                for path in paths
            }
            for future in as_completed(futures):
                result = future.result()
                if result == "processed":
                    processed += 1
                elif result == "failed":
                    failed += 1
                else:
                    skipped += 1

    rebuild_index()
    save_manifest(manifest)

    # Self-heal: clear stale failures that are already in manifest
    with _failures_lock:
        stale_failures = load_failures()
        if stale_failures:
            active_failures = [f for f in stale_failures if f["video_id"] not in manifest]
            cleared = len(stale_failures) - len(active_failures)
            if cleared > 0:
                save_failures(active_failures)
                print(f"  [self-heal] Cleared {cleared} stale failure entries (already ingested).")
            stale_failures = active_failures

    # Self-analysis summary
    print(f"\n{'='*50}")
    print(f"INGEST SUMMARY")
    print(f"{'='*50}")
    print(f"  Processed: {processed}")
    print(f"  Skipped (already done): {skipped}")
    print(f"  Failed this run: {failed}")
    print(f"  Total in failure log: {len(stale_failures)}")
    print(f"  Workers used: {args.workers}")
    if stale_failures:
        print(f"  Re-run with --all --force to retry failed items.")
    print(f"  Status: {'ALL CLEAR' if not stale_failures and failed == 0 else 'HAS ISSUES'}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
