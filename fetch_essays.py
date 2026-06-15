"""
Download essay datasets from HuggingFace and convert to transcript format.

Datasets:
  - sgoel9/paul_graham_essays (215 essays)
  - sgoel9/sam_altman_essays

Usage:
    python3 fetch_essays.py
"""

import csv
import io
import re
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATASETS = [
    {
        "name": "Paul Graham",
        "url": "https://huggingface.co/datasets/sgoel9/paul_graham_essays/resolve/main/pual_graham_essays.csv",
        "id_prefix": "pg",
        "channel": "Paul Graham Essays",
        "source": "HuggingFace sgoel9/paul_graham_essays",
        "has_id_col": True,
    },
    {
        "name": "Sam Altman",
        "url": "https://huggingface.co/datasets/sgoel9/sam_altman_essays/resolve/main/sam_altman_essays.csv",
        "id_prefix": "sa",
        "channel": "Sam Altman Essays",
        "source": "HuggingFace sgoel9/sam_altman_essays",
        "has_id_col": False,
    },
]


def slugify(text: str, max_len: int = 60) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text[:max_len] or "untitled"


def write_essay_file(filepath: Path, video_id: str, title: str, date: str, channel: str, source: str, text: str):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"Title: {title}\n")
        f.write(f"Video ID: {video_id}\n")
        f.write(f"Channel: {channel}\n")
        f.write(f"Published: {date}\n")
        f.write(f"Source: {source}\n")
        f.write(f"\n{'=' * 60}\n")
        f.write("TRANSCRIPT\n")
        f.write(f"{'=' * 60}\n\n")
        f.write(text)


def fetch_dataset(config: dict) -> int:
    folder = BASE_DIR / config["name"]
    folder.mkdir(parents=True, exist_ok=True)

    print(f"\nDownloading: {config['name']} from {config['url']}")
    response = urllib.request.urlopen(config["url"])
    raw = response.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(raw))

    created = 0
    skipped = 0

    for i, row in enumerate(reader, start=1):
        title = row.get("title", "").strip() or f"Untitled {i}"
        date = row.get("date", "").strip() or "Unknown"
        text = row.get("text", "").strip()

        if not text:
            continue

        slug = slugify(title)
        video_id = f"{config['id_prefix']}-{slug}"
        filename = f"{video_id}.txt"
        filepath = folder / filename

        if filepath.exists():
            skipped += 1
            continue

        write_essay_file(filepath, video_id, title, date, config["channel"], config["source"], text)
        created += 1

    return created, skipped


def main():
    total_created = 0
    total_skipped = 0

    for config in DATASETS:
        try:
            created, skipped = fetch_dataset(config)
            total_created += created
            total_skipped += skipped
            print(f"  {config['name']}: {created} created, {skipped} skipped (already exist)")
        except Exception as e:
            print(f"  ERROR fetching {config['name']}: {e}")

    print(f"\n{'=' * 50}")
    print(f"FETCH SUMMARY")
    print(f"{'=' * 50}")
    print(f"  Total created: {total_created}")
    print(f"  Total skipped: {total_skipped}")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
