# Quick TTS Test 🎤

Verify everything is working before deployment!

## Local Test (No deployment needed)

### Step 1: Start TTS Backend Locally

```bash
# Terminal 1: Start Flask server
cd /home/user/Sukuna
python tts_server.py

# Output should show:
# 🚀 Starting Sukuna TTS Server...
# 📍 Server running at http://localhost:5000
```

### Step 2: Test Backend API

```bash
# Terminal 2: Test health
curl http://localhost:5000/api/health

# Should return:
# {"status":"ok","service":"Sukuna TTS Server","version":"1.0.0"}
```

### Step 3: Generate Voice File

```bash
# Generate Sukuna's voice
curl -X POST http://localhost:5000/api/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "KUKUKU! Speak insect!", "character": "sukuna", "format": "mp3"}' \
  --output sukuna_voice.mp3

# Check if file was created
ls -lh sukuna_voice.mp3

# Play it (macOS/Linux)
afplay sukuna_voice.mp3
# or
mpv sukuna_voice.mp3
```

### Step 4: Test Frontend Integration

```bash
# Terminal 3: Serve frontend
cd /home/user/Sukuna
python3 -m http.server 8000

# Open browser:
# http://localhost:8000

# In the chat:
# 1. Type something → Sukuna replies
# 2. Look for 🎤 button (next to 📷)
# 3. Click 🎤 → Audio should play!
```

---

## What Should Happen

✅ **Green light checklist:**

```
TTS Service
  ✅ python tts_service.py runs without errors
  ✅ tts_server.py starts Flask server at localhost:5000
  ✅ /api/health returns OK status
  ✅ /api/characters lists 4 characters
  ✅ /api/tts generates MP3 file
  ✅ Audio file plays when you click play

Frontend
  ✅ index.html loads in browser
  ✅ Chat with Sukuna works (Groq API)
  ✅ Image upload works
  ✅ 🎤 button appears in input bar
  ✅ Click 🎤 → Last Sukuna message plays as voice
  ✅ Audio controls appear (play/pause/volume)

Netlify Deployment
  ✅ Site builds and deploys
  ✅ Frontend accessible at netlify URL
  ✅ Chat still works (Groq API in frontend)
  ✅ 🎤 button calls your Render backend
  ✅ Audio plays from Render TTS service
```

---

## Troubleshooting

### Backend won't start
```bash
# Error: Module not found
pip install -r requirements.txt

# Error: HF_TOKEN missing
echo "HF_TOKEN=your_token" > .env

# Error: Port 5000 already in use
python tts_server.py --port 5001
```

### Frontend can't find backend
```javascript
// In browser console (F12):
// Check what TTS_URL is set to:
console.log(TTS_URL);

// Should print:
// http://localhost:5000 (if local)
// https://sukuna-tts.onrender.com (if remote)
```

### Audio doesn't play
```javascript
// Check browser console for errors
// Click 🎤 button and look for error message
// Make sure CORS is enabled on backend
// (tts_server.py line 8 should have CORS(app))
```

### Render backend sleeping
```bash
# Render free tier sleeps after 15 minutes of no activity
# First request will be slow (30 seconds)
# Subsequent requests are instant
# This is normal for free tier!
```

---

## Quick Commands

```bash
# Kill Flask server
pkill -f "python tts_server.py"

# Check if port 5000 is in use
lsof -i :5000

# Clear output_audio directory
rm output_audio/*.mp3

# Test all characters
for char in sukuna gojo megumi yuji; do
  curl -X POST http://localhost:5000/api/tts \
    -H "Content-Type: application/json" \
    -d "{\"text\": \"Hello from $char\", \"character\": \"$char\"}" \
    --output $char.mp3
done
```

---

## Success = This Works

```
Browser Console (F12):
> console.log(TTS_URL)
< "http://localhost:5000"

Type in chat:
> "Sukuna, are you here?"

Sukuna replies:
< "KUKUKU! What do you want, insect?!"

Click 🎤:
🔊 Audio plays: "KUKUKU! What do you want, insect?!"
```

---

**If all green → You're ready to deploy!** 🚀

Next: Deploy to Netlify + Render using NETLIFY_SETUP.md
