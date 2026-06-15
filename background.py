"""
Background-sync launcher used by the Q&A CLI.

When `query_wiki.py` starts an interactive session it calls
`maybe_launch_background_sync()`. That spins up `auto_sync.py` as a *detached*
child process (its own session, output redirected to `automation.log`) so the
heavy work — YouTube/Tor extraction and Gemini ingestion — happens completely
in the background while you ask questions. The REPL is never blocked.

It is conservative about when it fires:
  - never if a sync is already running (lockfile present + process alive)
  - never if a full pass finished within the cooldown window
This keeps it from re-crawling on every launch while still feeling automatic.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STATE_PATH = BASE_DIR / "wiki" / "automation_state.json"
LOCK_PATH = BASE_DIR / ".auto_sync.lock"
LOG_PATH = BASE_DIR / "automation.log"
AUTO_SYNC = BASE_DIR / "auto_sync.py"

# Don't auto-launch more often than this (minutes). auto_sync also enforces a
# per-source cooldown, so this is just to avoid spawning a process needlessly.
LAUNCH_COOLDOWN_MIN = 180


def _load_json(path: Path, default):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            return default
    return default


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False


def _minutes_since(iso: str | None) -> float:
    if not iso:
        return float("inf")
    try:
        then = datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return float("inf")
    return (datetime.now(timezone.utc) - then).total_seconds() / 60.0


def is_running() -> bool:
    info = _load_json(LOCK_PATH, {})
    pid = info.get("pid")
    return bool(pid) and _pid_alive(pid)


def _spawn(extra_args: list[str]) -> bool:
    """Launch auto_sync.py detached. Returns True if a process was started."""
    if not AUTO_SYNC.exists():
        return False
    try:
        logf = open(LOG_PATH, "a", buffering=1)  # noqa: SIM115 — handed to the child
        logf.write(f"\n----- background sync launched {datetime.now().isoformat()} -----\n")
        subprocess.Popen(
            [sys.executable, str(AUTO_SYNC), "--once", *extra_args],
            cwd=str(BASE_DIR),
            stdout=logf,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            start_new_session=True,  # fully detach from the CLI's session
        )
        return True
    except Exception:  # noqa: BLE001 — background sync must never break the CLI
        return False


def maybe_launch_background_sync() -> str:
    """Launch a background sync if appropriate. Returns a one-line status."""
    if is_running():
        return "Background sync already running — new content will appear as it's processed."

    state = _load_json(STATE_PATH, {})
    since = _minutes_since(state.get("last_run"))
    if since < LAUNCH_COOLDOWN_MIN:
        return f"Wiki auto-synced {since:.0f} min ago. Type /sync now to refresh."

    if _spawn([]):
        return "Background sync started — new videos & essays will ingest while you work. /sync for status."
    return "Background sync unavailable (auto_sync.py not found)."


def force_sync() -> str:
    if is_running():
        return "A sync is already running. Watch progress in automation.log."
    if _spawn(["--force"]):
        return "Forced background sync started. Watch automation.log for progress."
    return "Could not start sync."


def status_text() -> str:
    lines = []
    if is_running():
        lines.append("Status: a background sync is RUNNING now.")
    else:
        lines.append("Status: idle.")
    state = _load_json(STATE_PATH, {})
    lines.append(f"Last full run: {state.get('last_run') or 'never'}")
    yt = state.get("youtube", {})
    if yt:
        lines.append("YouTube channels:")
        for name, st in yt.items():
            pend = len(st.get("pending_video_ids", []))
            extra = f", {pend} queued for Tor" if pend else ""
            lines.append(f"  - {name}: last sync {st.get('last_sync', 'never')}, "
                         f"last new {st.get('last_new', 0)}{extra}")
    es = state.get("essays", {})
    if es:
        lines.append("Essay sources:")
        for name, st in es.items():
            lines.append(f"  - {name}: last sync {st.get('last_sync', 'never')}")
    if LOG_PATH.exists():
        lines.append(f"Log: {LOG_PATH}")
    return "\n".join(lines)


def short_status() -> str:
    """One-line, glanceable sync state for the prompt's bottom toolbar."""
    if is_running():
        return "sync ● running…"
    state = _load_json(STATE_PATH, {})
    since = _minutes_since(state.get("last_run"))
    if since == float("inf"):
        return "sync ○ idle"
    if since < 60:
        age = f"{int(since)}m"
    elif since < 1440:
        age = f"{int(since / 60)}h"
    else:
        age = f"{int(since / 1440)}d"
    new = sum(st.get("last_new", 0) for st in state.get("youtube", {}).values())
    suffix = f" · {new} new last run" if new else ""
    return f"sync ○ idle · last {age} ago{suffix}"
