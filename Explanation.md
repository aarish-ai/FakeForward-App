# FakeForward Detector: Technical & Non-Technical Explanation

## Non-Technical Overview

**What is it?**
FakeForward Detector is a web tool built to combat misinformation spread through forwarded messages (like those on WhatsApp or Telegram). Users can copy and paste a long message into the app, and the system will automatically break it down, check the facts, and give a clear verdict on whether the message is true, false, or misleading.

**How does it work?**
1. **Extract**: The system reads the pasted message and ignores opinions or jokes, pulling out only the checkable facts (e.g., "The sky is blue").
2. **Search**: For every fact, it searches Wikipedia and DuckDuckGo for evidence.
3. **Score**: It compares the fact against the found evidence and scores its accuracy from 0 to 100.
4. **Verdict**: It averages the scores to give an overall "True", "False", "Misleading", or "Unverifiable" rating.
5. **Share**: Users can click a button to copy a quick summary of the results to send back to whoever forwarded them the message.

**Why is it useful?**
It automates the tedious process of fact-checking. Instead of manually Googling 5 different claims from a single long forward, this tool does the heavy lifting in seconds and provides a simple color-coded result.

---

## Technical Overview

**Architecture & Stack**
The project follows a decoupled client-server architecture.
- **Frontend**: Plain HTML, CSS, and vanilla JavaScript. No heavy frameworks or build tools, making it extremely lightweight and easy to deploy on a static host like Netlify.
- **Backend**: Python 3.11 with FastAPI. It handles the orchestration of the AI models and search APIs.

**The Pipeline**
The backend `/analyze` endpoint triggers a linear, 4-stage pipeline (`main.py` -> `extractor.py` -> `searcher.py` -> `scorer.py` -> `verdict.py`):
1. **Extractor**: Uses an LLM (Gemini 2.5 Flash) prompted to return JSON containing up to 5 objective claims from the text.
2. **Searcher**: Makes parallel-like HTTP requests to the Wikipedia REST API and DuckDuckGo using the `duckduckgo-search` Python package.
3. **Scorer**: Feeds the claim + search results back into the LLM to request a score, verdict, and a 2-sentence summary. If the searcher found nothing, it bypasses the LLM entirely and returns `UNVERIFIABLE` to save API quota and latency.
4. **Verdict**: Aggregates the claim scores mathematically and maps them to final string categories.

**Resilience & Guardrails**
Built specifically for hackathon reliability, the system features multiple defensive coding layers:
- **Timeouts**: Every external HTTP call (Gemini, Wikipedia, DuckDuckGo) has strict timeouts (5s to 15s) so the API never hangs indefinitely.
- **Graceful Degradation**: DuckDuckGo search is wrapped in a catch-all exception block so rate-limiting doesn't break the pipeline.
- **LLM Fallback**: If Gemini fails (network issue, quota exceeded), the system seamlessly falls back to a locally hosted Ollama model (`qwen2.5:3b`).
- **JSON Repair**: The LLM parser strips markdown code fences. If JSON decoding still fails, it automatically runs one "repair" prompt before giving up.
- **Bounded Inputs**: Both the frontend textarea and backend Pydantic models enforce a 3000-character limit to prevent token exhaustion or denial-of-service attempts.
