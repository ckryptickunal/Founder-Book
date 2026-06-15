#!/usr/bin/env python3
"""
Background auto-sync — keeps the wiki current with zero manual work.

It watches the YouTube channels and essay sites declared in `sources.json`,
discovers anything published since the last run, transcribes/downloads only
the *new* items, and ingests them into the wiki. It is built to run silently
in the background while you use the Q&A CLI (`query_wiki.py` launches it for
you), and it can also run standalone or on a schedule.

Design goals
------------
- Smart, not brute force: YouTube discovery walks the uploads feed newest-first
  and STOPS as soon as it reaches videos it already has — so a routine sync
  costs a couple of cheap metadata calls, not a full channel re-crawl.
- Never repeats work: an item is "known" if it is on disk, in a channel's
  extract-state file, or already in the ingest manifest. Only genuinely new
  items are fetched.
- Never blocks or crashes the CLI: runs as a detached process, writes to
  `automation.log`, guards itself with a lockfile and a cooldown.
- Degrades gracefully: no Tor → skips YouTube extraction but still does essays
  + ingest; no API key → skips that stage and reports it. One failure never
  aborts the rest.
- Fully resumable: state lives in `wiki/automation_state.json`; safe to Ctrl-C.

Deterministic building blocks reused (already in this repo):
  transcriptor.py        channel resolution + video metadata + writer
  extract_channel.py     Tor-parallel transcript extraction
  fetch_new_essays.py    incremental essay scraping
  ingest.py              Gemini wiki ingestion

Usage:
    python3 auto_sync.py                 # one sync pass (respects cooldown)
    python3 auto_sync.py --force         # ignore cooldown, sync now
    python3 auto_sync.py --dry-run       # show what WOULD be fetched
    python3 auto_sync.py --source "Garry Tan"   # only one source
    python3 auto_sync.py --no-ingest     # fetch only, skip Gemini ingestion
    python3 auto_sync.py --loop 360      # daemon: sync every 360 min
    python3 auto_sync.py --status        # print last-sync summary and exit
"""

from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except Exception:  # noqa: BLE001 — dotenv is optional; env vars may be set externally
    pass

SOURCES_PATH = BASE_DIR / "sources.json"
STATE_PATH = BASE_DIR / "wiki" / "automation_state.json"
LOCK_PATH = BASE_DIR / ".auto_sync.lock"
MANIFEST_PATH = BASE_DIR / "wiki" / "ingested.json"

TOR_HOST = "127.0.0.1"
TOR_PORT = 9050
DEFAULT_COOLDOWN_MIN = 360          # don't re-sync a source more than once / 6h
DISCOVERY_MAX_PAGES = 40            # safety cap (40 * 50 = 2000 videos)
DISCOVERY_STOP_AFTER_KNOWN = 2      # stop after N consecutive all-known pages


# ---------------------------------------------------------------------------
# Small utilities
# ---------------------------------------------------------------------------
def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def load_json(path: Path, default):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            return default
    return default


def load_config() -> dict:
    cfg = load_json(SOURCES_PATH, {})
    if not cfg:
        log(f"No sources.json found at {SOURCES_PATH} — nothing to sync.")
    return cfg


def load_state() -> dict:
    return load_json(STATE_PATH, {"last_run": None, "youtube": {}, "essays": {}})


def save_state(state: dict) -> None:
    state["last_run"] = now_iso()
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")


def tor_available() -> bool:
    try:
        with socket.create_connection((TOR_HOST, TOR_PORT), timeout=3):
            return True
    except OSError:
        return False


def minutes_since(iso: str | None) -> float:
    if not iso:
        return float("inf")
    try:
        then = datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return float("inf")
    return (datetime.now(timezone.utc) - then).total_seconds() / 60.0


# ---------------------------------------------------------------------------
# Lockfile (prevents two syncs running at once across CLI instances)
# ---------------------------------------------------------------------------
def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False


def acquire_lock() -> bool:
    if LOCK_PATH.exists():
        info = load_json(LOCK_PATH, {})
        pid = info.get("pid")
        # Stale lock from a dead process, or older than 2h → reclaim it.
        if (pid and not _pid_alive(pid)) or minutes_since(info.get("at")) > 120:
            log("Reclaiming stale auto-sync lock.")
        else:
            return False
    LOCK_PATH.write_text(json.dumps({"pid": os.getpid(), "at": now_iso()}), encoding="utf-8")
    return True


def release_lock() -> None:
    try:
        LOCK_PATH.unlink()
    except OSError:
        pass


# ---------------------------------------------------------------------------
# "Already known" set — the heart of avoiding repetition
# ---------------------------------------------------------------------------
def known_ids_for_folder(folder: Path) -> set[str]:
    known: set[str] = set()
    if folder.is_dir():
        for p in folder.glob("*.txt"):
            if not p.name.startswith("_"):
                known.add(p.stem)
    state_file = folder / "_extract_state.json"
    st = load_json(state_file, {})
    known.update(st.get("done", []))
    known.update(st.get("permanent_skip", []))
    return known


def manifest_ids() -> set[str]:
    return set(load_json(MANIFEST_PATH, {}).keys())


# ---------------------------------------------------------------------------
# YouTube discovery (incremental, newest-first, early-stop)
# ---------------------------------------------------------------------------
def discover_new_video_ids(youtube, channel_id: str, known: set[str]) -> list[str]:
    """Walk the channel uploads feed newest-first; stop once we hit known videos."""
    resp = youtube.channels().list(part="contentDetails", id=channel_id).execute()
    items = resp.get("items", [])
    if not items:
        return []
    uploads = items[0]["contentDetails"]["relatedPlaylists"]["uploads"]

    new_ids: list[str] = []
    page_token = None
    consecutive_known_pages = 0

    for _ in range(DISCOVERY_MAX_PAGES):
        pl = youtube.playlistItems().list(
            part="contentDetails", playlistId=uploads, maxResults=50, pageToken=page_token,
        ).execute()

        page_new = 0
        for item in pl.get("items", []):
            vid = item["contentDetails"]["videoId"]
            if vid in known or vid in new_ids:
                continue
            new_ids.append(vid)
            page_new += 1

        # Early stop: once we've fully entered already-synced territory.
        if page_new == 0:
            consecutive_known_pages += 1
            if consecutive_known_pages >= DISCOVERY_STOP_AFTER_KNOWN:
                break
        else:
            consecutive_known_pages = 0

        page_token = pl.get("nextPageToken")
        if not page_token:
            break

    return new_ids


# ---------------------------------------------------------------------------
# Subprocess helpers (reuse the deterministic CLIs already in this repo)
# ---------------------------------------------------------------------------
def run(cmd: list[str], timeout: int = 1800) -> int:
    log(f"$ {' '.join(cmd)}")
    try:
        proc = subprocess.run(cmd, cwd=str(BASE_DIR), timeout=timeout)
        return proc.returncode
    except subprocess.TimeoutExpired:
        log(f"  [warn] timed out after {timeout}s: {' '.join(cmd)}")
        return 1
    except Exception as exc:  # noqa: BLE001
        log(f"  [warn] command failed: {exc}")
        return 1


def extract_new_videos(folder_name: str, video_ids: list[str]) -> None:
    folder = BASE_DIR / folder_name
    folder.mkdir(parents=True, exist_ok=True)
    urls_file = folder / "_new_urls.txt"
    urls_file.write_text(
        "\n".join(f"https://www.youtube.com/watch?v={v}" for v in video_ids) + "\n",
        encoding="utf-8",
    )
    run([sys.executable, "extract_channel.py", str(urls_file), folder_name])
    try:
        urls_file.unlink()
    except OSError:
        pass


# ---------------------------------------------------------------------------
# Per-source sync
# ---------------------------------------------------------------------------
def sync_youtube(cfg: dict, state: dict, opts) -> int:
    channels = cfg.get("youtube_channels", [])
    if opts.source:
        channels = [c for c in channels if c["name"].lower() == opts.source.lower()]
    if not channels:
        return 0

    if not os.getenv("YOUTUBE_API_KEY"):
        log("[skip] YOUTUBE_API_KEY not set — cannot discover new videos.")
        return 0

    # transcriptor.get_youtube_service exits the process if the key is missing;
    # we already guarded for that above.
    from transcriptor import get_youtube_service, resolve_channel_id

    try:
        youtube = get_youtube_service()
    except SystemExit:
        log("[skip] YouTube Data API unavailable.")
        return 0

    have_tor = tor_available()
    if not have_tor:
        log("[note] Tor not running (127.0.0.1:9050) — will DISCOVER new videos "
            "but defer extraction until Tor is up. Start it with: tor")

    total_new = 0
    yt_state = state.setdefault("youtube", {})

    for ch in channels:
        name = ch["name"]
        st = yt_state.setdefault(name, {})

        if not opts.force and minutes_since(st.get("last_sync")) < opts.cooldown:
            log(f"[cooldown] {name}: synced {minutes_since(st.get('last_sync')):.0f}m ago — skipping.")
            continue

        # Resolve + cache channel_id.
        channel_id = ch.get("channel_id") or st.get("channel_id")
        if not channel_id:
            try:
                channel_id, resolved_title = resolve_channel_id(youtube, ch["query"])
                log(f"{name}: resolved to channel_id {channel_id} ({resolved_title})")
                ch["channel_id"] = channel_id  # cached back to sources.json below
            except SystemExit:
                log(f"[warn] {name}: could not resolve channel from '{ch['query']}'.")
                continue
            except Exception as exc:  # noqa: BLE001
                log(f"[warn] {name}: resolve failed — {exc}")
                continue

        folder = BASE_DIR / ch["folder"]
        known = known_ids_for_folder(folder) | manifest_ids()
        try:
            new_ids = discover_new_video_ids(youtube, channel_id, known)
        except Exception as exc:  # noqa: BLE001
            log(f"[warn] {name}: discovery failed — {exc}")
            continue

        st["channel_id"] = channel_id
        st["last_checked"] = now_iso()

        if not new_ids:
            log(f"{name}: up to date (0 new).")
            st["last_sync"] = now_iso()
            st.pop("pending_video_ids", None)  # nothing missing → clear stale queue
            continue

        log(f"{name}: {len(new_ids)} new video(s) discovered.")
        if opts.dry_run:
            for v in new_ids[:20]:
                log(f"    [dry-run] would extract https://www.youtube.com/watch?v={v}")
            continue

        if have_tor:
            extract_new_videos(ch["folder"], new_ids)
            # Reconcile: anything now on disk or marked skipped is done; only
            # genuinely still-missing IDs (e.g. blocked) stay queued.
            still_missing = sorted(set(new_ids) - known_ids_for_folder(folder))
            st["last_sync"] = now_iso()
            st["last_new"] = len(new_ids)
            st["extracted"] = len(new_ids) - len(still_missing)
            if still_missing:
                st["pending_video_ids"] = still_missing
            else:
                st.pop("pending_video_ids", None)
        else:
            # Leave a queue file so the next Tor-up run extracts them.
            st["pending_video_ids"] = sorted(set(st.get("pending_video_ids", [])) | set(new_ids))
            log(f"{name}: queued {len(new_ids)} video(s) for extraction once Tor is available.")

        total_new += len(new_ids)

    return total_new


def sync_essays(cfg: dict, state: dict, opts) -> int:
    sources = cfg.get("essay_sources", [])
    if opts.source:
        sources = [s for s in sources if s["name"].lower() == opts.source.lower()]
    if not sources:
        return 0

    es_state = state.setdefault("essays", {})
    to_run = []
    for s in sources:
        st = es_state.setdefault(s["name"], {})
        if not opts.force and minutes_since(st.get("last_sync")) < opts.cooldown:
            log(f"[cooldown] {s['name']} essays: skipping.")
            continue
        to_run.append(s)
        st["last_sync"] = now_iso()

    if not to_run:
        return 0

    cmd = [sys.executable, "fetch_new_essays.py"]
    if opts.dry_run:
        cmd.append("--dry-run")
    if opts.source:
        cmd.append(opts.source)
    run(cmd, timeout=900)
    return len(to_run)


# ---------------------------------------------------------------------------
# One full pass
# ---------------------------------------------------------------------------
def sync_once(opts) -> None:
    if not acquire_lock():
        log("Another auto-sync is already running — exiting.")
        return
    try:
        cfg = load_config()
        if not cfg:
            return
        state = load_state()

        log("=" * 56)
        log("AUTO-SYNC pass starting")
        log("=" * 56)

        new_videos = sync_youtube(cfg, state, opts)
        sync_essays(cfg, state, opts)

        # Persist resolved channel_ids back to sources.json (one-time caching).
        try:
            SOURCES_PATH.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
        except OSError:
            pass

        save_state(state)

        if opts.dry_run:
            log("Dry-run complete — nothing fetched or ingested.")
            return

        # Single ingest pass picks up every new transcript + essay at once.
        if opts.no_ingest:
            log("[skip] --no-ingest set; new content fetched but not ingested.")
        elif not os.getenv("GEMINI_API_KEY"):
            log("[skip] GEMINI_API_KEY not set — fetched content not yet ingested.")
        else:
            log("Ingesting new content into the wiki...")
            run([sys.executable, "ingest.py", "--all", "--workers", "20"], timeout=3600)

        log(f"AUTO-SYNC pass complete. New videos this pass: {new_videos}.")
    finally:
        release_lock()


def show_status() -> None:
    state = load_state()
    print(f"\n  Last full run: {state.get('last_run') or 'never'}")
    print("\n  YouTube channels:")
    for name, st in state.get("youtube", {}).items():
        pend = len(st.get("pending_video_ids", []))
        print(f"    {name:<18} last sync {st.get('last_sync', 'never')}"
              f"  last new: {st.get('last_new', 0)}" + (f"  pending: {pend}" if pend else ""))
    print("\n  Essay sources:")
    for name, st in state.get("essays", {}).items():
        print(f"    {name:<18} last sync {st.get('last_sync', 'never')}")
    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Background auto-sync for the founder wiki.")
    parser.add_argument("--once", action="store_true", help="Run a single pass (default).")
    parser.add_argument("--loop", type=int, metavar="MIN", help="Daemon mode: sync every MIN minutes.")
    parser.add_argument("--force", action="store_true", help="Ignore the per-source cooldown.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be fetched; change nothing.")
    parser.add_argument("--no-ingest", action="store_true", help="Fetch new content but skip ingestion.")
    parser.add_argument("--source", metavar="NAME", help="Limit to a single source by name.")
    parser.add_argument("--cooldown", type=int, default=DEFAULT_COOLDOWN_MIN,
                        help=f"Minutes between syncs of the same source (default {DEFAULT_COOLDOWN_MIN}).")
    parser.add_argument("--status", action="store_true", help="Print last-sync summary and exit.")
    opts = parser.parse_args()

    if opts.status:
        show_status()
        return

    if opts.loop:
        log(f"Auto-sync daemon: every {opts.loop} min. Ctrl-C to stop.")
        while True:
            sync_once(opts)
            log(f"Next pass in {opts.loop} min.")
            time.sleep(opts.loop * 60)
    else:
        sync_once(opts)


if __name__ == "__main__":
    main()
