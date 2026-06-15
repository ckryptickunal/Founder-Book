"""
Ingest local files into the LLM wiki.

Supported inputs:
    - PDF (.pdf) via PyMuPDF
    - PDF (.pdf) via Gemini file upload when --extractor gemini is used
    - Text / markdown (.txt, .md)
    - HTML (.html, .htm) with basic tag stripping

Usage:
    python3 ingest_file.py "~/Downloads/document.pdf"
    python3 ingest_file.py --extractor gemini "~/Downloads/document.pdf"
    python3 ingest_file.py ~/Downloads/*.pdf
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from datetime import datetime
from pathlib import Path

from google.genai import types

from ingest import (
    BASE_DIR,
    WIKI_DIR,
    configure_gemini,
    ensure_dirs,
    ingest_worker,
    load_manifest,
    rebuild_index,
    slugify,
)

LOCAL_FILES_DIR = BASE_DIR / "Local Files"
SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md", ".markdown", ".html", ".htm"}


def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def extract_pdf_text(path: Path) -> str:
    try:
        import fitz  # PyMuPDF
    except ImportError as exc:
        raise RuntimeError(
            "PDF ingestion needs PyMuPDF. Install it with: pip3 install PyMuPDF"
        ) from exc

    parts: list[str] = []
    with fitz.open(path) as doc:
        for page_number, page in enumerate(doc, start=1):
            text = page.get_text("text").strip()
            if text:
                parts.append(f"\n\n--- Page {page_number} ---\n{text}")
    return "\n".join(parts).strip()


def extract_pdf_text_with_gemini(path: Path, gemini) -> str:
    prompt = """
Extract the full meaningful text from this PDF into clean markdown.

Requirements:
- Preserve the document's question/answer structure.
- Keep important numbers, URLs, names, dates, and product/company details.
- Remove repeated browser chrome, page headers, page footers, nav labels, and duplicated URLs when they do not add meaning.
- Do not summarize. Do not critique. Do not add commentary.
- Return only the extracted document text.
"""
    uploaded_file = gemini["client"].files.upload(
        file=str(path),
        config=types.UploadFileConfig(mime_type="application/pdf", display_name=path.name),
    )
    try:
        response = gemini["client"].models.generate_content(
            model=gemini["model_name"],
            contents=[uploaded_file, prompt],
            config=types.GenerateContentConfig(temperature=0.0),
        )
        text = (response.text or "").strip()
        if not text:
            raise ValueError("Gemini returned empty PDF extraction text")
        return text
    finally:
        try:
            gemini["client"].files.delete(name=uploaded_file.name)
        except Exception:
            pass


def strip_html(raw: str) -> str:
    raw = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    raw = html.unescape(raw)
    raw = re.sub(r"[ \t]+", " ", raw)
    raw = re.sub(r"\n\s*\n\s*\n+", "\n\n", raw)
    return raw.strip()


def extract_text(path: Path, extractor: str = "local", gemini=None) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        if extractor == "gemini":
            if gemini is None:
                raise ValueError("Gemini extractor requires a configured Gemini client")
            return extract_pdf_text_with_gemini(path, gemini)
        return extract_pdf_text(path)
    if suffix in {".txt", ".md", ".markdown"}:
        return path.read_text(encoding="utf-8", errors="replace").strip()
    if suffix in {".html", ".htm"}:
        raw = path.read_text(encoding="utf-8", errors="replace")
        return strip_html(raw)
    raise ValueError(f"Unsupported file type: {suffix}. Supported: {sorted(SUPPORTED_EXTENSIONS)}")


def infer_title(path: Path) -> str:
    return path.stem.replace("_", " ").replace("-", " ").strip().title() or path.stem


def local_video_id(path: Path) -> str:
    return f"local-{slugify(path.stem, fallback='file')}"


def transcript_path_for(path: Path) -> Path:
    return LOCAL_FILES_DIR / f"{local_video_id(path)}.txt"


def write_local_transcript(source_path: Path, text: str, force: bool = False) -> Path:
    if not text.strip():
        raise ValueError(f"No extractable text found in {source_path}")

    LOCAL_FILES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = transcript_path_for(source_path)
    if output_path.exists() and not force:
        return output_path

    title = infer_title(source_path)
    video_id = local_video_id(source_path)
    content = "\n".join(
        [
            f"Title: {title}",
            f"Video ID: {video_id}",
            "Channel: Local Files",
            f"Published: {today()}",
            f"Source: {source_path}",
            "",
            "=" * 60,
            "TRANSCRIPT",
            "=" * 60,
            "",
            text.strip(),
            "",
        ]
    )
    output_path.write_text(content, encoding="utf-8")
    return output_path


def verify_ingested(transcript_path: Path, manifest: dict) -> bool:
    expected_id = transcript_path.stem
    return expected_id in manifest


def ingest_local_file(
    path: Path,
    gemini,
    manifest: dict,
    force: bool,
    max_chars: int,
    extractor: str = "local",
) -> dict:
    source_path = path.expanduser().resolve()
    if not source_path.exists():
        return {"path": str(path), "status": "failed", "error": "file does not exist"}
    if source_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        return {
            "path": str(source_path),
            "status": "failed",
            "error": f"unsupported extension {source_path.suffix}",
        }

    text = extract_text(source_path, extractor=extractor, gemini=gemini)
    transcript_path = write_local_transcript(source_path, text, force=force)
    result = ingest_worker(transcript_path, gemini, manifest, force, max_chars)

    # Self-heal verification: reload manifest after ingestion_worker saves it.
    updated_manifest = load_manifest()
    verified = verify_ingested(transcript_path, updated_manifest)
    if result in {"processed", "skipped"} and verified:
        return {
            "path": str(source_path),
            "transcript": str(transcript_path.relative_to(BASE_DIR)),
            "status": result,
            "extractor": extractor,
            "verified": True,
        }

    return {
        "path": str(source_path),
        "transcript": str(transcript_path.relative_to(BASE_DIR)),
        "status": "failed",
        "extractor": extractor,
        "verified": False,
        "error": "ingestion did not appear in manifest after processing",
    }


def ingest_files(
    paths: list[Path],
    force: bool = False,
    max_chars: int = 120_000,
    extractor: str = "local",
) -> list[dict]:
    if extractor not in {"local", "gemini"}:
        raise ValueError("extractor must be 'local' or 'gemini'")

    ensure_dirs()
    gemini = configure_gemini()
    manifest = load_manifest()

    results: list[dict] = []
    for path in paths:
        try:
            results.append(
                ingest_local_file(
                    path,
                    gemini,
                    manifest,
                    force,
                    max_chars,
                    extractor=extractor,
                )
            )
        except Exception as exc:
            results.append({"path": str(path), "status": "failed", "error": str(exc)})

    rebuild_index()
    return results


def print_report(results: list[dict]) -> int:
    success = [r for r in results if r.get("verified")]
    failed = [r for r in results if not r.get("verified")]

    print("\n" + "=" * 50)
    print("LOCAL FILE INGEST REPORT")
    print("=" * 50)
    print(f"  Verified: {len(success)}")
    print(f"  Failed:   {len(failed)}")
    for result in results:
        status = "OK" if result.get("verified") else "FAIL"
        print(f"  [{status}] {result.get('path')}")
        if result.get("transcript"):
            print(f"       transcript: {result['transcript']}")
        if result.get("extractor"):
            print(f"       extractor: {result['extractor']}")
        if result.get("error"):
            print(f"       error: {result['error']}")
    print("=" * 50)
    return 0 if not failed else 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest local files into the LLM wiki.")
    parser.add_argument("paths", nargs="+", type=Path, help="Local file paths to ingest.")
    parser.add_argument("--force", action="store_true", help="Re-extract and re-ingest existing files.")
    parser.add_argument("--max-chars", type=int, default=120_000, help="Maximum text characters sent to Gemini.")
    parser.add_argument(
        "--extractor",
        choices=["local", "gemini"],
        default="local",
        help="Use local extraction or Gemini file upload for PDFs.",
    )
    parser.add_argument(
        "--gemini",
        action="store_true",
        help="Shortcut for --extractor gemini.",
    )
    args = parser.parse_args()

    extractor = "gemini" if args.gemini else args.extractor
    results = ingest_files(args.paths, force=args.force, max_chars=args.max_chars, extractor=extractor)
    raise SystemExit(print_report(results))


if __name__ == "__main__":
    main()
