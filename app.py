import os
import streamlit as st

st.set_page_config(page_title="Nyaya Mitra - AI Legal Help", page_icon="⚖️", layout="centered")

# Streamlit Cloud secrets -> env vars (local runs use .env instead)
try:
    for k, v in st.secrets.items():
        if isinstance(v, str):
            os.environ.setdefault(k, v)
except Exception:
    pass

from lawyer import respond  # noqa: E402
from llm import provider_info, transcribe  # noqa: E402

if "messages" not in st.session_state:
    st.session_state.messages = []
if "practice" not in st.session_state:
    st.session_state.practice = []

with st.sidebar:
    st.title("⚖️ Nyaya Mitra")
    st.caption(f"Model: `{provider_info()}`")
    mode = st.radio("Mode", ["Get help", "Practice arguing"])
    other_side = st.text_input("Other side (for practice)", "the landlord") if mode == "Practice arguing" else ""
    st.divider()
    st.markdown("**Covers:** security deposit, refunds/consumer, unpaid salary, cheque bounce, "
                "understanding a notice.")
    st.markdown("**Free legal aid:** NALSA 15100 · **Emergency:** 112 · **Consumer:** 1915")
    st.caption("General information only, not legal advice. Verify with a lawyer before acting.")
    if st.button("🗑️ New conversation"):
        st.session_state.messages, st.session_state.practice, st.session_state.doc = [], [], None
        st.rerun()

st.title("Talk to your AI legal helper")
st.caption("Tell your problem in any language - English, Hindi, Hinglish, Marathi, Tamil...")

msgs_key = "messages" if mode == "Get help" else "practice"
history = st.session_state[msgs_key]

for m in history:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Voice input (needs GROQ_API_KEY for Whisper transcription)
audio = st.audio_input("🎤 Or speak your problem")
voice_text = None
if audio is not None and st.session_state.get("last_audio") != audio.getvalue():
    st.session_state.last_audio = audio.getvalue()
    try:
        voice_text = transcribe(audio.getvalue())
    except Exception as e:
        st.error(f"Transcription failed: {e}")

prompt = st.chat_input("Describe your problem...") or voice_text

if prompt:
    history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                if mode == "Get help":
                    out = respond("advisor", history)
                else:
                    out = respond("roleplay", st.session_state.messages + history, other_side=other_side)
                st.markdown(out["reply"])
                history.append({"role": "assistant", "content": out["reply"]})
            except Exception as e:
                st.error(f"Model call failed: {e}")

# Action buttons (only in help mode, once there's a conversation)
if mode == "Get help" and st.session_state.messages:
    st.divider()
    c1, c2, c3 = st.columns(3)
    action = None
    if c1.button("📋 Case summary"):
        action = ("summary", {})
    if c2.button("📝 Draft legal notice"):
        action = ("draft", {"doc_type": "legal notice"})
    if c3.button("📮 Draft complaint"):
        action = ("draft", {"doc_type": "complaint letter to the relevant authority/forum"})
    if action:
        with st.spinner("Preparing..."):
            try:
                out = respond(action[0], st.session_state.messages, **action[1])
                st.session_state.doc = (action[0], out["reply"])
            except Exception as e:
                st.error(f"Model call failed: {e}")
    if st.session_state.get("doc"):
        name, text = st.session_state.doc
        st.markdown(text)
        st.download_button("⬇️ Download", text, file_name=f"{name}.md")
