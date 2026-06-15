#!/usr/bin/env python3
"""
YouTube Channel Transcript Extractor
=====================================

Extracts transcripts for an entire channel (or any list of YouTube URLs)
using parallel Tor circuits for reliable, block-free operation at scale.

How it works:
  - Each parallel worker routes through a unique Tor exit IP
    (via SOCKS auth isolation — Tor's IsolateSOCKSAuth feature)
  - If one exit IP is blocked, the worker simply gets a fresh circuit
  - State is saved per-video to disk — safe to Ctrl-C and restart anytime
  - Typically extracts ~25-30 videos/min with 5 workers

Prerequisites:
  1. Tor running locally:  brew install tor && tor
  2. Python deps:          pip install youtube-transcript-api pysocks google-api-python-client python-dotenv
  3. .env file with:       YOUTUBE_API_KEY=your_key_here

Usage:
  # Extract a channel
  python3 extract_channel.py urls.txt "Channel Name"

  # Extract with more workers (default: 5)
  python3 extract_channel.py urls.txt "Channel Name" --workers 8

  # Check status of a previous/running extraction
  python3 extract_channel.py --status "Channel Name"

  # Resume a stopped extraction (just re-run the same command)
  python3 extract_channel.py urls.txt "Channel Name"

URL file format:
  One YouTube URL per line, e.g.:
    https://www.youtube.com/watch?v=dQw4w9WgXcQ
    https://www.youtube.com/watch?v=abcdef12345
"""

import os
import sys
import time
import json
import random
import uuid
import argparse
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import parse_qs, urlparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import GenericProxyConfig
from transcriptor import write_transcript_file, get_youtube_service, get_video_metadata

# ---------------------------------------------------------------------------
# Config — tune these if needed
# ---------------------------------------------------------------------------
TOR_HOST = "127.0.0.1"
TOR_PORT = 9050
DEFAULT_WORKERS = 5
STAGGER_RANGE = (1.0, 2.0)   # delay between submitting jobs to the pool
MAX_CIRCUIT_RETRIES = 4       # fresh Tor circuits to try per video before giving up


# ---------------------------------------------------------------------------
# Tor circuit builder
# ---------------------------------------------------------------------------
def build_tor_api():
    """Create a YouTubeTranscriptApi routed through a fresh Tor circuit.

    Tor's IsolateSOCKSAuth ensures that different username:password combos
    get different circuits (and therefore different exit IPs). We generate
    a random combo each time so every call gets a unique IP.
    """
    tag = uuid.uuid4().hex[:8]
    pwd = uuid.uuid4().hex[:8]
    proxy_url = f"socks5://w{tag}:{pwd}@{TOR_HOST}:{TOR_PORT}"
    return YouTubeTranscriptApi(proxy_config=GenericProxyConfig(https_url=proxy_url))


# ---------------------------------------------------------------------------
# State management (tracks progress on disk for resume)
# ---------------------------------------------------------------------------
def _state_path(channel_folder):
    return os.path.join(channel_folder, "_extract_state.json")


def load_state(channel_folder):
    p = _state_path(channel_folder)
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return {
        "done": [],
        "permanent_skip": [],
        "stats": {"success": 0, "skipped": 0, "failed": 0, "blocks_hit": 0},
    }


def save_state(channel_folder, state):
    with open(_state_path(channel_folder), "w") as f:
        json.dump(state, f, indent=2)


# ---------------------------------------------------------------------------
# URL parsing
# ---------------------------------------------------------------------------
def parse_urls(filepath):
    """Extract video IDs from a file of YouTube URLs (one per line)."""
    ids = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            q = parse_qs(urlparse(line).query)
            if "v" in q:
                ids.append(q["v"][0])
    return ids


# ---------------------------------------------------------------------------
# Error classification
# ---------------------------------------------------------------------------
def _is_permanent(err):
    e = err.lower()
    return any(k in e for k in [
        "no transcripts", "disabled", "unplayable",
        "live event", "private video", "video unavailable",
    ])


# ---------------------------------------------------------------------------
# Single-video fetch (called by each worker)
# ---------------------------------------------------------------------------
def fetch_one(vid, channel_folder, channel_name, youtube, lock, state, counters, total, start_time):
    """Fetch one video's transcript. Tries up to MAX_CIRCUIT_RETRIES fresh Tor circuits."""
    filepath = os.path.join(channel_folder, f"{vid}.txt")

    # Already on disk
    if os.path.exists(filepath):
        with lock:
            if vid not in state["done"]:
                state["done"].append(vid)
            counters["ok"] += 1
        return

    # Fetch metadata (via YouTube Data API — not rate-limited)
    meta = {"title": "Unknown", "channel_title": channel_name}
    if youtube:
        try:
            m = get_video_metadata(youtube, vid)
            if m:
                meta.update(m)
        except Exception:
            pass

    title = meta.get("title", vid)[:55]

    for attempt in range(MAX_CIRCUIT_RETRIES):
        try:
            api = build_tor_api()
            transcript = api.fetch(vid, languages=["en"])
            write_transcript_file(filepath, vid, meta, transcript)

            with lock:
                counters["ok"] += 1
                state["done"].append(vid)
                elapsed = (time.time() - start_time) / 60
                n = counters["ok"] + counters["skip"] + counters["fail"]
                print(f"  [{n}/{total} {elapsed:.0f}m] {title}  OK ({len(transcript)})", flush=True)
            return

        except Exception as e:
            err = str(e)
            if _is_permanent(err):
                with lock:
                    counters["skip"] += 1
                    state["permanent_skip"].append(vid)
                    n = counters["ok"] + counters["skip"] + counters["fail"]
                    print(f"  [{n}/{total}] {title}  SKIP (no transcript)", flush=True)
                return

            # Blocked on this circuit — get a fresh one
            if attempt < MAX_CIRCUIT_RETRIES - 1:
                time.sleep(random.uniform(1, 3))
                continue

    # All retries exhausted
    with lock:
        counters["fail"] += 1
        state["stats"]["blocks_hit"] += 1
        n = counters["ok"] + counters["skip"] + counters["fail"]
        print(f"  [{n}/{total}] {title}  FAIL ({MAX_CIRCUIT_RETRIES} circuits tried)", flush=True)


# ---------------------------------------------------------------------------
# Main extraction loop
# ---------------------------------------------------------------------------
def extract(video_ids, channel_folder, channel_name, num_workers):
    os.makedirs(channel_folder, exist_ok=True)
    state = load_state(channel_folder)
    done_set = set(state["done"])
    perm_set = set(state["permanent_skip"])

    remaining = [v for v in video_ids if v not in done_set and v not in perm_set]

    print(f"\n{'='*60}")
    print(f"  TRANSCRIPT EXTRACTOR (Tor parallel circuits)")
    print(f"{'='*60}")
    print(f"  Channel:    {channel_name}")
    print(f"  Total:      {len(video_ids)}")
    print(f"  Done:       {len(done_set)}")
    print(f"  Skipped:    {len(perm_set)}")
    print(f"  Remaining:  {len(remaining)}")
    print(f"  Workers:    {num_workers}")
    print(f"  Tor proxy:  socks5://{TOR_HOST}:{TOR_PORT}")
    print(f"  State file: {_state_path(channel_folder)}")
    print(f"{'='*60}\n", flush=True)

    if not remaining:
        print("All videos already extracted!")
        return

    # YouTube Data API for metadata (titles, dates, etc.)
    youtube = None
    try:
        youtube = get_youtube_service()
    except Exception:
        print("  [warn] YouTube Data API unavailable — titles will be 'Unknown'")

    lock = threading.Lock()
    counters = {"ok": 0, "skip": 0, "fail": 0}
    start = time.time()

    with ThreadPoolExecutor(max_workers=num_workers) as pool:
        futures = []
        for vid in remaining:
            f = pool.submit(
                fetch_one, vid, channel_folder, channel_name,
                youtube, lock, state, counters, len(remaining), start,
            )
            futures.append(f)
            time.sleep(random.uniform(*STAGGER_RANGE))

        for f in as_completed(futures):
            f.result()

    save_state(channel_folder, state)

    elapsed = (time.time() - start) / 60
    total_files = len([f for f in os.listdir(channel_folder) if f.endswith(".txt")])

    print(f"\n{'='*60}")
    print(f"  FINISHED in {elapsed:.1f} min")
    print(f"  Transcripts: {total_files}")
    print(f"  This run — OK: {counters['ok']} | Skipped: {counters['skip']} | Failed: {counters['fail']}")
    if counters["fail"] > 0:
        print(f"  Re-run the same command to retry failed videos.")
    print(f"{'='*60}")


# ---------------------------------------------------------------------------
# Status display
# ---------------------------------------------------------------------------
def show_status(channel_folder):
    folder = os.path.join(BASE_DIR, channel_folder) if not os.path.isabs(channel_folder) else channel_folder
    if not os.path.isdir(folder):
        print(f"  No folder found: {folder}")
        return

    state = load_state(folder)
    total_files = len([f for f in os.listdir(folder) if f.endswith(".txt")])

    print(f"\n  Channel folder: {folder}")
    print(f"  Transcript files on disk: {total_files}")
    print(f"  State — done: {len(state['done'])}")
    print(f"  State — permanent skips: {len(state['permanent_skip'])}")
    print(f"  Stats — blocks hit: {state['stats'].get('blocks_hit', 0)}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Extract YouTube transcripts via parallel Tor circuits.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 extract_channel.py urls.txt "Garry Tan"
  python3 extract_channel.py urls.txt "Garry Tan" --workers 8
  python3 extract_channel.py --status "Garry Tan"
        """,
    )
    parser.add_argument("urls_file", nargs="?", help="File with one YouTube URL per line")
    parser.add_argument("channel", help="Channel folder name (created if needed)")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS,
                        help=f"Parallel workers (default: {DEFAULT_WORKERS})")
    parser.add_argument("--status", action="store_true", help="Show extraction status and exit")

    args = parser.parse_args()
    channel_folder = os.path.join(BASE_DIR, args.channel)

    if args.status:
        show_status(channel_folder)
        return

    if not args.urls_file:
        parser.error("urls_file is required (unless using --status)")

    video_ids = parse_urls(args.urls_file)
    print(f"Parsed {len(video_ids)} video IDs from {args.urls_file}")

    extract(video_ids, channel_folder, args.channel, args.workers)


if __name__ == "__main__":
    main()
