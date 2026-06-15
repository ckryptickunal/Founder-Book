import argparse
import os
import re
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

from ingest import WIKI_DIR, SYNTHESIS_DIR, append_log, rebuild_index, slugify, today


SPECIAL_FILES = {"index.md", "log.md", "schema.md", "ingested.json"}


def timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def configure_gemini():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your-gemini-api-key-here":
        raise RuntimeError("Set GEMINI_API_KEY in .env before using --gemini")
    model_name = os.getenv("GEMINI_MODEL_LINT", os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))
    return {"client": genai.Client(api_key=api_key), "model_name": model_name}


def wiki_pages() -> dict[str, Path]:
    pages = {}
    for path in WIKI_DIR.rglob("*.md"):
        if path.name in SPECIAL_FILES:
            continue
        rel = str(path.relative_to(WIKI_DIR).with_suffix(""))
        pages[rel] = path
        pages[path.stem] = path
    return pages


def extract_links(text: str) -> list[str]:
    links = []
    for match in re.findall(r"\[\[([^\]]+)\]\]", text):
        target = match.split("|", 1)[0].split("#", 1)[0].strip()
        if target:
            links.append(target.removesuffix(".md"))
    return links


def has_frontmatter(text: str) -> bool:
    return text.startswith("---\n") and "\n---\n" in text[4:]


def build_report() -> dict:
    pages = wiki_pages()
    canonical_paths = {str(path.relative_to(WIKI_DIR).with_suffix("")): path for path in set(pages.values())}
    inbound = {rel: 0 for rel in canonical_paths}
    missing_links = []
    missing_frontmatter = []
    page_count_by_dir: dict[str, int] = {}

    for rel, path in canonical_paths.items():
        text = path.read_text(encoding="utf-8", errors="replace")
        top_dir = rel.split("/", 1)[0] if "/" in rel else "."
        page_count_by_dir[top_dir] = page_count_by_dir.get(top_dir, 0) + 1

        if not has_frontmatter(text):
            missing_frontmatter.append(rel)

        for link in extract_links(text):
            if link in pages:
                target_rel = str(pages[link].relative_to(WIKI_DIR).with_suffix(""))
                inbound[target_rel] = inbound.get(target_rel, 0) + 1
            else:
                missing_links.append({"from": rel, "target": link})

    orphan_pages = [
        rel for rel, count in inbound.items()
        if count == 0 and not rel.startswith("sources/")
    ]

    return {
        "generated_at": timestamp(),
        "page_count": len(canonical_paths),
        "page_count_by_dir": page_count_by_dir,
        "orphan_pages": sorted(orphan_pages),
        "missing_links": missing_links,
        "missing_frontmatter": sorted(missing_frontmatter),
    }


def render_report(report: dict) -> str:
    lines = [
        "# Wiki Lint Report",
        "",
        f"Generated: {report['generated_at']}",
        "",
        "## Summary",
        "",
        f"- Total pages: {report['page_count']}",
    ]
    for directory, count in sorted(report["page_count_by_dir"].items()):
        lines.append(f"- `{directory}/`: {count}")

    lines.extend(["", "## Orphan Pages", ""])
    if report["orphan_pages"]:
        lines.extend(f"- `{page}`" for page in report["orphan_pages"])
    else:
        lines.append("No non-source orphan pages found.")

    lines.extend(["", "## Missing Links", ""])
    if report["missing_links"]:
        lines.extend(
            f"- `{item['from']}` links to missing page `{item['target']}`"
            for item in report["missing_links"]
        )
    else:
        lines.append("No missing wikilinks found.")

    lines.extend(["", "## Missing Frontmatter", ""])
    if report["missing_frontmatter"]:
        lines.extend(f"- `{page}`" for page in report["missing_frontmatter"])
    else:
        lines.append("All generated pages have frontmatter.")

    return "\n".join(lines)


def gemini_review(gemini, report_text: str) -> str:
    index_text = (WIKI_DIR / "index.md").read_text(encoding="utf-8", errors="replace") if (WIKI_DIR / "index.md").exists() else ""
    prompt = f"""
You are maintaining an LLM-generated markdown wiki.

Review this lint report and index. Suggest the highest-value maintenance actions:
- missing cross-references
- topics/entities that likely need pages
- stale or weak synthesis opportunities
- data gaps to fill later

Keep the answer concise and actionable. Do not invent facts not present in the report/index.

Lint report:
{report_text}

Index:
{index_text[:60_000]}
"""
    response = gemini["client"].models.generate_content(
        model=gemini["model_name"],
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.2),
    )
    return response.text.strip()


def save_report(report_text: str, gemini_text: str | None) -> Path:
    SYNTHESIS_DIR.mkdir(parents=True, exist_ok=True)
    path = SYNTHESIS_DIR / f"{today()}-wiki-lint-report.md"
    content = "\n".join(
        [
            "---",
            "type: synthesis",
            "title: Wiki Lint Report",
            f"created: {today()}",
            f"updated: {today()}",
            "sources: []",
            "tags:",
            "  - lint",
            "---",
            "",
            report_text,
            "",
        ]
    )
    if gemini_text:
        content += "\n## Gemini Maintenance Suggestions\n\n" + gemini_text + "\n"
    path.write_text(content, encoding="utf-8")
    rebuild_index()
    append_log("lint", "Wiki Lint Report", f"- Saved: `{path.relative_to(WIKI_DIR.parent)}`")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Health-check the generated LLM wiki.")
    parser.add_argument("--gemini", action="store_true", help="Ask Gemini 2.5 Flash for maintenance suggestions.")
    parser.add_argument("--save", action="store_true", help="Save the lint report under wiki/synthesis.")
    parser.add_argument("--fix-index", action="store_true", help="Rebuild wiki/index.md before linting.")
    args = parser.parse_args()

    if args.fix_index:
        rebuild_index()

    report = build_report()
    report_text = render_report(report)
    print(report_text)

    gemini_text = None
    if args.gemini:
        gemini = configure_gemini()
        gemini_text = gemini_review(gemini, report_text)
        print("\n## Gemini Maintenance Suggestions\n")
        print(gemini_text)

    if args.save:
        path = save_report(report_text, gemini_text)
        print(f"\nSaved lint report to: {path}")


if __name__ == "__main__":
    main()
