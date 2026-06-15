"""
Retry daemon for failed transcript fetches.

Routes each worker through a unique Tor circuit (different exit IP)
using SOCKS auth isolation. On rate limit, rotates to a fresh circuit
instantly — no cooldown needed.

Usage:
    python3 retry_failed.py              # Run until all done
    python3 retry_failed.py --workers 3  # Use 3 parallel workers (default)
    python3 retry_failed.py --status     # Show current stats
"""

import os
import sys
import time
import json
import shutil
import random
import uuid
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FAILED_LOG = os.path.join(BASE_DIR, "failed_videos.json")

sys.path.insert(0, BASE_DIR)
from transcriptor import (
    write_transcript_file,
    remove_from_failed,
    load_failed_videos,
    save_failed_videos,
    get_youtube_service,
    get_video_metadata,
)
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import GenericProxyConfig

DELAY_MIN = 3
DELAY_MAX = 6
DEFAULT_WORKERS = 3
TOR_HOST = "127.0.0.1"
TOR_PORT = 9050

lock = threading.Lock()
print_lock = threading.Lock()


def build_api(worker_id=None):
    """Each call gets a unique SOCKS auth → unique Tor circuit → unique IP."""
    tag = worker_id or uuid.uuid4().hex[:8]
    proxy_url = f"socks5://w{tag}:{uuid.uuid4().hex[:8]}@{TOR_HOST}:{TOR_PORT}"
    proxy_config = GenericProxyConfig(https_url=proxy_url)
    return YouTubeTranscriptApi(proxy_config=proxy_config)


def check_disk_space(min_mb=50):
    stat = shutil.disk_usage("/")
    return stat.free / (1024 * 1024) >= min_mb


def show_status():
    failed = load_failed_videos()
    if not failed:
        print("No failed videos. All clear!")
        return

    reasons = {}
    folders = {}
    for v in failed:
        r = v.get("reason", "unknown")
        reasons[r] = reasons.get(r, 0) + 1
        folder = os.path.basename(v.get("channel_folder", "unknown"))
        folders[folder] = folders.get(folder, 0) + 1

    retryable = reasons.get("ip_blocked", 0) + reasons.get("pending", 0)

    print(f"\n{'='*60}")
    print(f"  FAILED VIDEOS STATUS")
    print(f"{'='*60}")
    print(f"  Total in queue:  {len(failed)}")
    for r, c in sorted(reasons.items(), key=lambda x: -x[1]):
        label = {"pending": "Pending (never tried)", "ip_blocked": "IP blocked (retryable)",
                 "unplayable": "Unplayable (permanent)", "no_transcript": "No transcript (permanent)"}.get(r, r)
        print(f"  {label}: {c}")
    print(f"  Total retryable: {retryable}")

    print(f"\n  By channel:")
    for folder, count in sorted(folders.items(), key=lambda x: -x[1]):
        print(f"    {folder}: {count}")


def update_failed_reason(vid, reason, error_msg=None):
    with lock:
        failed = load_failed_videos()
        for v in failed:
            if v["id"] == vid:
                v["reason"] = reason
                v["attempts"] = v.get("attempts", 0) + 1
                v["last_attempt"] = time.strftime("%Y-%m-%dT%H:%M:%S")
                if error_msg:
                    v["last_error"] = error_msg[:100]
                break
        save_failed_videos(failed)


def log(msg):
    with print_lock:
        print(msg, flush=True)


def fetch_one(video, youtube, counter, total, start_time):
    """Fetch a single video's transcript. Returns (video_id, 'ok'|'permanent'|'blocked'|'error')."""
    vid = video["id"]
    channel_folder = video.get("channel_folder", os.path.join(BASE_DIR, "unknown_channel"))
    os.makedirs(channel_folder, exist_ok=True)

    filepath = os.path.join(channel_folder, f"{vid}.txt")
    if os.path.exists(filepath):
        with lock:
            remove_from_failed(vid)
        return vid, "ok"

    title_display = video.get("title", vid)
    if title_display == "Unknown":
        title_display = vid

    idx = counter()
    elapsed = (time.time() - start_time) / 60

    max_retries = 3
    for attempt in range(max_retries):
        try:
            ytt_api = build_api()
            transcript = ytt_api.fetch(vid, languages=["en"])

            metadata = {
                "title": video.get("title", "Unknown"),
                "published_at": video.get("published_at", "Unknown"),
                "description": video.get("description", ""),
                "channel_title": video.get("channel_title", ""),
            }
            if youtube:
                try:
                    api_meta = get_video_metadata(youtube, vid)
                    if api_meta:
                        metadata.update(api_meta)
                except Exception:
                    pass

            write_transcript_file(filepath, vid, metadata, transcript)
            with lock:
                remove_from_failed(vid)
            log(f"  [{idx}/{total} {elapsed:.0f}m] {title_display[:45]}... OK ({len(transcript)} snippets)")
            return vid, "ok"

        except Exception as e:
            error_str = str(e).lower()

            if "unplayable" in error_str or "live event" in error_str:
                log(f"  [{idx}/{total} {elapsed:.0f}m] {title_display[:45]}... PERMANENT (unplayable)")
                update_failed_reason(vid, "unplayable")
                return vid, "permanent"

            if "no transcripts" in error_str or "disabled" in error_str:
                log(f"  [{idx}/{total} {elapsed:.0f}m] {title_display[:45]}... PERMANENT (no transcript)")
                update_failed_reason(vid, "no_transcript", str(e))
                return vid, "permanent"

            if "429" in error_str or "blocked" in error_str or "ipblocked" in error_str:
                if attempt < max_retries - 1:
                    time.sleep(random.uniform(2, 5))
                    continue
                log(f"  [{idx}/{total} {elapsed:.0f}m] {title_display[:45]}... BLOCKED (retrying later)")
                update_failed_reason(vid, "ip_blocked")
                return vid, "blocked"

            if attempt < max_retries - 1:
                time.sleep(random.uniform(2, 5))
                continue

            log(f"  [{idx}/{total} {elapsed:.0f}m] {title_display[:45]}... ERROR ({str(e)[:50]})")
            update_failed_reason(vid, "ip_blocked", str(e))
            return vid, "error"

    return vid, "error"


def make_counter():
    c = [0]
    l = threading.Lock()
    def inc():
        with l:
            c[0] += 1
            return c[0]
    return inc


def run(num_workers=DEFAULT_WORKERS):
    failed = load_failed_videos()
    ip_blocked = [v for v in failed if v.get("reason") == "ip_blocked"]
    pending = [v for v in failed if v.get("reason") == "pending"]
    retryable = ip_blocked + pending

    if not retryable:
        print(f"[{time.strftime('%H:%M:%S')}] No retryable videos left!")
        return

    if not check_disk_space():
        print(f"[{time.strftime('%H:%M:%S')}] Disk space low (<50MB). Aborting.")
        return

    total = len(retryable)
    avg_time_per = 15
    eta_hours = (total * avg_time_per) / (3600 * num_workers)
    print(f"{'='*60}")
    print(f"  TRANSCRIPT FETCHER (Tor isolated circuits)")
    print(f"  Videos: {total} | Workers: {num_workers}")
    print(f"  Each worker gets a unique Tor exit IP")
    print(f"  Blocked? → new circuit, retry with fresh IP")
    print(f"  ETA: ~{eta_hours:.1f} hours")
    print(f"{'='*60}")

    youtube = None
    try:
        youtube = get_youtube_service()
    except Exception:
        print("  [meta] YouTube Data API unavailable")

    success = 0
    permanent_skip = 0
    blocked_vids = []
    start_time = time.time()
    counter = make_counter()

    with ThreadPoolExecutor(max_workers=num_workers) as pool:
        futures = {}
        for video in retryable:
            f = pool.submit(fetch_one, video, youtube, counter, total, start_time)
            futures[f] = video
            time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

        for f in as_completed(futures):
            vid, result = f.result()
            if result == "ok":
                success += 1
            elif result == "permanent":
                permanent_skip += 1
            elif result == "blocked":
                blocked_vids.append(futures[f])

    if blocked_vids:
        print(f"\n  {len(blocked_vids)} videos still blocked — retrying with fresh circuits...")
        counter2 = make_counter()
        with ThreadPoolExecutor(max_workers=num_workers) as pool:
            futures = {}
            for video in blocked_vids:
                f = pool.submit(fetch_one, video, youtube, counter2, len(blocked_vids), time.time())
                futures[f] = video
                time.sleep(random.uniform(DELAY_MIN + 2, DELAY_MAX + 4))

            for f in as_completed(futures):
                vid, result = f.result()
                if result == "ok":
                    success += 1
                elif result == "permanent":
                    permanent_skip += 1

    elapsed_total = (time.time() - start_time) / 60
    print(f"\n{'='*60}")
    print(f"  FINISHED in {elapsed_total:.0f} minutes")
    print(f"  Recovered: {success} | Permanent skips: {permanent_skip}")
    remaining = total - success - permanent_skip
    if remaining > 0:
        print(f"  Still failing: {remaining} (run again later)")
    print(f"{'='*60}")
    show_status()


def parse_int_arg(flag, default):
    if flag in sys.argv:
        idx = sys.argv.index(flag)
        if idx + 1 < len(sys.argv):
            try:
                return int(sys.argv[idx + 1])
            except ValueError:
                pass
    return default


def main():
    if "--status" in sys.argv:
        show_status()
        return
    workers = parse_int_arg("--workers", DEFAULT_WORKERS)
    run(num_workers=workers)


if __name__ == "__main__":
    main()
