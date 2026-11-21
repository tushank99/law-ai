"""Provider-agnostic LLM client. Swap models with env vars only:

  LLM_PROVIDER  = groq | gemini | anthropic | openai   (primary)
  LLM_MODEL     = model override for the primary provider
  <NAME>_API_KEY = key per provider (GROQ_API_KEY, GEMINI_API_KEY, ANTHROPIC_API_KEY, OPENAI_API_KEY)
  LLM_BASE_URL  = custom OpenAI-compatible endpoint (used with LLM_PROVIDER=openai)

If the primary provider fails, any other provider with a key is tried automatically.
"""
import os
import time
import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

PROVIDERS = {
    "groq": ("https://api.groq.com/openai/v1", "openai/gpt-oss-120b"),
    "gemini": ("https://generativelanguage.googleapis.com/v1beta/openai", "gemini-2.5-flash"),
    "openai": ("https://api.openai.com/v1", "gpt-4o-mini"),
    "anthropic": ("https://api.anthropic.com/v1", "claude-haiku-5-5"),
}


def _key(p):
    return os.getenv(f"{p.upper()}_API_KEY", "")


def _chain():
    primary = os.getenv("LLM_PROVIDER", "").lower()
    order = ([primary] if primary in PROVIDERS else []) + [p for p in PROVIDERS if p != primary]
    chain = [p for p in order if _key(p)]
    if not chain:
        raise RuntimeError("No API key found. Set GROQ_API_KEY or GEMINI_API_KEY (see .env.example).")
    return chain


def _model(p):
    if p == os.getenv("LLM_PROVIDER", "").lower() and os.getenv("LLM_MODEL"):
        return os.getenv("LLM_MODEL")
    return PROVIDERS[p][1]


def provider_info():
    try:
        p = _chain()[0]
        return f"{p} / {_model(p)}"
    except RuntimeError as e:
        return str(e)


def _call(p, system, messages, temperature):
    if p == "anthropic":
        r = requests.post(
            f"{PROVIDERS[p][0]}/messages",
            headers={"x-api-key": _key(p), "anthropic-version": "2023-06-01"},
            json={"model": _model(p), "max_tokens": 4000, "system": system,
                  "messages": messages, "temperature": temperature},
            timeout=120,
        )
        r.raise_for_status()
        return "".join(b.get("text", "") for b in r.json()["content"])

    base = os.getenv("LLM_BASE_URL", PROVIDERS[p][0]) if p == "openai" else PROVIDERS[p][0]
    r = requests.post(
        f"{base}/chat/completions",
        headers={"Authorization": f"Bearer {_key(p)}"},
        json={"model": _model(p), "temperature": temperature,
              "messages": [{"role": "system", "content": system}] + messages},
        timeout=120,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"] or ""


def chat(system: str, messages: list[dict], temperature: float = 0.2) -> str:
    """messages: [{"role": "user"|"assistant", "content": str}]"""
    errors = []
    for p in _chain():
        for attempt in range(3):
            try:
                return _call(p, system, messages, temperature)
            except requests.HTTPError as e:
                if e.response is not None and e.response.status_code == 429 and attempt < 2:
                    wait = float(e.response.headers.get("retry-after", 10))
                    time.sleep(min(wait, 30))
                    continue
                errors.append(f"{p}: {e}")
                break
            except Exception as e:
                errors.append(f"{p}: {e}")
                break
    raise RuntimeError("All providers failed -> " + " | ".join(errors))


def transcribe(audio_bytes: bytes) -> str:
    """Voice to text via Groq Whisper (free tier)."""
    if not _key("groq"):
        raise RuntimeError("Voice input needs GROQ_API_KEY.")
    r = requests.post(
        "https://api.groq.com/openai/v1/audio/transcriptions",
        headers={"Authorization": f"Bearer {_key('groq')}"},
        files={"file": ("audio.wav", audio_bytes, "audio/wav")},
        data={"model": "whisper-large-v3"},
        timeout=120,
    )
    r.raise_for_status()
    return r.json().get("text", "").strip()
