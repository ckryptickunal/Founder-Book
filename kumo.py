"""
Kumo — the living terminal companion for the Founder Book Q&A CLI.

Kumo is a small ASCII cat that actually *moves*: it blinks and stretches on
greeting, looks around and mutters quirky status while the wiki is being
searched, "talks" while the answer streams in, and does a little sparkly bounce
when it lands. Colour is used with intent — calm cyan at rest, warm amber while
thinking, bright green when it succeeds, muted red when it comes up empty — so
the mood of the moment reads at a glance and the tool feels alive and friendly.

Everything degrades gracefully: when stdout is not a TTY (piped/redirected),
all animation is skipped and the work still happens, so scripting stays clean.

This module owns Kumo's whole personality (art, colour, motion, voice) so the
REPL in query_wiki.py can just say what's happening:

    kumo.greet()
    pages = kumo.think(search_pages, question)        # animates while it works
    answer = kumo.stream_answer(stream, transform=fix) # animates while it talks
    kumo.celebrate()
"""

from __future__ import annotations

import random
import threading
import time
from typing import Callable, Iterable

from rich.console import Console, Group
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

PET_NAME = "Kumo"

# --- Voice ----------------------------------------------------------------
GREETINGS = [
    "Source-of-truth ready. Ask me anything.",
    "Plan → retrieve → answer → verify.",
    "I cite evidence and keep unknowns unknown.",
    "Ready to search your wiki memory.",
    "Ask a question, or /ingest a file.",
]

# Claude-Code-style quirky gerunds shown (and rotated) while Kumo searches.
THINKING_STATUS = [
    "Percolating", "Pondering", "Spelunking the archive", "Consulting the founders",
    "Cross-referencing mental models", "Distilling wisdom", "Connecting the dots",
    "Mining transcripts", "Tracing the through-line", "Rummaging the wiki",
    "Triangulating sources", "Channeling YC", "Reticulating splines", "Noodling",
    "Synthesizing", "Foraging for evidence", "Untangling threads", "Marinating",
    "Chasing footnotes", "Reading between the lines",
]

SUCCESS_MSGS = [
    "Evidence found.",
    "Answer built from wiki memory.",
    "Verified against retrieved pages.",
    "Here's the grounded answer.",
]

EMPTY_MSGS = [
    "Nothing matched — the unknown stays unknown.",
    "Not observed in the wiki yet.",
    "No evidence found for that one.",
]

# --- Art (3 lines each, padded to equal width for jitter-free animation) ---
def _f(a: str, b: str, c: str) -> list[str]:
    w = max(len(a), len(b), len(c))
    return [a.ljust(w), b.ljust(w), c.ljust(w)]

IDLE = [
    _f(r" /\_/\ ", r"( o.o )", r"  > ^ <"),
    _f(r" /\_/\ ", r"( o.o )", r"  > ^ <"),
    _f(r" /\_/\ ", r"( -.- )", r"  > ^ <"),   # blink
]
STRETCH = [
    _f(r" /\_/\ ", r"( o.o )", r"  > ^ <"),
    _f(r" /\_/\~", r"( o.o )", r"  > ^ <"),    # tail flick
    _f(r" /\_/\ ", r"( ^.^ )", r"  > w <"),
]
THINK = [
    _f(r" /\_/\ ", r"( o.o )", r"  > ? <"),
    _f(r" /\_/\ ", r"( o.O )", r"  > ? <"),
    _f(r" /\_/\ ", r"( O.o )", r"  > ? <"),
    _f(r" /\_/\ ", r"( -.- )", r"  > ~ <"),
]
HAPPY = [
    _f(r"✦/\_/\ ", r"( ^.^ )", r"  >‿< ✦"),
    _f(r" /\_/\✦", r"( ^o^ )", r"✦ >‿<  "),
    _f(r"✦/\_/\ ", r"( ^.^ )", r"  >‿< ✦"),
]
SAD = [
    _f(r" /\_/\ ", r"( ._. )", r"  > ! <"),
]
SPEAK_FACES = ["( o.o )", "( ^.^ )", "( ^o^ )", "( ^.^ )"]

# --- Colour per mood (intentional, harmonious) ----------------------------
MOOD = {
    "idle":     {"face": "cyan",          "mouth": "bright_cyan",  "border": "cyan",          "msg": "cyan"},
    "thinking": {"face": "gold3",         "mouth": "yellow1",      "border": "gold3",         "msg": "yellow"},
    "speaking": {"face": "spring_green3", "mouth": "green1",       "border": "spring_green3", "msg": "green"},
    "happy":    {"face": "spring_green2", "mouth": "bright_green", "border": "spring_green2", "msg": "bright_green"},
    "sad":      {"face": "indian_red",    "mouth": "red1",         "border": "indian_red",    "msg": "red"},
}


class Kumo:
    def __init__(self, console: Console):
        self.console = console

    @property
    def alive(self) -> bool:
        """Only animate on a real terminal."""
        return self.console.is_terminal

    # -- rendering ----------------------------------------------------------
    def _face(self, mood: str, frame: list[str], message: str = "") -> Panel:
        c = MOOD.get(mood, MOOD["idle"])
        body = Text()
        body.append(frame[0] + "\n", style=c["face"])
        body.append(frame[1] + "\n", style=f"bold {c['face']}")
        body.append(frame[2], style=c["mouth"])
        if message:
            body.append("\n\n  " + message, style=c["msg"])
        return Panel(body, title=PET_NAME, title_align="left", border_style=c["border"], width=38)

    def say(self, mood: str = "idle", message: str = "") -> None:
        """Static (non-animated) appearance — used for quick feedback moments."""
        frames = {"idle": IDLE, "thinking": THINK, "happy": HAPPY, "sad": SAD}.get(mood, IDLE)
        self.console.print(self._face(mood, frames[0], message))

    def _animate(self, mood: str, frames: list[list[str]], message: str, seconds: float, fps: int = 12) -> None:
        if not self.alive:
            self.say(mood, message)
            return
        steps = max(1, int(seconds * fps))
        with Live(console=self.console, refresh_per_second=fps, transient=True) as live:
            for i in range(steps):
                live.update(self._face(mood, frames[i % len(frames)], message))
                time.sleep(1 / fps)
        self.console.print(self._face(mood, frames[0], message))  # settle, stays in scrollback

    # -- public moments -----------------------------------------------------
    def greet(self, message: str | None = None) -> None:
        self._animate("idle", STRETCH, message or random.choice(GREETINGS), seconds=0.8)

    def farewell(self, message: str = "See you next time!") -> None:
        self.say("happy", message)

    def empty(self, remedy: str = "") -> None:
        self.say("sad", random.choice(EMPTY_MSGS))
        if remedy:
            self.console.print(f"  [dim]{remedy}[/dim]")

    def celebrate(self, message: str | None = None) -> None:
        self._animate("happy", HAPPY, message or random.choice(SUCCESS_MSGS), seconds=0.7, fps=10)

    def think(self, work: Callable, *args, **kwargs):
        """Run blocking work in a thread while Kumo looks around and mutters
        rotating quirky status. Returns work()'s result; re-raises its errors."""
        if not self.alive:
            return work(*args, **kwargs)

        box: dict = {}

        def runner():
            try:
                box["value"] = work(*args, **kwargs)
            except BaseException as exc:  # noqa: BLE001 — surfaced to caller below
                box["error"] = exc

        worker = threading.Thread(target=runner, daemon=True)
        worker.start()

        start = time.time()
        verb = random.choice(THINKING_STATUS)
        last_change = start
        i = 0
        interrupted = False
        try:
            with Live(console=self.console, refresh_per_second=12, transient=True) as live:
                while worker.is_alive():
                    now = time.time()
                    if now - last_change > 1.6:
                        verb = random.choice(THINKING_STATUS)
                        last_change = now
                    elapsed = int(now - start)
                    msg = f"{verb}…" if elapsed < 2 else f"{verb}… ({elapsed}s · ctrl-c to cancel)"
                    live.update(self._face("thinking", THINK[i % len(THINK)], msg))
                    i += 1
                    time.sleep(1 / 12)
        except KeyboardInterrupt:
            interrupted = True
        # The work is not cancellable, so always wait for it rather than leaving
        # an orphaned thread churning the filesystem behind the next query.
        worker.join()
        if interrupted:
            raise KeyboardInterrupt
        if "error" in box:
            raise box["error"]
        return box.get("value")

    def stream_answer(self, chunks: Iterable, transform: Callable[[str], str] | None = None) -> str:
        """Render a streaming answer live (Kumo 'talks' above the text), then
        return the full text (optionally transformed)."""
        buf = ""
        if not self.alive:
            for ch in chunks:
                buf += getattr(ch, "text", "") or ""
            return transform(buf) if transform else buf

        i = 0
        # "ellipsis" keeps the live region within the viewport so the transient
        # erase is always clean — long answers can't leave duplicated lines
        # behind before the final panel prints.
        with Live(console=self.console, refresh_per_second=12, transient=True, vertical_overflow="ellipsis") as live:
            for ch in chunks:
                piece = getattr(ch, "text", "") or ""
                if not piece:
                    continue
                buf += piece
                i += 1
                head = Text(f" {SPEAK_FACES[i % len(SPEAK_FACES)]} Kumo is answering…", style="green")
                live.update(Group(head, Markdown(buf)))
        return transform(buf) if transform else buf
