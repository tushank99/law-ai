# Nyaya Mitra: AI legal helper for everyday problems in India

Chat by text or voice, in any language, about a **security deposit, a consumer refund, unpaid salary,
a bounced cheque, or a legal notice you received**. It builds your case and explains where you stand.
It can draft a legal notice or complaint, and you can practise arguing against the other side.

## Run locally
```bash
pip install -r requirements.txt
cp .env.example .env      # add GROQ_API_KEY and/or GEMINI_API_KEY
streamlit run app.py
```

## Deploy (Streamlit Community Cloud)
1. Push this repo to GitHub. `.env` is gitignored, so the keys stay out of the repo.
2. On share.streamlit.io, create a new app with `app.py` as the main file.
3. In **Settings → Secrets**, paste:
   ```toml
   LLM_PROVIDER = "groq"
   GROQ_API_KEY = "..."
   GEMINI_API_KEY = "..."
   ```

## Swap the model
Change environment variables only: set `LLM_PROVIDER` to groq, gemini, anthropic or openai (for any
OpenAI-compatible endpoint, also set `LLM_BASE_URL`), and optionally `LLM_MODEL`. If the primary provider
fails, the app tries any other provider that has a key.

## How it avoids made-up law
1. **Verified knowledge base** ([knowledge.py](knowledge.py)): hand-checked Acts and sections for each
   problem type. Only the entries that match the user's problem are put into the prompt.
2. **Prompt rule:** the model may cite only these laws, never case names or judgments.
3. **Citation guard** ([lawyer.py](lawyer.py)): every answer is scanned for Act and Section references,
   and any that are not in the knowledge base get a visible ⚠️ "unverified" warning.
4. It points users to a lawyer or to free legal aid (NALSA 15100) where it matters.

## Limits
- It covers 5 problem types. Anything else gets general guidance only.
- Topics are detected by keyword, so unusual wording can be missed.
- The knowledge base needs a lawyer's review before real use.
