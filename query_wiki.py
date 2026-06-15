"""
Interactive Wiki Q&A CLI with a terminal pet companion.

Usage:
    python3 query_wiki.py              # Interactive mode
    python3 query_wiki.py "question"   # One-shot mode
"""

import argparse
import json
import os
import random
import re
import shlex
import sys
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme

from ingest import WIKI_DIR, SYNTHESIS_DIR, BASE_DIR, MANIFEST_PATH, append_log, rebuild_index, slugify, today
from ingest_file import ingest_files, local_video_id
from query_skills import render_skills_help, route_skill
from kumo import Kumo

try:
    import background  # background auto-sync of new videos/essays
except Exception:  # pragma: no cover — sync is optional, never break the CLI
    background = None

INDEX_PATH = WIKI_DIR / "index.md"


def _load_manifest() -> dict:
    """Load the ingestion manifest keyed by video_id."""
    if MANIFEST_PATH.exists():
        import json
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {}


def _resolve_raw_transcript(page_path: Path, manifest: dict) -> str | None:
    """Given a wiki source page path, find and read the raw transcript file.
    Extracts video_id from the filename to handle renamed pages."""
    stem = page_path.stem
    # Video ID is the part before the first hyphen (for YouTube) or the full stem (for essays/local)
    video_id = stem.split("-")[0] if stem[0] != "-" else "-" + stem.split("-", 2)[1]

    entry = manifest.get(video_id)
    if not entry:
        # Try matching the full stem as video_id (for pg- and sa- essay IDs)
        for key, val in manifest.items():
            wiki_page = val.get("wiki_page", "")
            if stem in wiki_page or page_path.name in wiki_page:
                entry = val
                break

    if not entry:
        return None

    source_file = entry.get("source_file", "")
    full_path = BASE_DIR / source_file
    if full_path.exists():
        return full_path.read_text(encoding="utf-8", errors="replace")
    return None

# Intentional, harmonious palette — colour reflects what's happening (calm cyan
# at rest, warm amber while working, bright green on success, soft red on miss).
# highlight=False stops Rich from auto-rainbowing numbers/paths inside answers;
# all colour below is applied on purpose.
console = Console(highlight=False, theme=Theme({
    "info": "cyan",
    "success": "spring_green2",
    "warning": "gold3",
    "error": "red bold",
    "pet": "cyan",
    "pet_border": "cyan",
    "accent": "bright_cyan",
    "cite": "bright_cyan",
    "dim": "grey50",
}))

# Kumo — the living terminal companion (animation, mood colour, quirky status).
pet = Kumo(console)

# Pet states and expressions
PET_NAME = "Kumo"
PET_IDLE = [
    r" /\_/\ ",
    r"( o.o )",
    r" > ^ < ",
]
PET_THINKING = [
    r" /\_/\ ",
    r"( -.- )",
    r" > ? < ",
]
PET_HAPPY = [
    r" /\_/\ ",
    r"( ^.^ )",
    r" > ✓ < ",
]
PET_SAD = [
    r" /\_/\ ",
    r"( ._. )",
    r" > ! < ",
]

PET_GREETINGS = [
    "Source-of-truth ready. Ask me anything.",
    "Plan -> retrieve -> answer -> verify.",
    "I will cite evidence and keep unknowns unknown.",
    "Ready to search your wiki memory.",
    "Ask a question, or /ingest a local file.",
]

PET_THINKING_MSGS = [
    "Investigating evidence...",
    "Checking the source-of-truth pages...",
    "Retrieving relevant memory...",
    "Separating observed facts from unknowns...",
    "Building an evidence pack...",
    "Scanning sources before answering...",
    "No unobserved claims. Looking it up...",
]

PET_SUCCESS_MSGS = [
    "Evidence found.",
    "Answer built from wiki memory.",
    "Verified against retrieved pages.",
    "Here is the grounded answer.",
]

PET_EMPTY_MSGS = [
    "No evidence found. Unknown stays unknown.",
    "Nothing matched. Try broader terms or /ingest a source.",
    "Not observed in the wiki yet.",
]


def extract_local_file_paths(text: str) -> list[Path]:
    paths: list[Path] = []
    seen: set[str] = set()

    for match in re.finditer(r"((?:~|/Users|/tmp|/private)[^'\"\n]*?\.(?:pdf|txt|md|markdown|html|htm))", text, re.IGNORECASE):
        path = Path(match.group(1).strip()).expanduser()
        key = str(path)
        if key not in seen:
            paths.append(path)
            seen.add(key)

    try:
        parts = shlex.split(text)
    except ValueError:
        parts = text.split()

    for part in parts:
        cleaned = part.strip().strip("'\"")
        if cleaned.startswith(("~", "/Users/", "/tmp/", "/private/")):
            path = Path(cleaned).expanduser()
            key = str(path)
            if key not in seen:
                paths.append(path)
                seen.add(key)
    return paths


def source_page_for_local_path(path: Path) -> Path | None:
    video_id = local_video_id(path)
    matches = sorted((WIKI_DIR / "sources").glob(f"{video_id}-*.md"))
    return matches[0] if matches else None


def page_dict(path: Path, score: int) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    return {"path": path, "title": page_title(text, path), "score": score, "text": text}


def local_page_dict(local_path: Path, source_page: Path, score: int) -> dict:
    page = page_dict(source_page, score)
    transcript_path = Path("Local Files") / f"{local_video_id(local_path)}.txt"
    full_transcript_path = source_page.parents[2] / transcript_path
    if full_transcript_path.exists():
        transcript_text = full_transcript_path.read_text(encoding="utf-8", errors="replace")
        page["text"] += f"\n\n## Extracted Local File Text\n\n{transcript_text}"
    return page


def enrich_local_source_with_raw_text(page: dict) -> dict:
    video_id_match = re.search(r"^video_id:\s*(local-[^\s]+)", page["text"], re.MULTILINE)
    if not video_id_match:
        return page

    transcript_path = WIKI_DIR.parent / "Local Files" / f"{video_id_match.group(1)}.txt"
    if transcript_path.exists():
        transcript_text = transcript_path.read_text(encoding="utf-8", errors="replace")
        page["text"] += f"\n\n## Extracted Local File Text\n\n{transcript_text}"
    return page


def ensure_question_files_ingested(question: str) -> list[dict]:
    paths = [path for path in extract_local_file_paths(question) if path.exists()]
    if not paths:
        return []
    return ingest_files(paths)


def show_pet(state: str = "idle", message: str = ""):
    """Static companion appearance — delegates to the Kumo character module."""
    pet.say(state, message)


def timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def configure_gemini():
    load_dotenv(BASE_DIR / ".env")
    api_key = os.getenv("GEMINI_API_KEY")
    placeholder = (None, "", "your-gemini-api-key-here")
    # First run with no key on a real terminal → walk the user through setup.
    if api_key in placeholder and sys.stdin.isatty():
        try:
            import setup_cli
            setup_cli.run_onboarding()
        except Exception:  # pragma: no cover — onboarding is best-effort
            pass
        load_dotenv(BASE_DIR / ".env", override=True)
        api_key = os.getenv("GEMINI_API_KEY")
    if api_key in placeholder:
        console.print("[error]No Gemini API key found.[/error] "
                      "Run [accent]python3 setup_cli.py[/accent] to set one up.")
        raise SystemExit(1)
    model_name = os.getenv("GEMINI_MODEL_QUERY", os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite"))
    return {"client": genai.Client(api_key=api_key), "model_name": model_name}


def tokenize(text: str) -> set[str]:
    text = text.lower()
    # Narrow typo repair for common query vocabulary.
    text = text.replace("braand", "brand")
    return {token for token in re.findall(r"[a-zA-Z0-9]{3,}", text)}


def is_personal_context_query(question: str) -> bool:
    words = set(re.findall(r"[a-zA-Z0-9]{2,}", question.lower()))
    words = {"brand" if word == "braand" else word for word in words}
    personal_terms = {"my", "me", "mine", "our", "us", "we"}
    artifact_terms = {
        "application",
        "apply",
        "yc",
        "ycombinator",
        "company",
        "startup",
        "draft",
        "pdf",
        "document",
        "file",
    }
    return bool(words & personal_terms) and bool(words & artifact_terms)


def is_local_file_source(path: Path, text: str) -> bool:
    return path.name.startswith("local-") or "channel: Local Files" in text or "Channel: Local Files" in text


def page_title(text: str, path: Path) -> str:
    match = re.search(r"^title:\s*(.+)$", text, re.MULTILINE)
    if match:
        return match.group(1).strip().strip('"')
    heading = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return heading.group(1).strip() if heading else path.stem


def search_pages(question: str, limit: int) -> list[dict]:
    query_terms = tokenize(question)
    pages = []
    pinned_paths: set[Path] = set()
    personal_context = is_personal_context_query(question)

    for local_path in extract_local_file_paths(question):
        source_page = source_page_for_local_path(local_path)
        if source_page:
            pages.append(local_page_dict(local_path, source_page, score=10_000))
            pinned_paths.add(source_page)

    for path in WIKI_DIR.rglob("*.md"):
        if path.name in {"schema.md", "log.md", "index.md"}:
            continue
        if path in pinned_paths:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        terms = tokenize(text)
        overlap = len(query_terms & terms)
        score = overlap
        local_source = is_local_file_source(path, text)
        if overlap == 0 and not (personal_context and local_source):
            continue
        if personal_context and local_source:
            score += 250
        page = {"path": path, "title": page_title(text, path), "score": score, "text": text}
        if local_source:
            page = enrich_local_source_with_raw_text(page)
        pages.append(page)
    return sorted(pages, key=lambda item: item["score"], reverse=True)[:limit]


def build_context(pages: list[dict], max_chars: int) -> str:
    """
    Build context from wiki pages AND their raw transcripts.
    For the top source pages, include the full transcript so Gemini
    can synthesize detailed answers instead of just citing references.
    """
    manifest = _load_manifest()
    chunks = []
    used = 0
    raw_budget_ratio = 0.7

    for page in pages:
        rel = page["path"].relative_to(WIKI_DIR)
        text = page["text"].strip()
        budget = max_chars - used
        if budget <= 0:
            break
        text = text[:budget]
        chunks.append(f"--- PAGE: {rel} | {page['title']} ---\n{text}")
        used += len(text)

    raw_budget = int(max_chars * raw_budget_ratio) - used
    if raw_budget > 0:
        for page in pages:
            if raw_budget <= 0:
                break
            if "sources/" not in str(page["path"]):
                continue
            transcript = _resolve_raw_transcript(page["path"], manifest)
            if not transcript:
                continue
            trimmed = transcript[:raw_budget]
            chunks.append(
                f"--- RAW TRANSCRIPT: {page['title']} ---\n{trimmed}"
            )
            raw_budget -= len(trimmed)

    return "\n\n".join(chunks)


def _build_answer_prompt(question: str, context: str, skill) -> str:
    return f"""You answer questions using an LLM-maintained markdown wiki and raw transcripts.

Active answer skill:
{skill.process}

Hard rules:
- Follow the active skill's process before writing the answer.
- READ the raw transcript content provided and extract specific details, frameworks, numbers, advice, and examples from it. Do NOT just list references for the user to read themselves.
- Synthesize a complete, self-contained answer. The user should NOT need to go read the source pages to get the information — give them the actual content.
- If raw transcripts are provided, mine them for specific tactical details: frameworks, numbers, step-by-step advice, examples, quotes.
- If local extracted file text is present, treat it as accessible evidence. Do not say you cannot access the local filesystem.
- Do not invent metrics, customers, dates, or claims.
- Use only the context below. Cite wiki pages by their PAGE label when making claims.
- If context is insufficient, say exactly what is missing and how to ingest it.

Question:
{question}

Context:
{context}
"""


def _finalize_answer(answer: str) -> str:
    """Tidy wikilinks into readable source mentions; trim."""
    answer = re.sub(r"\[\[([^|]+)\|([^\]]+)\]\]", r"(Source: *\2*)", answer)
    answer = re.sub(r"\[\[([^\]]+)\]\]", r"(Source: *\1*)", answer)
    return answer.strip()


def gemini_answer_stream(gemini, question: str, context: str, skill):
    """Return a streaming iterator of answer chunks (each has .text)."""
    prompt = _build_answer_prompt(question, context, skill)
    return gemini["client"].models.generate_content_stream(
        model=gemini["model_name"],
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.2),
    )


def ask_gemini(gemini, question: str, context: str, pages: list[dict]) -> str:
    """Non-streaming answer (kept for callers that don't render live)."""
    skill = route_skill(question, pages)
    response = gemini["client"].models.generate_content(
        model=gemini["model_name"],
        contents=_build_answer_prompt(question, context, skill),
        config=types.GenerateContentConfig(temperature=0.2),
    )
    return _finalize_answer(response.text.strip())


# --- shared UX helpers (consistent across interactive + one-shot) ----------
def fmt_path(p) -> str:
    """One consistent root for every artifact path the user sees (wiki/...)."""
    try:
        return str(Path(p).resolve().relative_to(BASE_DIR))
    except (ValueError, OSError):
        return str(p)


def footer_hint(n_pages: int) -> str:
    return f"  [dim]Grounded in {n_pages} page(s) · [accent]/pages[/accent] to inspect · [accent]/save[/accent] to keep[/dim]"


def whats_new_line() -> str | None:
    """Ambient '+N sources since your last visit' from a tiny cached snapshot."""
    cache = BASE_DIR / ".last_seen.json"
    try:
        current = len(list((WIKI_DIR / "sources").glob("*.md")))
        previous = json.loads(cache.read_text()).get("sources") if cache.exists() else None
        cache.write_text(json.dumps({"sources": current}))
        if previous is not None and current > previous:
            return f"+{current - previous} sources since your last visit"
    except Exception:  # pragma: no cover — ambient nicety, never break startup
        return None
    return None


def make_prompt_session():
    """A prompt_toolkit session (slash-command autocomplete, history, ghost
    suggestions) when on a real TTY; None otherwise so piping stays clean."""
    if not sys.stdin.isatty():
        return None
    try:
        from prompt_toolkit import PromptSession
        from prompt_toolkit.history import FileHistory
        from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
        from prompt_toolkit.completion import NestedCompleter
    except Exception:
        return None
    completer = NestedCompleter.from_nested_dict({
        "/idea": None, "/save": None, "/pages": None, "/skills": None,
        "/stats": None, "/sync": {"now": None, "force": None},
        "/ingest": {"--gemini": None, "--force": None},
        "/help": None, "/quit": None, "/exit": None,
    })
    try:
        return PromptSession(
            history=FileHistory(str(BASE_DIR / ".qa_history")),
            auto_suggest=AutoSuggestFromHistory(),
            completer=completer,
            complete_while_typing=True,
        )
    except Exception:
        return None


def _bottom_toolbar():
    """Passive background-sync indicator shown under the input line."""
    if background is None:
        return ""
    try:
        return f" {background.short_status()} "
    except Exception:
        return ""


def read_question(session) -> str:
    """Read the next question via prompt_toolkit (TTY) or plain input (piped)."""
    if session is not None:
        from prompt_toolkit.formatted_text import HTML
        return session.prompt(
            HTML("<ansigreen><b>You:</b></ansigreen> "),
            bottom_toolbar=_bottom_toolbar,
        ).strip()
    return console.input("[bold green]You:[/bold green] ").strip()


IDEAS_DIR = WIKI_DIR / "ideas"


def list_existing_ideas() -> list[tuple[str, Path]]:
    """Return list of (title, path) for existing ideas."""
    IDEAS_DIR.mkdir(parents=True, exist_ok=True)
    ideas = []
    for p in sorted(IDEAS_DIR.glob("*.md")):
        text = p.read_text(encoding="utf-8", errors="replace")
        match = re.search(r"^title:\s*(.+)$", text, re.MULTILINE)
        title = match.group(1).strip() if match else p.stem
        ideas.append((title, p))
    return ideas


def find_idea_by_name(name: str) -> Path | None:
    """Fuzzy-match an idea by name."""
    name_lower = name.lower().strip()
    for title, path in list_existing_ideas():
        if name_lower in title.lower() or name_lower in path.stem.lower():
            return path
    return None


def append_to_idea(filepath: Path, new_content: str) -> None:
    """Append content to an existing idea and update its timestamp."""
    content = filepath.read_text(encoding="utf-8")
    content = re.sub(r"updated: \d{4}-\d{2}-\d{2}", f"updated: {today()}", content)
    content = content.rstrip() + f"\n\n---\n*Added {today()}:*\n\n{new_content}\n"
    filepath.write_text(content, encoding="utf-8")


def capture_multiline(console_obj, prompt_msg: str) -> str:
    """Read multiline input until double-Enter."""
    console_obj.print(f"\n  [accent]{prompt_msg} (press Enter twice to finish)[/accent]")
    lines = []
    while True:
        try:
            line = console_obj.input("  [dim]>[/dim] ").rstrip()
        except (EOFError, KeyboardInterrupt):
            break
        if line == "" and lines and lines[-1] == "":
            lines.pop()
            break
        lines.append(line)
    return "\n".join(lines).strip()


def capture_idea(console_obj, gemini, update_target: str = "") -> Path | None:
    """Create a new idea or update an existing one.
    
    If update_target is given (e.g. 'my-startup'), appends to that idea.
    If update_target is empty, prompts for new or update.
    """
    existing = list_existing_ideas()

    # If a target is specified, find and append to it
    if update_target:
        match = find_idea_by_name(update_target)
        if not match:
            console_obj.print(f"  [warning]No idea matching '{update_target}' found.[/warning]")
            if existing:
                console_obj.print(f"  [dim]Existing ideas:[/dim]")
                for title, _ in existing:
                    console_obj.print(f"    [dim]•[/dim] {title}")
            return None
        title = re.search(r"^title:\s*(.+)$", match.read_text(), re.MULTILINE).group(1).strip()
        text = capture_multiline(console_obj, f"Add to '{title}'")
        if not text:
            return None
        append_to_idea(match, text)
        append_log("idea-update", title, f"- Page: `{match.relative_to(WIKI_DIR.parent)}`")
        return match

    # If ideas exist, ask whether to create or update
    if existing:
        console_obj.print(f"\n  [accent]Your ideas:[/accent]")
        for i, (title, _) in enumerate(existing, 1):
            console_obj.print(f"    [dim]{i}.[/dim] {title}")
        console_obj.print(f"    [dim]{len(existing)+1}.[/dim] [accent]+ New idea[/accent]")
        console_obj.print()
        choice = console_obj.input("  [accent]Pick a number (or Enter for new):[/accent] ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(existing):
            idx = int(choice) - 1
            title, path = existing[idx]
            text = capture_multiline(console_obj, f"Add to '{title}'")
            if not text:
                return None
            append_to_idea(path, text)
            append_log("idea-update", title, f"- Page: `{path.relative_to(WIKI_DIR.parent)}`")
            return path

    # Create a new idea
    text = capture_multiline(console_obj, "What's the idea?")
    if not text:
        return None

    console_obj.print()
    title_prompt = console_obj.input("  [accent]Short title (or Enter to auto-generate):[/accent] ").strip()

    if not title_prompt:
        try:
            resp = gemini["client"].models.generate_content(
                model=gemini["model_name"],
                contents=f"Give a concise 3-8 word title for this idea. Return ONLY the title, nothing else.\n\n{text}",
                config=types.GenerateContentConfig(temperature=0.3),
            )
            title_prompt = resp.text.strip().strip('"').strip("'")
        except Exception:
            title_prompt = f"Idea {datetime.now().strftime('%Y%m%d-%H%M')}"

    IDEAS_DIR.mkdir(parents=True, exist_ok=True)
    stem = slugify(title_prompt, fallback="idea")
    idea_id = f"idea-{stem}"
    filepath = IDEAS_DIR / f"{idea_id}.md"

    content = "\n".join([
        "---",
        "type: idea",
        f"title: {title_prompt}",
        f"created: {today()}",
        f"updated: {today()}",
        "tags:",
        "  - personal",
        "  - idea",
        "---",
        "",
        f"# {title_prompt}",
        "",
        text,
        "",
    ])
    filepath.write_text(content, encoding="utf-8")

    rebuild_index()
    append_log("idea", title_prompt, f"- Page: `{filepath.relative_to(WIKI_DIR.parent)}`")
    return filepath


def save_synthesis(question: str, answer: str, pages: list[dict]) -> Path:
    SYNTHESIS_DIR.mkdir(parents=True, exist_ok=True)
    stem = slugify(question, fallback="query")
    path = SYNTHESIS_DIR / f"{today()}-{stem}.md"
    source_links = [f"  - {page['path'].relative_to(WIKI_DIR).with_suffix('')}" for page in pages]
    content = "\n".join([
        "---", "type: synthesis", f"title: Query - {question}",
        f"created: {today()}", f"updated: {today()}", "sources:",
        *source_links, "tags:", "  - query", "---", "",
        f"# {question}", "", answer, "",
    ])
    path.write_text(content, encoding="utf-8")
    rebuild_index()
    append_log("query", question, f"- Saved: `{path.relative_to(WIKI_DIR.parent)}`")
    return path


def print_header():
    header = Text()
    header.append("╔════════════════════════════════════════════════════╗\n", style="accent")
    header.append("║", style="accent")
    header.append("       Wiki Q&A Harness ", style="bold white")
    header.append("— evidence-first memory     ", style="dim")
    header.append("║\n", style="accent")
    header.append("╚════════════════════════════════════════════════════╝", style="accent")
    console.print(header)


def print_commands():
    console.print("  [dim]/idea[/dim]   — jot down a new idea or update an existing one")
    console.print("  [dim]/idea <name>[/dim] — add to an existing idea by name")
    console.print("  [dim]/save[/dim]   — save last answer as synthesis page")
    console.print("  [dim]/pages[/dim]  — show pages referenced in last answer")
    console.print("  [dim]/skills[/dim] — show answer skills/processes")
    console.print("  [dim]/stats[/dim]  — show wiki stats")
    console.print("  [dim]/sync[/dim]   — background-sync status ([dim]/sync now[/dim] to refresh)")
    console.print("  [dim]/ingest <path>[/dim] — ingest a local PDF/TXT/MD/HTML file")
    console.print("  [dim]/ingest --gemini <pdf>[/dim] — force Gemini PDF extraction")
    console.print("  [dim]/quit[/dim]   — exit\n")


def print_operating_loop():
    console.print("  [accent]Loop:[/accent] investigate → retrieve → answer → verify")
    console.print("  [dim]Rule: if the wiki has no evidence, the answer should say what is missing.[/dim]\n")


def interactive_mode(top_k: int = 8, max_context: int = 80_000):
    if not INDEX_PATH.exists():
        console.print("[error]wiki/index.md not found. Run ingest.py first.[/error]")
        return

    gemini = configure_gemini()

    console.print()
    print_header()
    console.print(f"  [dim]Model: {gemini['model_name']}[/dim]")
    print_operating_loop()
    console.print(f"  [dim]Commands:[/dim]")
    print_commands()

    # Kick off a detached background sync of new videos/essays (non-blocking).
    if background is not None:
        try:
            console.print(f"  [dim]{background.maybe_launch_background_sync()}[/dim]")
        except Exception:  # pragma: no cover — never let sync break the REPL
            pass

    new_line = whats_new_line()
    if new_line:
        console.print(f"  [success]{new_line}[/success]")

    session = make_prompt_session()
    if session is not None:
        console.print("  [dim]Tab completes commands · ↑ recalls history[/dim]")

    pet.greet()

    last_question = None
    last_pages = None
    last_answer = None

    while True:
        try:
            console.print()
            question = read_question(session)
        except (EOFError, KeyboardInterrupt):
            console.print()
            pet.farewell()
            break

        if not question:
            continue

        if question.lower() in ("/quit", "/exit", "/q"):
            show_pet("happy", "See you next time!")
            break

        if question.lower().startswith("/idea"):
            args = question[5:].strip()
            if args:
                # /idea my-startup → update existing idea named "my-startup"
                path = capture_idea(console, gemini, update_target=args)
            else:
                # /idea → interactive create or update
                path = capture_idea(console, gemini)
            if path:
                console.print(f"  [success]Idea saved → {fmt_path(path)}[/success]")
                show_pet("happy", "Idea captured! It's now searchable in the wiki.")
            else:
                console.print("  [warning]No idea captured.[/warning]")
            continue

        # Detect natural language idea updates: "add X to my <name> idea"
        idea_update_match = re.match(
            r"(?:add|append|update|save)\s+(.+?)\s+(?:to|in|into)\s+(?:my\s+)?(.+?)\s*(?:idea|note)s?\s*$",
            question, re.IGNORECASE,
        )
        if idea_update_match:
            content_to_add = idea_update_match.group(1).strip()
            idea_name = idea_update_match.group(2).strip()
            target = find_idea_by_name(idea_name)
            if target:
                append_to_idea(target, content_to_add)
                title = re.search(r"^title:\s*(.+)$", target.read_text(), re.MULTILINE).group(1).strip()
                console.print(f"  [success]Added to '{title}' → {fmt_path(target)}[/success]")
                show_pet("happy", f"Updated '{title}' with your note!")
                append_log("idea-update", title, f"- Page: `{target.relative_to(WIKI_DIR.parent)}`")
                continue

        if question.lower() == "/save":
            if last_question and last_answer and last_pages:
                path = save_synthesis(last_question, last_answer, last_pages)
                console.print(f"  [success]Saved → {fmt_path(path)}[/success]")
                show_pet("happy", "Saved for later!")
            else:
                console.print("  [warning]Nothing to save yet.[/warning]")
            continue

        if question.lower() == "/pages":
            if last_pages:
                console.print(f"\n  [info]Pages referenced ({len(last_pages)}):[/info]")
                for p in last_pages:
                    console.print(f"    [accent]•[/accent] {fmt_path(p['path'])} [dim]({p['title']})[/dim]")
            else:
                console.print("  [warning]No pages yet. Ask a question first.[/warning]")
            continue

        if question.lower() in ("/help", "/?"):
            print_commands()
            continue

        if question.lower() == "/skills":
            console.print(Panel(Markdown(render_skills_help()), title="[bold cyan]Answer Skills[/bold cyan]", border_style="cyan"))
            continue

        if question.lower().startswith("/sync"):
            if background is None:
                console.print("  [warning]Background sync module unavailable.[/warning]")
                continue
            arg = question[5:].strip().lower()
            if arg in ("now", "force"):
                console.print(f"  [info]{background.force_sync()}[/info]")
            else:
                console.print(Panel(background.status_text(), title="[bold cyan]Auto-sync[/bold cyan]", border_style="cyan"))
            continue

        if question.lower().startswith("/ingest"):
            try:
                parts = shlex.split(question)
            except ValueError as exc:
                console.print(f"  [error]Could not parse command: {exc}[/error]")
                console.print('  [dim]Example: /ingest "~/Downloads/document.pdf"[/dim]')
                continue

            force = "--force" in parts
            use_gemini = "--gemini" in parts or "--extractor=gemini" in parts
            control_flags = {"--force", "--gemini", "--extractor=gemini", "--extractor", "gemini", "local"}
            extractor = "gemini" if use_gemini else "local"
            paths = [Path(part).expanduser() for part in parts[1:] if part not in control_flags]
            if not paths:
                console.print('  [warning]Usage: /ingest "/path/to/file.pdf" [--force] [--gemini][/warning]')
                continue

            show_pet("thinking", f"Ingesting {len(paths)} local file(s) with {extractor} extraction...")
            results = ingest_files(paths, force=force, extractor=extractor)
            verified = [result for result in results if result.get("verified")]
            failed = [result for result in results if not result.get("verified")]

            console.print(f"\n  [success]Verified ingests: {len(verified)}[/success]")
            if failed:
                console.print(f"  [error]Failed ingests: {len(failed)}[/error]")
                for result in failed:
                    console.print(f"    [error]• {result.get('path')}: {result.get('error', 'unknown error')}[/error]")
                show_pet("sad", "Some files did not ingest. I reported the exact failures.")
            else:
                for result in verified:
                    console.print(f"    [dim]• {result.get('transcript')} ({result.get('extractor', extractor)})[/dim]")
                show_pet("happy", "Memory updated and verified. Ask me about it now!")
            continue

        if question.lower() == "/stats":
            sources = list((WIKI_DIR / "sources").glob("*.md"))
            entities = list((WIKI_DIR / "entities").glob("*.md"))
            topics = list((WIKI_DIR / "topics").glob("*.md"))
            console.print(f"\n  [info]Wiki Stats:[/info]")
            console.print(f"    Sources:  {len(sources)}")
            console.print(f"    Entities: {len(entities)}")
            console.print(f"    Topics:   {len(topics)}")
            show_pet("idle", f"That's {len(sources) + len(entities) + len(topics)} pages of knowledge!")
            continue

        # Auto-ingest any local file paths mentioned in the question.
        auto_ingests = ensure_question_files_ingested(question)
        if auto_ingests:
            verified = [result for result in auto_ingests if result.get("verified")]
            failed = [result for result in auto_ingests if not result.get("verified")]
            if verified:
                console.print(f"  [success]Auto-ingested local file references: {len(verified)}[/success]")
            if failed:
                for result in failed:
                    console.print(f"  [error]Auto-ingest failed: {result.get('path')}: {result.get('error')}[/error]")

        # Retrieve while Kumo looks around and mutters quirky status.
        def _retrieve():
            found = search_pages(question, top_k)
            if not found:
                return None
            picked = route_skill(question, found)
            ctx = build_context(found, max_context)
            return found, picked, ctx

        try:
            retrieved = pet.think(_retrieve)
        except KeyboardInterrupt:
            console.print("  [dim]Cancelled.[/dim]")
            continue
        except Exception as exc:  # noqa: BLE001 — surface, don't crash
            console.print(f"  [error]Search failed:[/error] {str(exc)[:160]}")
            continue

        if not retrieved:
            pet.empty(remedy="Try broader terms, or [accent]/ingest <path>[/accent] to add a source.")
            continue

        pages, skill, context = retrieved
        console.print(f"  [dim]Skill: [accent]{skill.name}[/accent] · {len(pages)} pages of evidence[/dim]")

        # Stream the answer in live (Kumo "talks" as it writes).
        try:
            stream = gemini_answer_stream(gemini, question, context, skill)
            answer = pet.stream_answer(stream, transform=_finalize_answer)
        except KeyboardInterrupt:
            console.print("  [dim]Cancelled.[/dim]")
            continue
        except Exception as exc:  # noqa: BLE001 — never dump a traceback at the user
            console.print(f"  [error]Gemini error:[/error] {str(exc)[:160]}")
            console.print("  [dim]Check GEMINI_API_KEY or try again.[/dim]")
            continue

        console.print()
        console.print(Panel(
            Markdown(answer),
            title="[bold cyan]Answer[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        ))
        console.print(footer_hint(len(pages)))
        pet.celebrate()

        last_question = question
        last_pages = pages
        last_answer = answer


def oneshot_mode(question: str, gemini, top_k: int, max_context: int, save: bool):
    auto_ingests = ensure_question_files_ingested(question)
    if auto_ingests:
        verified = [result for result in auto_ingests if result.get("verified")]
        failed = [result for result in auto_ingests if not result.get("verified")]
        if verified:
            console.print(f"  [success]Auto-ingested local file references: {len(verified)}[/success]")
        if failed:
            for result in failed:
                console.print(f"  [error]Auto-ingest failed: {result.get('path')}: {result.get('error')}[/error]")

    pages = search_pages(question, top_k)
    if not pages:
        console.print("[warning]No relevant wiki pages found.[/warning] [dim]Try broader terms, or /ingest a source.[/dim]")
        return

    skill = route_skill(question, pages)
    console.print(f"  [dim]Skill: [accent]{skill.name}[/accent] · {len(pages)} pages of evidence[/dim]")
    context = build_context(pages, max_context)
    # Streams live on a TTY; collects silently when piped/redirected.
    try:
        stream = gemini_answer_stream(gemini, question, context, skill)
        answer = pet.stream_answer(stream, transform=_finalize_answer)
    except KeyboardInterrupt:
        console.print("  [dim]Cancelled.[/dim]")
        return
    except Exception as exc:  # noqa: BLE001 — never dump a traceback at the user
        console.print(f"  [error]Gemini error:[/error] {str(exc)[:160]}")
        return

    console.print(Panel(
        Markdown(answer),
        title="[bold cyan]Answer[/bold cyan]",
        border_style="cyan",
        padding=(1, 2),
    ))
    console.print(footer_hint(len(pages)))

    if save:
        path = save_synthesis(question, answer, pages)
        console.print(f"  [success]Saved → {fmt_path(path)}[/success]")


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask questions against the LLM wiki.")
    parser.add_argument("question", nargs="?", help="Question (omit for interactive mode).")
    parser.add_argument("--top-k", type=int, default=8, help="Number of wiki pages to include.")
    parser.add_argument("--max-context-chars", type=int, default=80_000, help="Maximum wiki context.")
    parser.add_argument("--save", action="store_true", help="Save the answer as synthesis.")
    args = parser.parse_args()

    if not INDEX_PATH.exists():
        console.print("[error]wiki/index.md not found. Run ingest.py first.[/error]")
        return

    if args.question:
        gemini = configure_gemini()
        oneshot_mode(args.question, gemini, args.top_k, args.max_context_chars, args.save)
    else:
        interactive_mode(args.top_k, args.max_context_chars)


if __name__ == "__main__":
    main()
