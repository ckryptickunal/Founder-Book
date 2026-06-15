# Automatic updates — deep dive

Founder Book keeps its wiki current without you doing anything. This document explains exactly how
the background sync works, how it avoids duplicate work, and how to run it on a schedule.

## The pieces

| File | Role |
|------|------|
| [`sources.json`](../sources.json) | The watch-list: which YouTube channels and essay sites to track. |
| [`auto_sync.py`](../auto_sync.py) | The engine: discover → fetch → ingest, one pass per run. |
| [`fetch_new_essays.py`](../fetch_new_essays.py) | Incremental essay scraper used by the engine. |
| [`background.py`](../background.py) | Detaches the engine from the CLI; status/force helpers. |
| `wiki/automation_state.json` | Persistent state: last-sync time + cached channel IDs per source. |
| `automation.log` | Where a background run writes its output. |
| `.auto_sync.lock` | Prevents two syncs running at once. |

## Lifecycle

1. You run `python3 query_wiki.py`. On startup it calls
   `background.maybe_launch_background_sync()`.
2. If no sync is already running **and** the last full pass was more than `LAUNCH_COOLDOWN_MIN`
   (default 180 min) ago, it launches `auto_sync.py --once` as a **detached process**
   (`start_new_session=True`, output → `automation.log`). The REPL continues immediately.
3. `auto_sync.py` takes the lockfile, reads `sources.json`, and for each source not in cooldown:
   - **YouTube:** resolve the channel ID (cached after the first time), then walk the uploads feed
     newest-first, collecting video IDs until it hits ones it already has. New IDs are written to a
     temp URL file and handed to `extract_channel.py` (Tor).
   - **Essays:** `fetch_new_essays.py` reads the site index and downloads only missing essays.
4. After fetching, a single `ingest.py --all` pass turns every new transcript/essay into wiki pages.
5. State is saved, the lock is released, and progress is in `automation.log`.

Check on it anytime from the CLI with `/sync` (status) or `/sync now` (force a pass).

## How duplicate work is avoided

An item is considered **already known** — and therefore skipped — if any of these are true:

- A transcript file for it exists on disk in the channel/essay folder.
- Its ID is listed in that channel's `_extract_state.json` (`done` or `permanent_skip`).
- Its ID is a key in `wiki/ingested.json` (the ingest manifest).

YouTube discovery additionally **stops early**: because the uploads feed is newest-first, once it
sees `DISCOVERY_STOP_AFTER_KNOWN` (default 2) consecutive pages with nothing new, it concludes it
has reached already-synced territory and stops paging. A routine check is therefore one or two API
calls, not a full channel crawl. (A brand-new, empty folder triggers a full backfill, as intended.)

## Graceful degradation

| Condition | Behavior |
|-----------|----------|
| Tor not running | Still discovers new videos and **queues** their IDs in `automation_state.json`; processes essays and ingestion normally. Extraction happens on the next pass once Tor is up. |
| `YOUTUBE_API_KEY` missing | Skips YouTube discovery; essays + ingestion still run. |
| `GEMINI_API_KEY` missing | Fetches new content but defers ingestion (and says so). |
| One source/essay errors | Logged; the rest of the pass continues. |

## Running it on a schedule (optional)

The CLI-launched background sync is enough for most people. If you want it to run even when the CLI
isn't open, use a scheduler.

### macOS — `launchd`

Create `~/Library/LaunchAgents/com.founderbook.autosync.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.founderbook.autosync</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>/ABSOLUTE/PATH/TO/auto_sync.py</string>
    <string>--once</string>
  </array>
  <key>WorkingDirectory</key><string>/ABSOLUTE/PATH/TO/repo</string>
  <key>StartInterval</key><integer>21600</integer>  <!-- every 6h -->
  <key>StandardOutPath</key><string>/ABSOLUTE/PATH/TO/repo/automation.log</string>
  <key>StandardErrorPath</key><string>/ABSOLUTE/PATH/TO/repo/automation.log</string>
</dict></plist>
```

```bash
launchctl load ~/Library/LaunchAgents/com.founderbook.autosync.plist
```

### Linux — `cron`

```cron
# every 6 hours
0 */6 * * * cd /ABSOLUTE/PATH/TO/repo && /usr/bin/python3 auto_sync.py --once >> automation.log 2>&1
```

> Keep `tor` running (`brew services start tor` / `systemctl enable --now tor`) so scheduled runs
> can extract transcripts.

### Or just loop it

```bash
python3 auto_sync.py --loop 360   # sync every 6 hours, foreground
```

## Tuning

Constants at the top of `auto_sync.py`:

| Constant | Default | Meaning |
|----------|---------|---------|
| `DEFAULT_COOLDOWN_MIN` | 360 | Minimum minutes between syncs of the same source (override with `--cooldown`). |
| `DISCOVERY_MAX_PAGES` | 40 | Safety cap on uploads-feed pages per channel (40 × 50 = 2000 videos). |
| `DISCOVERY_STOP_AFTER_KNOWN` | 2 | Stop after this many consecutive all-known pages. |

And in `background.py`: `LAUNCH_COOLDOWN_MIN` (default 180) — how recently a full pass must have run
for the CLI to skip auto-launching another.

## Troubleshooting

- **"Another auto-sync is already running"** — a previous run holds `.auto_sync.lock`. If you're
  sure none is running, the lock is reclaimed automatically when it's stale (dead PID or >2h old).
- **Nothing happens on launch** — you're within the launch cooldown. Use `/sync now` or
  `python3 auto_sync.py --force`.
- **Watch a run live:** `tail -f automation.log`.
