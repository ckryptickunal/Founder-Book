"""
Autonomous pipeline: fetch transcripts, ingest into wiki, self-verify.

Runs the full loop without needing Opus to intervene:
1. Retry failed YouTube transcript fetches (if any retryable)
2. Fetch essay datasets (idempotent)
3. Ingest all new content into wiki
4. Rebuild index
5. Self-verify and report

Usage:
    python3 run_pipeline.py              # One full pass
    python3 run_pipeline.py --loop 30    # Repeat every 30 minutes
"""

import json
import subprocess
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FAILED_VIDEOS = BASE_DIR / "failed_videos.json"
MANIFEST = BASE_DIR / "wiki" / "ingested.json"


def run_script(cmd: list[str], label: str) -> tuple[int, str]:
    print(f"\n{'─'*50}")
    print(f"  STEP: {label}")
    print(f"{'─'*50}")
    result = subprocess.run(
        cmd, cwd=str(BASE_DIR), capture_output=True, text=True, timeout=600
    )
    output = result.stdout + result.stderr
    if result.returncode != 0:
        print(f"  [WARN] Exit code {result.returncode}")
    last_lines = output.strip().split("\n")[-15:]
    for line in last_lines:
        print(f"  {line}")
    return result.returncode, output


def count_retryable() -> int:
    if not FAILED_VIDEOS.exists():
        return 0
    try:
        data = json.loads(FAILED_VIDEOS.read_text())
        return sum(1 for v in data if v.get("reason") in ("ip_blocked", "pending"))
    except (json.JSONDecodeError, ValueError):
        return 0


def count_manifest() -> int:
    if not MANIFEST.exists():
        return 0
    try:
        return len(json.loads(MANIFEST.read_text()))
    except (json.JSONDecodeError, ValueError):
        return 0


def discover_transcripts() -> int:
    skip_dirs = {".cursor", "__pycache__", "wiki", ".git"}
    count = 0
    for child in BASE_DIR.iterdir():
        if not child.is_dir() or child.name in skip_dirs or child.name.startswith("."):
            continue
        count += sum(1 for p in child.glob("*.txt") if not p.name.startswith("_"))
    return count


def run_pipeline():
    print(f"\n{'='*50}")
    print(f"  AUTONOMOUS PIPELINE")
    print(f"  {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")

    # Step 1: Retry failed transcripts (small batch, won't block long)
    retryable = count_retryable()
    if retryable > 0:
        run_script(
            [sys.executable, "retry_failed.py", "--batch", "5"],
            f"Retry failed transcripts ({retryable} retryable)"
        )
    else:
        print(f"\n  [skip] No retryable transcript failures.")

    # Step 2: Fetch essays (idempotent, skips existing)
    run_script(
        [sys.executable, "fetch_essays.py"],
        "Fetch essay datasets"
    )

    # Step 3: Ingest new content
    run_script(
        [sys.executable, "ingest.py", "--all", "--workers", "40"],
        "Ingest new content into wiki"
    )

    # Step 4: Self-verify
    total_on_disk = discover_transcripts()
    total_ingested = count_manifest()
    remaining = total_on_disk - total_ingested
    retryable_now = count_retryable()

    print(f"\n{'='*50}")
    print(f"  PIPELINE REPORT")
    print(f"{'='*50}")
    print(f"  Transcripts on disk: {total_on_disk}")
    print(f"  Ingested in wiki:    {total_ingested}")
    print(f"  Gap (need ingest):   {remaining}")
    print(f"  YouTube retryable:   {retryable_now}")
    status = "ALL CLEAR" if remaining == 0 and retryable_now == 0 else "WORK REMAINING"
    print(f"  Status: {status}")
    print(f"{'='*50}\n")

    return remaining == 0


def main():
    loop_flag = "--loop" in sys.argv
    interval = 30

    if loop_flag:
        idx = sys.argv.index("--loop")
        if idx + 1 < len(sys.argv):
            try:
                interval = int(sys.argv[idx + 1])
            except ValueError:
                pass

        print(f"Pipeline loop mode: every {interval} minutes. Ctrl+C to stop.")
        while True:
            run_pipeline()
            print(f"  Next run in {interval} minutes...")
            time.sleep(interval * 60)
    else:
        run_pipeline()


if __name__ == "__main__":
    main()
