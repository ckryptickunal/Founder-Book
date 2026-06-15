#!/usr/bin/env python3
"""
Founder Book — first-run setup & one-word launcher installer.

Two jobs, both designed to be friendly for someone opening the project for the
very first time:

1. run_onboarding()   — a guided, navigable walkthrough to add API keys and pick
                        models, with optional live key validation. Writes .env.
2. install_launcher() — registers a terminal keyword (like `claude`) so the user
                        can open the wiki from anywhere by typing one word.

Run the whole thing:
    python3 setup_cli.py            # keys + models + launcher keyword
    python3 setup_cli.py --keys     # only the API-key / model walkthrough
    python3 setup_cli.py --launcher # only register the terminal keyword

The Q&A CLI also calls run_onboarding() automatically the first time it starts
without a key, so a brand-new user is never dropped at a cryptic error.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.theme import Theme
from rich import box

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
PLACEHOLDER = {"", "your-gemini-api-key-here", "your-youtube-data-api-key-here"}

console = Console(theme=Theme({
    "info": "cyan",
    "success": "spring_green2",
    "warning": "gold3",
    "error": "red bold",
    "accent": "bright_cyan",
    "dim": "grey50",
}))

GEMINI_KEY_URL = "https://aistudio.google.com/apikey"
YT_KEY_URL = "https://console.cloud.google.com/  (APIs & Services → YouTube Data API v3)"

# Curated model tiers — one easy choice that sets both ingestion + Q&A models.
# Default (#1) is the free-tier-friendly model so a brand-new key works without
# enabling billing — the smoothest possible first run.
MODEL_TIERS = {
    "1": ("Recommended — works on the free tier", "gemini-2.5-flash", "gemini-2.5-flash"),
    "2": ("Fastest & lowest cost", "gemini-3.1-flash-lite", "gemini-3.1-flash-lite"),
    "3": ("Best quality — higher cost", "gemini-3.5-flash", "gemini-3.5-flash"),
    "4": ("Custom — type your own model ids", None, None),
}


# ---------------------------------------------------------------------------
# .env read / write (preserves any unknown keys already present)
# ---------------------------------------------------------------------------
def load_env() -> dict:
    values: dict[str, str] = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            values[k.strip()] = v.strip()
    return values


def write_env(values: dict) -> None:
    order = ["GEMINI_API_KEY", "YOUTUBE_API_KEY", "GEMINI_MODEL", "GEMINI_MODEL_QUERY", "GEMINI_MODEL_LINT"]
    lines = [
        "# Founder Book configuration — created by setup_cli.py",
        "# This file holds secrets. Do NOT commit it.",
        "",
    ]
    for key in order:
        if values.get(key):
            lines.append(f"{key}={values[key]}")
    for key, val in values.items():  # keep anything else the user had
        if key not in order and val:
            lines.append(f"{key}={val}")
    ENV_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    try:
        ENV_PATH.chmod(0o600)  # secrets — owner read/write only
    except OSError:
        pass


def keys_configured() -> bool:
    return load_env().get("GEMINI_API_KEY", "") not in PLACEHOLDER


# ---------------------------------------------------------------------------
# Optional live key validation
# ---------------------------------------------------------------------------
def validate_gemini_key(key: str) -> tuple[bool, str]:
    try:
        from google import genai
        client = genai.Client(api_key=key)
        next(iter(client.models.list()), None)  # cheap authenticated call
        return True, "Key works."
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)[:180]


# ---------------------------------------------------------------------------
# Guided onboarding
# ---------------------------------------------------------------------------
def _ask_gemini_key(current: str) -> str:
    console.print(Panel(
        f"Founder Book uses Google [bold]Gemini[/bold] to read transcripts and answer your questions.\n"
        f"Grab a free API key here:\n  [accent]{GEMINI_KEY_URL}[/accent]",
        title="Step 1 of 3 · Gemini API key", border_style="cyan", padding=(1, 2),
    ))
    while True:
        key = Prompt.ask("  Paste your Gemini API key", password=True, default=current or None)
        key = (key or "").strip()
        if key in PLACEHOLDER:
            console.print("  [warning]A Gemini key is required to continue.[/warning]")
            continue
        if Confirm.ask("  Test this key now?", default=True):
            with console.status("  Checking key…", spinner="dots"):
                ok, msg = validate_gemini_key(key)
            if ok:
                console.print("  [success]✓ Key works.[/success]")
                return key
            console.print(f"  [error]✗ {msg}[/error]")
            if Confirm.ask("  Use it anyway?", default=False):
                return key
            continue
        return key


def _ask_youtube_key(current: str) -> str:
    console.print(Panel(
        "Optional. Only needed to auto-discover [bold]new YouTube videos[/bold] from watched channels.\n"
        "You can skip this and add it later — everything else works without it.\n"
        f"  [dim]{YT_KEY_URL}[/dim]",
        title="Step 2 of 3 · YouTube key (optional)", border_style="cyan", padding=(1, 2),
    ))
    key = Prompt.ask("  Paste your YouTube Data API key (Enter to skip)", password=True,
                     default="" if current in PLACEHOLDER else current)
    key = (key or "").strip()
    return "" if key in PLACEHOLDER else key


def _ask_models() -> dict:
    table = Table(box=box.SIMPLE, show_header=True, header_style="bold cyan", pad_edge=False)
    table.add_column("#", style="accent", no_wrap=True)
    table.add_column("Tier")
    table.add_column("Model", style="dim")
    for num, (label, ingest, _q) in MODEL_TIERS.items():
        table.add_row(num, label, ingest or "you choose")
    console.print(Panel(table, title="Step 3 of 3 · Model quality", border_style="cyan", padding=(1, 1)))

    choice = Prompt.ask("  Pick a tier", choices=list(MODEL_TIERS), default="1")
    _, ingest, query = MODEL_TIERS[choice]
    if choice == "4":
        ingest = Prompt.ask("  Ingestion model id", default="gemini-3.1-flash-lite").strip()
        query = Prompt.ask("  Q&A model id", default=ingest).strip()
    return {"GEMINI_MODEL": ingest, "GEMINI_MODEL_QUERY": query}


def run_onboarding() -> None:
    """Interactive, navigable first-run setup. Safe to re-run anytime."""
    console.print()
    console.print(Panel(
        "[bold]Welcome to Founder Book[/bold] — a wiki of founder wisdom you can just ask.\n"
        "Three quick steps and you're in. (Ctrl-C to cancel.)",
        border_style="accent", padding=(1, 2),
    ))
    env = load_env()
    try:
        while True:
            env["GEMINI_API_KEY"] = _ask_gemini_key(env.get("GEMINI_API_KEY", ""))
            yt = _ask_youtube_key(env.get("YOUTUBE_API_KEY", ""))
            if yt:
                env["YOUTUBE_API_KEY"] = yt
            env.update(_ask_models())

            # Review & confirm — gives the user a sense of control / navigation.
            summary = Table(box=box.SIMPLE, show_header=False, pad_edge=False)
            summary.add_column(style="dim")
            summary.add_column()
            summary.add_row("Gemini key", "•••• set")
            summary.add_row("YouTube key", "•••• set" if env.get("YOUTUBE_API_KEY") else "[dim]skipped[/dim]")
            summary.add_row("Ingestion model", env.get("GEMINI_MODEL", "—"))
            summary.add_row("Q&A model", env.get("GEMINI_MODEL_QUERY", "—"))
            console.print(Panel(summary, title="Review your setup", border_style="success", padding=(1, 2)))
            if Confirm.ask("  Save these settings?", default=True):
                break
            console.print("  [dim]No problem — let's go through it again.[/dim]\n")
    except (KeyboardInterrupt, EOFError):
        console.print("\n  [warning]Setup cancelled. Run [accent]python3 setup_cli.py[/accent] anytime.[/warning]")
        return

    write_env(env)
    console.print(f"  [success]✓ Saved to {ENV_PATH.name}[/success]\n")


# ---------------------------------------------------------------------------
# One-word terminal launcher
# ---------------------------------------------------------------------------
def _shell_rc() -> Path:
    shell = os.environ.get("SHELL", "")
    home = Path.home()
    if "zsh" in shell:
        return home / ".zshrc"
    if "bash" in shell:
        return home / ".bashrc" if (home / ".bashrc").exists() else home / ".bash_profile"
    return home / ".profile"


def install_launcher(keyword: str) -> None:
    """Create an executable `keyword` on PATH that opens the wiki from anywhere."""
    keyword = keyword.strip()
    if not keyword or " " in keyword:
        console.print("  [error]Keyword must be a single word.[/error]")
        return

    bindir = Path.home() / ".local" / "bin"
    bindir.mkdir(parents=True, exist_ok=True)
    launcher = bindir / keyword
    launcher.write_text(
        f'#!/bin/sh\n'
        f'# Founder Book launcher (created by setup_cli.py)\n'
        f'exec "{sys.executable}" "{BASE_DIR / "query_wiki.py"}" "$@"\n',
        encoding="utf-8",
    )
    launcher.chmod(0o755)

    path_dirs = os.environ.get("PATH", "").split(os.pathsep)
    on_path = str(bindir) in path_dirs
    rc = _shell_rc()
    added = False
    if not on_path:
        marker = "# >>> founder-book launcher >>>"
        existing = rc.read_text(encoding="utf-8") if rc.exists() else ""
        if marker not in existing:
            with rc.open("a", encoding="utf-8") as fh:
                fh.write(f'\n{marker}\nexport PATH="$HOME/.local/bin:$PATH"\n# <<< founder-book launcher <<<\n')
            added = True

    console.print(Panel(
        f"[success]✓ Installed[/success]  [bold accent]{keyword}[/bold accent] → {launcher}\n\n"
        + (f"Added [dim]~/.local/bin[/dim] to your PATH in [dim]{rc.name}[/dim].\n"
           f"Open a new terminal (or run [accent]source {rc}[/accent]), then type:\n\n    [bold accent]{keyword}[/bold accent]\n"
           if added else
           f"Just open a new terminal and type:\n\n    [bold accent]{keyword}[/bold accent]\n")
        + f"\n[dim]{keyword} \"your question\"[/dim] also works for a one-shot answer.",
        title="Launcher ready", border_style="success", padding=(1, 2),
    ))


def _ask_keyword() -> None:
    console.print(Panel(
        "Pick a word to launch Founder Book from anywhere — like typing [dim]claude[/dim].\n"
        "Short and memorable is best (e.g. [accent]fb[/accent], [accent]wiki[/accent], [accent]founderbook[/accent]).",
        title="Terminal keyword", border_style="cyan", padding=(1, 2),
    ))
    keyword = Prompt.ask("  Keyword to type", default="founderbook").strip()
    install_launcher(keyword)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> None:
    args = sys.argv[1:]
    console.print()
    console.print("[bold accent]Founder Book setup[/bold accent]")

    only_launcher = "--launcher" in args
    only_keys = "--keys" in args

    try:
        if only_launcher:
            _ask_keyword()
            return

        if only_keys:
            run_onboarding()
            return

        if keys_configured():
            if Confirm.ask("  API keys already configured. Reconfigure them?", default=False):
                run_onboarding()
            else:
                console.print("  [dim]Keeping existing keys.[/dim]")
        else:
            run_onboarding()

        if Confirm.ask("  Set up a terminal keyword to launch Founder Book?", default=True):
            _ask_keyword()
    except (KeyboardInterrupt, EOFError):
        console.print("\n  [warning]Setup cancelled.[/warning]")
        return

    console.print("\n  [success]All set. Happy exploring![/success]\n")


if __name__ == "__main__":
    main()
