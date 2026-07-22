# Deploy to Netlify + TTS Backend 🚀

## Quick Setup (5 minutes)

### Step 1: Deploy Frontend to Netlify

```bash
# Option A: Via Netlify UI (Easiest)
1. Go to https://netlify.com
2. Click "Add new site" → "Import an existing project"
3. Authorize GitHub
4. Select repository: "Sukuna"
5. Configure:
   - Branch: claude/sukuna-ai-persistent-memory-62ra7h
   - Build command: (leave empty)
   - Publish directory: . (root)
6. Deploy!
```

**Your site will be live at:** `https://your-sukuna-app.netlify.app`

### Step 2: Deploy Backend to Render (Free)

TTS server cannot run on Netlify (it's static hosting only). Deploy Flask backend to Render:

```bash
1. Go to https://render.com
2. "New" → "Web Service"
3. Connect GitHub repo: Sukuna
4. Configure:
   - Name: sukuna-tts
   - Runtime: Python 3.10
   - Build command: pip install -r requirements.txt
   - Start command: python tts_server.py
   - Free tier is fine
5. Environment Variables:
   - HF_TOKEN: <your_hugging_face_token>
6. Deploy
```

Render will give you a URL like: `https://sukuna-tts.onrender.com`

### Step 3: Connect Frontend to Backend

Update Netlify environment or modify code:

**Option A: Netlify Environment Variables**
1. Netlify site → Settings → Build & deploy → Environment
2. Add: `TTS_URL=https://sukuna-tts.onrender.com`
3. Rebuild site

**Option B: Edit index.html**
```javascript
// Find this line in index.html:
const TTS_URL = window.location.hostname === 'localhost'
  ? 'http://localhost:5000'
  : 'https://sukuna-tts.onrender.com';  // ← Change this URL

// Replace with your Render URL:
const TTS_URL = 'https://sukuna-tts.onrender.com';
```

## Testing TTS

### Test 1: Check if TTS button appears
- Open your Netlify site
- Look for 🎤 button next to 📷 button in chat input
- If you don't see it, hard refresh (Ctrl+Shift+R)

### Test 2: Generate voice
```bash
# From terminal:
curl -X POST https://sukuna-tts.onrender.com/api/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "Speak insect!", "character": "sukuna", "format": "mp3"}' \
  --output test.mp3

# Play test.mp3 - if it works, audio is generating!
```

### Test 3: Full integration
1. Go to Netlify site
2. Chat with Sukuna (he'll reply)
3. Click 🎤 button
4. If audio plays → TTS works! ✅
5. If error → Check backend URL in index.html

## Troubleshooting

### 🎤 Button shows but no audio
**Problem:** Backend URL wrong or backend is down
**Fix:**
```javascript
// In index.html, change:
const TTS_URL = 'https://your-actual-render-url.onrender.com';
```

### Backend says "does not exist" 
**Problem:** Render URL is wrong
**Fix:**
1. Go to render.com → Your service
2. Copy the exact public URL
3. Update in index.html

### Audio file downloads instead of plays
**Problem:** CORS headers missing (Flask-CORS not working)
**Fix:** Make sure tts_server.py has `CORS(app)` on line 8

### First request is slow
**Problem:** Render free tier spins down, needs to boot
**Fix:** Just wait 30 seconds on first request, then it's fast

## Costs

| Service | Cost | Limit |
|---------|------|-------|
| Netlify | Free | 300 min/month builds, unlimited hosting |
| Render | Free | 750 compute hours/month (always free, sleeps after 15min) |
| Groq API | Free | Rate limited but sufficient |
| Hugging Face | Free | Rate limited but sufficient |

**Total:** $0 for hobby projects

## Architecture

```
User's Browser (Netlify)
        ↓
Sukuna AI (Frontend - HTML/JS)
        ↓ (HTTP CORS request)
Render Backend (Flask/Python)
        ↓
Hugging Face TTS
        ↓ (MP3 audio)
Browser plays voice 🔊
```

## Live Example

```
Frontend: https://your-sukuna-app.netlify.app
Backend:  https://sukuna-tts.onrender.com
Chat:     Works (Groq API, no key needed - built-in)
Images:   Works (vision model, auto-fallback)
Thinking: Works (💭 collapsible)
Voices:   Works (🎤 button plays TTS audio)
```

## Commands Reference

```bash
# Test backend health
curl https://sukuna-tts.onrender.com/api/health

# List characters
curl https://sukuna-tts.onrender.com/api/characters

# Generate MP3
curl -X POST https://sukuna-tts.onrender.com/api/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "Test", "character": "sukuna"}' \
  --output voice.mp3
```

## Next Steps

1. ✅ Deploy frontend to Netlify (5 min)
2. ✅ Deploy backend to Render (5 min)
3. ✅ Update TTS_URL in index.html (1 min)
4. ✅ Test 🎤 voice button (2 min)
5. 🎉 Share your Sukuna AI!

---

**Questions?**
- Netlify docs: https://docs.netlify.com
- Render docs: https://render.com/docs
- This repo: https://github.com/thanoxxinfnity/Sukuna
