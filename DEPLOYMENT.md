# Sukuna AI - Deployment Guide 🚀

Deploy Sukuna AI to the world! This guide covers:
- 🌐 **Frontend** → GitHub Pages (static HTML/JS)
- 🔌 **Backend** → Cloud services (Flask/Python)

## Architecture

```
GitHub Pages (Frontend)
        ↓ (HTTPS requests)
Cloud Backend (TTS + Optional services)
        ↓
Hugging Face / Groq APIs
```

---

## Part 1: Deploy Frontend to GitHub Pages 🌐

### Step 1: Enable GitHub Pages

1. Go to your repository on GitHub: `https://github.com/thanoxxinfnity/Sukuna`
2. Settings → Pages
3. Select branch: `main` or `claude/sukuna-ai-persistent-memory-62ra7h`
4. Root folder: `/` (or `/docs` if you create one)
5. Click Save

Your site will be live at: `https://thanoxxinfnity.github.io/Sukuna/`

### Step 2: Verify Frontend Works

Open the GitHub Pages URL and test:
- Chat works ✅
- History sidebar works ✅
- Image upload works ✅
- Groq API calls work (using built-in key) ✅

---

## Part 2: Deploy Backend (TTS Server) to Cloud ☁️

### Option A: Render (Recommended - Free tier available)

1. **Create Render account** → https://render.com

2. **Create Web Service:**
   - Connect your GitHub repo
   - Select branch: `claude/sukuna-ai-persistent-memory-62ra7h`
   - Build command: `pip install -r requirements.txt`
   - Start command: `python tts_server.py`
   - Environment: Python 3.10
   - Free tier: 750 compute hours/month

3. **Set Environment Variables:**
   - Go to Service Settings → Environment
   - Add: `HF_TOKEN=<your_hugging_face_token>`
   - Get token from: https://huggingface.co/settings/tokens

4. **Get Your Backend URL:**
   - Render gives you: `https://sukuna-tts.onrender.com`
   - Test: `curl https://sukuna-tts.onrender.com/api/health`

### Option B: Railway (Easy, Free trial)

1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Select your Sukuna repo
4. Railway auto-detects Python and requirements.txt
5. Add `HF_TOKEN` in Variables
6. Deploy!

### Option C: Replit (Simplest)

1. Go to https://replit.com
2. "Import from GitHub" → paste repo URL
3. Click Run (auto-detects Python)
4. Replit provides a public URL automatically
5. Add `HF_TOKEN` in Secrets

---

## Part 3: Connect Frontend to Backend 🔗

### Update Frontend for Remote Backend

In `index.html`, change the TTS endpoint:

**Find this line:**
```javascript
const TTS_URL = 'http://localhost:5000';
```

**Update to your backend URL:**
```javascript
const TTS_URL = 'https://sukuna-tts.onrender.com';
```

Or make it dynamic:
```javascript
const TTS_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:5000' 
  : 'https://sukuna-tts.onrender.com';
```

### Add TTS Button to Frontend

Add a 🎤 voice button to the chat UI:

```javascript
// In index.html, add to input bar:
document.getElementById('voiceBtn').addEventListener('click', async () => {
  const text = document.getElementById('msg').value;
  if (!text) return;
  
  const response = await fetch(`${TTS_URL}/api/tts/url`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, character: 'sukuna', format: 'mp3' })
  });
  
  const data = await response.json();
  if (data.audio_url) {
    const audio = new Audio(data.audio_url);
    audio.play();
  }
});
```

---

## Part 4: Domain & Custom URL (Optional)

### Use Custom Domain with GitHub Pages

1. Buy domain (GoDaddy, Namecheap, etc.)
2. Point to GitHub Pages:
   - `A` record: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - Or `CNAME`: `thanoxxinfnity.github.io`
3. GitHub Pages Settings → Custom domain → enter your domain
4. GitHub auto-generates SSL certificate (HTTPS)

Example: `sukuna.yourdomin.com`

---

## Security Checklist ✅

### Frontend (GitHub Pages)
- ✅ No sensitive data in HTML/JS
- ✅ API keys are user-provided (Groq token) or environment vars (HF token)
- ✅ Chat history is localStorage-only (never sent to server)

### Backend (Render/Railway/Replit)
- ✅ `HF_TOKEN` is environment variable (not in code)
- ✅ `.env` file is in `.gitignore`
- ✅ `.env` is never committed to Git
- ✅ Backend validates all inputs before API calls

### API Keys
```
🚫 Never: Hardcode secrets in code/docs
✅ Always: Use environment variables
✅ Always: Add sensitive files to .gitignore
✅ Always: Use GitHub's secret scanning
```

---

## Testing Deployment

### Test Frontend
```bash
# Visit GitHub Pages URL
https://thanoxxinfnity.github.io/Sukuna/

# Test features:
1. Type message → Sukuna replies (Groq API)
2. Upload image → Sukuna analyzes (vision)
3. Check sidebar → History persists
4. Refresh page → Chat history restored
```

### Test Backend
```bash
# Health check
curl https://YOUR_BACKEND_URL/api/health

# List characters
curl https://YOUR_BACKEND_URL/api/characters

# Generate voice
curl -X POST https://YOUR_BACKEND_URL/api/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "Test voice", "character": "sukuna"}'
```

### Test Integration
1. Open GitHub Pages frontend
2. Click 🎤 voice button
3. Audio should play from TTS backend

---

## Troubleshooting

### Frontend shows "API Error 404"
- Backend URL not updated in index.html
- Backend service might be down (check on Render/Railway)
- CORS not enabled on backend (Flask-CORS should handle it)

### TTS gives "Invalid HF_TOKEN"
- Check environment variable is set correctly on cloud platform
- Regenerate token at https://huggingface.co/settings/tokens
- Redeploy after updating token

### GitHub Pages shows blank page
- Repository is private (make it public)
- Pages branch not selected in Settings
- index.html is not in repo root

### Rate limit errors
- Groq: Free tier has rate limits (wait a few minutes)
- Hugging Face: Free tier has rate limits
- Consider upgrading if heavy usage

---

## Cost Breakdown

| Service | Cost | Notes |
|---------|------|-------|
| **GitHub Pages** | Free | Unlimited static hosting |
| **Render** | Free | 750 hrs/month compute, sleeps after 15min inactivity |
| **Railway** | Free trial | After trial: $5-20/month |
| **Replit** | Free | Limited resources, simple deployments |
| **Groq API** | Free | Rate limited, sufficient for light use |
| **Hugging Face** | Free | Rate limited, sufficient for light use |

**Total for hobby project:** ~$0 (all free tier)

---

## Next Steps

1. **Deploy frontend to GitHub Pages** (5 min)
2. **Deploy backend to Render** (10 min)
3. **Update frontend with backend URL** (2 min)
4. **Test TTS integration** (5 min)
5. **Share your Sukuna AI** 🎉

---

## Live Demo URL

Once deployed:
- Frontend: `https://thanoxxinfnity.github.io/Sukuna/`
- Backend API: `https://sukuna-tts.onrender.com/api/health`

---

## Questions?

- GitHub Pages docs: https://docs.github.com/en/pages
- Render docs: https://render.com/docs
- Hugging Face docs: https://huggingface.co/docs
- Groq docs: https://groq.com/docs

**Deploy with confidence! Sukuna will conquer the web.** ⛩️🔥
