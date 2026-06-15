#!/usr/bin/env python3
"""
Incremental essay fetcher — discovers and downloads NEW essays/articles
directly from authors' websites, in the same transcript format the wiki
ingests.

Why this exists
---------------
`fetch_essays.py` pulls a *fixed* HuggingFace snapshot of Paul Graham / Sam
Altman essays. It never sees anything published after that snapshot. This
script instead reads each author's live index page, diffs it against what is
already on disk, and downloads only the essays we do not yet have.

It is deliberately defensive: a failure on one essay (network blip, layout
change) is logged and skipped — it never aborts the batch. It is idempotent:
re-running only fetches what is missing.

Currently supported `kind`s (see sources.json):
  - "paulgraham"  → https://www.paulgraham.com/articles.html
  - "samaltman"   → https://blog.samaltman.com/archive  (Posthaven)
  - "generic"     → any index page; pulls <a> links under base_url

Usage:
    python3 fetch_new_essays.py                 # all essay sources in sources.json
    python3 fetch_new_essays.py "Paul Graham"   # only one source (by name)
    python3 fetch_new_essays.py --dry-run       # list new essays, download nothing
"""

from __future__ import annotations

import html
import json
import re
import sys
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SOURCES_PATH = BASE_DIR / "sources.json"

# Reuse the exact on-disk format the rest of the pipeline expects.
from fetch_essays import slugify, write_essay_file

USER_AGENT = "Mozilla/5.0 (compatible; FounderBook/1.0; +https://github.com/ckryptickunal/Founder-Book)"


# ---------------------------------------------------------------------------
# HTTP + HTML helpers
# ---------------------------------------------------------------------------
def fetch_url(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, errors="replace")


def html_to_text(raw: str) -> str:
    """Crude but dependency-free HTML → text. Good enough for plain essay pages."""
    raw = re.sub(r"(?is)<(script|style|head|nav|footer|form).*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>", "\n", raw)
    raw = re.sub(r"(?i)</p>", "\n\n", raw)
    raw = re.sub(r"(?i)</(div|h[1-6]|li|tr)>", "\n", raw)
    text = re.sub(r"(?s)<[^>]+>", " ", raw)
    text = html.unescape(text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ---------------------------------------------------------------------------
# Index parsers — return list of {title, url}
# ---------------------------------------------------------------------------
def parse_paulgraham_index(index_html: str, base_url: str) -> list[dict]:
    essays = []
    seen = set()
    for href, title in re.findall(r'<a\s+href="([\w./-]+\.html)"[^>]*>(.*?)</a>', index_html, re.I | re.S):
        if href.startswith(("index", "rss", "articles")):
            continue
        title = re.sub(r"<[^>]+>", "", title).strip()
        if not title or href in seen:
            continue
        seen.add(href)
        url = href if href.startswith("http") else base_url.rstrip("/") + "/" + href.lstrip("/")
        essays.append({"title": html.unescape(title), "url": url})
    return essays


def parse_samaltman_index(index_html: str, base_url: str) -> list[dict]:
    essays = []
    seen = set()
    for href, title in re.findall(r'<a\s+href="(https?://blog\.samaltman\.com/[^"#]+)"[^>]*>(.*?)</a>', index_html, re.I | re.S):
        if href.rstrip("/").endswith(("archive", "blog.samaltman.com")):
            continue
        title = re.sub(r"<[^>]+>", "", title).strip()
        if not title or len(title) < 3 or href in seen:
            continue
        seen.add(href)
        essays.append({"title": html.unescape(title), "url": href})
    return essays


def parse_generic_index(index_html: str, base_url: str) -> list[dict]:
    essays = []
    seen = set()
    base = base_url.rstrip("/")
    for href, title in re.findall(r'<a\s+href="([^"#]+)"[^>]*>(.*?)</a>', index_html, re.I | re.S):
        title = re.sub(r"<[^>]+>", "", title).strip()
        if not title or len(title) < 5:
            continue
        url = href if href.startswith("http") else base + "/" + href.lstrip("/")
        if base not in url or url in seen:
            continue
        seen.add(url)
        essays.append({"title": html.unescape(title), "url": url})
    return essays


INDEX_PARSERS = {
    "paulgraham": parse_paulgraham_index,
    "samaltman": parse_samaltman_index,
    "generic": parse_generic_index,
}


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------
def load_essay_sources() -> list[dict]:
    if not SOURCES_PATH.exists():
        return []
    data = json.loads(SOURCES_PATH.read_text(encoding="utf-8"))
    return data.get("essay_sources", [])


def discover_new(source: dict) -> list[dict]:
    """Return essays present on the site but not yet on disk."""
    folder = BASE_DIR / source["folder"]
    folder.mkdir(parents=True, exist_ok=True)
    prefix = source.get("id_prefix", "essay")

    index_html = fetch_url(source["index_url"])
    parser = INDEX_PARSERS.get(source.get("kind", "generic"), parse_generic_index)
    listed = parser(index_html, source.get("base_url", source["index_url"]))

    new = []
    for essay in listed:
        video_id = f"{prefix}-{slugify(essay['title'])}"
        if (folder / f"{video_id}.txt").exists():
            continue
        essay["video_id"] = video_id
        new.append(essay)
    return new


def fetch_one_essay(source: dict, essay: dict) -> bool:
    folder = BASE_DIR / source["folder"]
    filepath = folder / f"{essay['video_id']}.txt"
    page = fetch_url(essay["url"])
    text = html_to_text(page)
    if len(text) < 400:  # almost certainly not a real essay body
        return False
    write_essay_file(
        filepath,
        essay["video_id"],
        essay["title"],
        "Unknown",
        f"{source['name']} (web)",
        essay["url"],
        text,
    )
    return True


def fetch_source(source: dict, dry_run: bool = False) -> tuple[int, int]:
    print(f"\n  Source: {source['name']} ({source.get('kind', 'generic')}) — {source['index_url']}")
    try:
        new = discover_new(source)
    except Exception as exc:  # noqa: BLE001 — never abort the batch
        print(f"    [warn] could not read index: {exc}")
        return 0, 0

    if not new:
        print("    Up to date — no new essays.")
        return 0, 0

    print(f"    {len(new)} new essay(s) found.")
    created = failed = 0
    for essay in new:
        if dry_run:
            print(f"      [dry-run] would fetch: {essay['title']}  ({essay['url']})")
            continue
        try:
            if fetch_one_essay(source, essay):
                print(f"      + {essay['title']}")
                created += 1
            else:
                print(f"      ~ skipped (too short): {essay['title']}")
                failed += 1
        except Exception as exc:  # noqa: BLE001
            print(f"      ! failed: {essay['title']} — {exc}")
            failed += 1
    return created, failed


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry_run = "--dry-run" in sys.argv
    only = args[0] if args else None

    sources = load_essay_sources()
    if only:
        sources = [s for s in sources if s["name"].lower() == only.lower()]
    if not sources:
        print("No matching essay sources in sources.json")
        return

    total_created = total_failed = 0
    for source in sources:
        c, f = fetch_source(source, dry_run=dry_run)
        total_created += c
        total_failed += f

    print(f"\n{'='*50}")
    print(f"  NEW ESSAYS: {total_created} created, {total_failed} skipped/failed")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
