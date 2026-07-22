# Sukuna AI ⛩️ — King of Curses Chatbot

Chat with **Ryomen Sukuna** (Jujutsu Kaisen) in a manga-sketch style chat panel — with **permanent chat history** and **long-term memory**. Powered by the free **Groq API**.

![style](https://img.shields.io/badge/style-manga%20sketch-black) ![api](https://img.shields.io/badge/API-Groq-orange) ![memory](https://img.shields.io/badge/memory-permanent-red)

## Features

- ⛩️ **Sukuna persona** — arrogant, ruthless King of Curses (persona lives in [`knowledge.json`](knowledge.json))
- 💾 **Permanent chat history** — saved in your browser's localStorage, survives refresh/close
- 🧠 **Long-term memory** — the app auto-distills facts about you every 10 messages and injects them into Sukuna's brain, so he remembers you even in endless conversations
- 🖋️ **Manga sketch UI** — halftone paper, ink-drawn speech bubbles, hand-drawn borders, Bangers/Patrick Hand fonts
- ⚡ **Streaming replies** via Groq (`llama-3.3-70b-versatile` by default)
- 🌐 Replies in your language — Hindi, Hinglish, or English

## Quick start

1. Get a free Groq API key → <https://console.groq.com/keys> (details in [`groq.md`](groq.md))
2. Open `index.html` in any browser (double-click, or `python3 -m http.server` and open `http://localhost:8000`)
3. Click **⚙**, paste your key, save
4. Speak, insect. 🔪

> Your API key stays in **your** browser only — requests go straight from your browser to Groq.

## Features Breakdown

### Chat Features
- ⛩️ **Sukuna persona** — unhinged, violent roaster at anger level 10000000000
- 💬 **Multi-chat history** — sidebar with unlimited conversations, per-chat timestamps
- 💾 **Permanent history** — saved in localStorage (survives browser close)
- 🧠 **Long-term memory** — auto-distilled facts injected into system prompt
- 📷 **Image upload** — send photos, Sukuna analyzes and reacts (uses vision model)
- 💭 **Thinking bubble** — see Sukuna's reasoning before response (with extended thinking)

### Backend Features (Optional)
- 🎤 **Text-to-Speech** — Generate Sukuna/Gojo/Megumi/Yuji voices via Hugging Face
- 🚀 **REST API** — Flask server for TTS, downloadable audio files
- 🧪 **Test suite** — Comprehensive tests for all features

## Files

| File | Purpose |
|---|---|
| `index.html` | Complete app — UI + Groq/chat logic + memory engine |
| `knowledge.json` | Sukuna persona & system prompt |
| `groq.md` | Groq API setup + how memory works |
| **Backend (Optional)** | |
| `tts_service.py` | Hugging Face TTS service (character voices) |
| `tts_server.py` | Flask API server (REST endpoints) |
| `test_tts.py` | Test suite for TTS |
| `TTS_SETUP.md` | TTS setup & usage guide |
| `requirements.txt` | Python dependencies |
| `.env` | Environment variables (not committed) |
