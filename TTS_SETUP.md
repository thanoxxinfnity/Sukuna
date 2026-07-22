# Sukuna AI - Text-to-Speech (TTS) Setup Guide 🎤

Generate character voices for Sukuna, Gojo, Megumi, and Yuji using Hugging Face TTS models.

## Prerequisites

- Python 3.8+
- Hugging Face Account (free)
- HF API Token

## Step 1: Get Hugging Face API Token

1. Visit [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Create a new token (with `read` permission is enough)
3. Copy the token

## Step 2: Set Up Environment

### Option A: Using Existing `.env` File

The `.env` file is already created with placeholder. Just update:

```env
HF_TOKEN=your_actual_hf_token_here
```

### Option B: Create `.env` Manually

```bash
echo "HF_TOKEN=your_token_here" > .env
```

Then replace `your_token_here` with your actual HF token from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

**⚠️ Security:** `.env` is in `.gitignore` — your token won't be committed to Git.

## Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Test TTS Service (CLI)

Run the Python service directly to test:

```bash
python tts_service.py
```

Expected output:
```
🎤 Sukuna AI - Text-to-Speech Service
==================================================

📢 Available Characters:
  • SUKUNA: Ryomen Sukuna - King of Curses (deep, aggressive, commanding tone)
  • GOJO: Satoru Gojo - Infinity (calm, confident, smooth tone)
  • MEGUMI: Megumi Fushiguro - Calm, composed sorcerer
  • YUJI: Yuji Itadori - Energetic, determined protagonist

🗣️ Example 1 - Sukuna speaks:
  ✅ Audio saved: output_audio/sukuna_KUKUKU_You_dare_challenge_the_King_of_Curses_12345678.mp3

🗣️ Example 2 - Gojo speaks:
  ✅ Audio saved: output_audio/gojo_You're_free._I_am_the_strongest_87654321.mp3

✨ TTS Service ready!
```

## Step 5: Run TTS Server

Start the Flask API server:

```bash
python tts_server.py
```

Output:
```
🚀 Starting Sukuna TTS Server...
📍 Server running at http://localhost:5000

📚 API Endpoints:
  • GET  /api/health                 - Health check
  • GET  /api/characters             - List all characters
  • GET  /api/character/<name>       - Get character info
  • POST /api/tts                    - Generate & return audio file
  • POST /api/tts/url                - Generate & return download URL
  • GET  /download/<filepath>        - Download audio file
```

## Usage Examples

### Python (Direct Service)

```python
from tts_service import generate_voice

# Generate Sukuna's voice
file_path, error = generate_voice("Speak, insect!", "sukuna")
if file_path:
    print(f"✅ Audio: {file_path}")
else:
    print(f"❌ Error: {error}")
```

### cURL (API Endpoints)

**Get Characters List:**
```bash
curl http://localhost:5000/api/characters
```

**Generate & Download Audio:**
```bash
curl -X POST http://localhost:5000/api/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "KUKUKU! You dare challenge me?!", "character": "sukuna", "format": "mp3"}' \
  --output sukuna_voice.mp3
```

**Generate & Get URL:**
```bash
curl -X POST http://localhost:5000/api/tts/url \
  -H "Content-Type: application/json" \
  -d '{"text": "I am the strongest", "character": "gojo"}' \
  | jq '.audio_url'
```

### JavaScript/Frontend

```javascript
// Function to request TTS from server
async function generateVoice(text, character = 'sukuna') {
  try {
    const response = await fetch('http://localhost:5000/api/tts/url', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: text,
        character: character,
        format: 'mp3'
      })
    });

    if (!response.ok) throw new Error(await response.text());

    const data = await response.json();
    return data.audio_url;  // Returns: /download/output_audio/...

  } catch (error) {
    console.error('TTS Error:', error);
    return null;
  }
}

// Usage
const audioUrl = await generateVoice("Speak, insect!", "sukuna");
if (audioUrl) {
  const audio = new Audio(audioUrl);
  audio.play();
}
```

## Available Characters

| Character | Voice | Tone | Speed |
|-----------|-------|------|-------|
| **sukuna** | Deep, aggressive | Commanding, ruthless | 0.9x |
| **gojo** | Neutral, smooth | Confident, calm | 1.0x |
| **megumi** | Calm, composed | Determined, serious | 0.95x |
| **yuji** | Energetic, youthful | Enthusiastic, hopeful | 1.05x |

## Troubleshooting

### ❌ `HF_TOKEN not found in .env`
- Make sure `.env` file exists in project root
- Check that `HF_TOKEN=...` is set correctly
- Restart the server after changing `.env`

### ❌ `Invalid HF_TOKEN. Check your credentials.`
- Token may be expired or invalid
- Generate a new token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
- Update `.env` and restart server

### ❌ `HuggingFace API rate limited`
- Wait a few minutes before trying again
- Free tier has rate limits
- Consider upgrading for higher limits

### ❌ `Request timeout`
- First API call might be slow (model loading)
- Retry after a few seconds
- Check internet connection

### ❌ Audio file not found
- Check `output_audio/` directory exists
- Ensure write permissions on directory
- Free up disk space if full

## Architecture

```
Sukuna AI (Frontend)
    ↓ (HTTP POST /api/tts)
Flask TTS Server (localhost:5000)
    ↓ (Python)
tts_service.py (TTS Logic)
    ↓ (API calls)
Hugging Face Models
    ↓ (Audio)
output_audio/ (MP3, WAV, etc.)
```

## Integration with Frontend

To add voice to chat messages in `index.html`:

```javascript
// In your chat response handler:
const audioUrl = await fetch('/api/tts/url', {
  method: 'POST',
  body: JSON.stringify({
    text: sukunaReply,
    character: 'sukuna',
    format: 'mp3'
  })
}).then(r => r.json()).then(d => d.audio_url);

// Add audio player to bubble
const audioPlayer = document.createElement('audio');
audioPlayer.src = audioUrl;
audioPlayer.controls = true;
bubble.appendChild(audioPlayer);
```

## Performance Tips

1. **Cache generated audio** — Store file paths to avoid regenerating same text
2. **Use shorter texts** — Under 100 characters is fastest
3. **Batch requests** — Generate multiple voices in parallel
4. **Pre-warm models** — First request loads model; subsequent are faster

## Next Steps

- Integrate TTS button (🎤) into chat UI
- Add voice selection dropdown
- Store generated audio files for reuse
- Add audio playback controls to messages
- Implement voice queue for simultaneous generations

---

**Need Help?** Check HuggingFace docs: https://huggingface.co/docs/inference-api
