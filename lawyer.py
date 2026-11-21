"""Core logic: prompts, grounding, and the citation guard. UI-independent."""
import re
from llm import chat
from knowledge import classify, context_for, allowed_citations

BASE_RULES = """You are "Nyaya Mitra", a friendly legal help assistant for ordinary people in India.
You are NOT a lawyer and you say so when relevant.

HARD RULES (never break):
1. Cite ONLY laws/sections listed under VERIFIED LAWS below. Never invent Acts, sections, case
   names, judgments, fees or deadlines. If unsure, say "I'm not sure - please confirm with a lawyer
   or free legal aid (NALSA 15100)."
2. Reply in the SAME language and script the user writes in (Hindi, Hinglish, Marathi, Tamil, etc.).
3. Use plain, simple words. Short paragraphs and bullet points. No legal jargon without explaining it.
4. Say clearly when they need a real lawyer (see GET A LAWYER WHEN). Mention free legal aid.
5. If it's an emergency (violence, threat to life, arrest), tell them to call 112 first.
6. This is general information, not legal advice.

VERIFIED KNOWLEDGE:
{context}
"""

MODES = {
    "advisor": """TASK: Help the user understand their problem and act.
- If key facts are missing (dates, amounts, who, what proof they have), ask at most 3 short questions.
- Once you have enough, answer with these headings:
  **What happened** (short timeline) | **Your proof** (have / should collect) |
  **Where you stand** (plain language, cite verified laws) | **Your options** (step by step) |
  **Do you need a lawyer?**
- End by offering to draft a legal notice / complaint.""",

    "summary": """TASK: From the conversation, output a structured CASE FILE in markdown:
## Parties | ## Timeline (date - event; write "date unknown" if not given) |
## Amount / relief claimed | ## Evidence available | ## Evidence missing |
## Relevant laws (verified only) | ## Open questions
Do NOT invent any facts. Mark anything assumed as [ASSUMED].""",

    "draft": """TASK: Draft a {doc_type} in formal English based ONLY on facts in the conversation.
- Use placeholders like [YOUR FULL ADDRESS], [DATE] for anything not provided. Never invent facts.
- Structure for a legal notice: sender/recipient, subject, numbered facts, legal basis (verified
  laws only), clear demand with deadline (e.g. 15 days), consequence if ignored, signature block.
- After the draft, add a short note (in the user's language) on how to send it (Registered Post
  A.D./Speed Post + email, keep copies and receipts) and that a lawyer can review it.""",

    "roleplay": """TASK: ROLE-PLAY PRACTICE. You play the OTHER SIDE ({other_side}) in the user's dispute,
so the user can practise arguing. Be realistic and a bit stubborn: use common excuses and pressure
tactics this kind of person uses, but stay respectful. Keep each turn to 2-4 sentences.
After each of your turns add one line in italics starting with "*Coach:*" giving the user one tip
on how to respond better (cite verified laws only). If the user types "end practice", give a short
feedback summary.""",
}


def build_system(mode: str, history_text: str, **kw) -> tuple[str, list[str]]:
    cats = classify(history_text) or []
    system = BASE_RULES.format(context=context_for(cats)) + "\n" + MODES[mode].format(**kw)
    return system, cats


# ---------- Citation guard (anti-hallucination, deterministic) ----------
_ACT_RE = re.compile(r"((?:[A-Z][a-zA-Z()&]*\s?){1,8}(?:Act|Code|Rules)),?\s*(\d{4})")
_SEC_RE = re.compile(r"\b(?:Section|Sec\.?|धारा|कलम)\s*(\d+[A-Z]?(?:\(\d+\))?)", re.I)


def check_citations(text: str) -> list[str]:
    """Return citations in `text` that are NOT in the verified knowledge base."""
    allowed = allowed_citations()
    blob = " ".join(allowed)
    unknown = []
    for name, year in _ACT_RE.findall(text):
        name = name.strip()
        short = name.split()[-1]  # 'Act' / 'Code' / 'Rules'
        if not any(year in a and name.split()[0] in a and short in a for a in allowed):
            unknown.append(f"{name}, {year}")
    for sec in _SEC_RE.findall(text):
        if f"Section {sec}" not in blob:
            unknown.append(f"Section {sec}")
    return sorted(set(unknown))


def respond(mode: str, messages: list[dict], **kw) -> dict:
    history_text = " ".join(m["content"] for m in messages if m["role"] == "user")
    system, cats = build_system(mode, history_text, **kw)
    if mode in ("summary", "draft"):
        transcript = "\n".join(f"{m['role'].upper()}: {m['content']}" for m in messages)
        msgs = [{"role": "user", "content": f"CONVERSATION SO FAR:\n{transcript}\n\nDo the TASK now."}]
    else:
        msgs = messages
    reply = chat(system, msgs)
    unknown = check_citations(reply)
    if unknown:
        reply += ("\n\n> ⚠️ **Unverified reference check:** this answer mentions "
                  + ", ".join(unknown)
                  + " which is not in my verified legal database. Please confirm it with a lawyer "
                    "before relying on it.")
    return {"reply": reply, "categories": cats, "unverified": unknown}
