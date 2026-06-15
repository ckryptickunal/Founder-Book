"""Task-specific answer skills for the wiki Q&A agent."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class QuerySkill:
    name: str
    description: str
    process: str


SKILLS: dict[str, QuerySkill] = {
    "yc_application_review": QuerySkill(
        name="yc_application_review",
        description="Review or rewrite YC applications using the user's application as primary evidence.",
        process="""
Skill: YC Application Review
Process:
1. First identify the user's own application/company details from local-file evidence.
2. Treat local application evidence as primary. Generic YC advice is secondary.
3. Extract concrete facts: product, users, traction, revenue, founders, market, why now, competitors.
4. Diagnose against YC criteria: clarity, market pull, founder-market fit, speed, insight, traction, ambition.
5. Produce specific edits or a draft using the user's actual facts. Do not invent metrics.
6. If a required fact is absent, mark it as MISSING instead of guessing.
7. Include citations to the source pages used.
""",
    ),
    "local_document_analysis": QuerySkill(
        name="local_document_analysis",
        description="Analyze an explicitly referenced local document or PDF.",
        process="""
Skill: Local Document Analysis
Process:
1. Use the local document's extracted text as the primary source.
2. If the local document text is present, never say you cannot access the local filesystem.
3. Summarize or critique only what appears in the extracted file text.
4. Separate observed facts from recommendations.
5. If extraction looks incomplete, say which sections are missing and suggest re-ingesting with --gemini.
6. Cite the local source page.
""",
    ),
    "comparison": QuerySkill(
        name="comparison",
        description="Compare people, companies, essays, or ideas across sources.",
        process="""
Skill: Comparison
Process:
1. Identify the items being compared.
2. Find evidence for each side before drawing conclusions.
3. Use a compact comparison structure: similarities, differences, tensions, takeaway.
4. Do not overfit one source to the other. If evidence is missing for one side, say so.
5. Cite sources for each substantive claim.
""",
    ),
    "source_summary": QuerySkill(
        name="source_summary",
        description="Summarize sources, essays, transcripts, or documents.",
        process="""
Skill: Source Summary
Process:
1. Identify the source(s) being summarized.
2. Summarize the main thesis, key ideas, examples, and useful quotes.
3. Preserve important numbers, names, and dates.
4. Avoid adding advice unless requested.
5. Cite the source page labels.
""",
    ),
    "default_qa": QuerySkill(
        name="default_qa",
        description="General evidence-grounded wiki question answering.",
        process="""
Skill: Evidence-Grounded Q&A
Process:
1. Read ALL provided context including raw transcripts thoroughly before answering.
2. Extract specific details, frameworks, numbers, step-by-step advice, and examples from the raw transcript content.
3. Synthesize a complete, self-contained answer. The user should NOT need to read any referenced pages — give them the actual information directly.
4. Distinguish facts, interpretations, and recommendations.
5. If evidence is insufficient, say what is missing and how to ingest it.
6. Cite wiki page labels for claims, but always include the actual content alongside citations.
""",
    ),
}


def route_skill(question: str, pages: list[dict]) -> QuerySkill:
    q = question.lower()
    page_titles = " ".join(page.get("title", "").lower() for page in pages[:3])
    has_local = any("Extracted Local File Text" in page.get("text", "") for page in pages)

    if ("yc" in q or "y combinator" in q or "ycombinator" in q) and any(
        term in q for term in ["application", "apply", "rewrite", "perfect", "review", "selection"]
    ):
        return SKILLS["yc_application_review"]

    if has_local or re.search(r"(?:/Users|~/|\.pdf|\.txt|\.md|\.html)", question):
        return SKILLS["local_document_analysis"]

    if any(term in q for term in ["compare", "versus", " vs ", "difference", "similarities"]) or " vs " in page_titles:
        return SKILLS["comparison"]

    if any(term in q for term in ["summarize", "summary", "what does this say", "key ideas"]):
        return SKILLS["source_summary"]

    return SKILLS["default_qa"]


def render_skills_help() -> str:
    lines = ["Available answer skills:"]
    for skill in SKILLS.values():
        lines.append(f"- {skill.name}: {skill.description}")
    return "\n".join(lines)
