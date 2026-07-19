# Groq API Setup ⛩️

Sukuna AI runs on the **Groq API** (free tier available, blazing fast inference).

## 1. Get your API key

1. Go to <https://console.groq.com/keys>
2. Sign in (Google account works) — it's free.
3. Click **Create API Key**, copy the key (starts with `gsk_...`).

## 2. Use it in the app

1. Open `index.html` in any browser.
2. Click the **⚙ gear icon** in the top bar.
3. Paste your key and save. It is stored **only in your browser's localStorage** — it never leaves your machine except to call Groq directly.

## 3. Model

Default model: `llama-3.3-70b-versatile` (you can change it in the settings panel).

Other good Groq options:

| Model | Notes |
|---|---|
| `llama-3.3-70b-versatile` | Best quality (default) |
| `llama-3.1-8b-instant` | Fastest, lighter |
| `openai/gpt-oss-20b` | Alternative |

## How memory works 🧠

- **Permanent chat history** — every message is saved to `localStorage` and restored when you reopen the page. No history is ever lost on refresh.
- **Long-term memory** — every 10 messages, the app silently asks the model to distill important facts about you and the conversation into a compact memory. That memory is injected into Sukuna's system prompt on every request, so he *remembers you* even in very long conversations (only the last ~20 messages are sent raw; older context lives in the distilled memory).
- **Persona** — loaded from [`knowledge.json`](knowledge.json).

## Reset

- **🗑 Clear chat** — wipes the visible history but keeps long-term memory.
- **💀 Full reset** (in settings) — wipes history, memory, and API key.
