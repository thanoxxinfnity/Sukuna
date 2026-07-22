"""
Hugging Face Text-to-Speech (TTS) Service for Sukuna AI
Generates character voices using Hugging Face models and APIs.
"""

import os
import json
import requests
from pathlib import Path
from typing import Optional, Dict, Tuple
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

HF_TOKEN = os.getenv('HF_TOKEN')
if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found in .env file. Please set it first.")

# Character to HuggingFace Space/Model mapping
CHARACTER_VOICES: Dict[str, Dict[str, str]] = {
    'sukuna': {
        'description': 'Ryomen Sukuna - King of Curses (deep, aggressive, commanding tone)',
        'model': 'https://api-inference.huggingface.co/models/gpt2',  # TTS model endpoint
        'speaker_id': '0',  # Some models have speaker IDs
        'pitch': '0.8',  # Lower pitch for aggressive tone
        'speed': '0.9',
    },
    'gojo': {
        'description': 'Satoru Gojo - Infinity (calm, confident, smooth tone)',
        'model': 'https://api-inference.huggingface.co/models/gpt2',
        'speaker_id': '1',
        'pitch': '1.0',
        'speed': '1.0',
    },
    'megumi': {
        'description': 'Megumi Fushiguro - Calm, composed sorcerer',
        'model': 'https://api-inference.huggingface.co/models/gpt2',
        'speaker_id': '2',
        'pitch': '0.95',
        'speed': '0.95',
    },
    'yuji': {
        'description': 'Yuji Itadori - Energetic, determined protagonist',
        'model': 'https://api-inference.huggingface.co/models/gpt2',
        'speaker_id': '3',
        'pitch': '1.05',
        'speed': '1.05',
    },
}

# Ensure output directory exists
OUTPUT_DIR = Path('./output_audio')
OUTPUT_DIR.mkdir(exist_ok=True)


def validate_character(character: str) -> bool:
    """Check if character is valid."""
    return character.lower() in CHARACTER_VOICES


def generate_voice(
    text: str,
    character: str = 'sukuna',
    output_format: str = 'mp3'
) -> Tuple[Optional[str], Optional[str]]:
    """
    Generate TTS audio for a given text using Hugging Face models.

    Args:
        text: The text to convert to speech
        character: Character name ('sukuna', 'gojo', 'megumi', 'yuji')
        output_format: Audio format ('mp3', 'wav', 'ogg')

    Returns:
        Tuple of (file_path: str or None, error_message: str or None)
        If successful: (file_path, None)
        If failed: (None, error_message)

    Example:
        >>> file_path, error = generate_voice("Speak, insect!", "sukuna")
        >>> if file_path:
        ...     print(f"Audio saved to: {file_path}")
        ... else:
        ...     print(f"Error: {error}")
    """

    # Validate character
    if not validate_character(character):
        valid = ', '.join(CHARACTER_VOICES.keys())
        return None, f"Invalid character '{character}'. Valid: {valid}"

    # Validate text
    if not text or len(text.strip()) == 0:
        return None, "Text cannot be empty"

    if len(text) > 1000:
        return None, "Text too long (max 1000 characters)"

    character = character.lower()
    char_config = CHARACTER_VOICES[character]

    try:
        # Generate unique filename
        safe_text = "".join(c if c.isalnum() or c in (' ', '-') else '_' for c in text[:30])
        safe_text = safe_text.replace(' ', '_')[:20]
        filename = f"{character}_{safe_text}_{hash(text) & 0x7fffffff}.{output_format}"
        file_path = OUTPUT_DIR / filename

        # Try using HuggingFace Inference API for TTS
        # This uses a public TTS model endpoint
        audio_bytes = _call_hf_tts_api(text, character, char_config)

        if audio_bytes is None:
            return None, "Failed to generate audio from HuggingFace API"

        # Save audio file
        with open(file_path, 'wb') as f:
            f.write(audio_bytes)

        return str(file_path), None

    except Exception as e:
        return None, f"Error generating voice: {str(e)}"


def _call_hf_tts_api(text: str, character: str, config: Dict) -> Optional[bytes]:
    """
    Call HuggingFace TTS API to generate audio.

    Uses the HuggingFace Inference API with a TTS model.
    """

    # Using Speecht5 TTS model on HuggingFace
    api_url = "https://api-inference.huggingface.co/models/microsoft/speecht5_tts"

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}

    payload = {
        "inputs": text,
        "parameters": {
            "speaker_embeddings": config.get('speaker_id', '0'),
        }
    }

    try:
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            return response.content  # Binary audio data
        elif response.status_code == 401:
            raise PermissionError("Invalid HF_TOKEN. Check your credentials.")
        elif response.status_code == 429:
            raise RuntimeError("HuggingFace API rate limited. Try again later.")
        else:
            error_msg = response.json().get('error', f"HTTP {response.status_code}")
            raise RuntimeError(f"HuggingFace API error: {error_msg}")

    except requests.exceptions.Timeout:
        raise RuntimeError("Request timeout. HuggingFace API took too long.")
    except requests.exceptions.ConnectionError:
        raise RuntimeError("Connection error. Cannot reach HuggingFace API.")


def list_characters() -> Dict[str, str]:
    """List all available characters and their descriptions."""
    return {
        char: config['description']
        for char, config in CHARACTER_VOICES.items()
    }


def get_character_info(character: str) -> Optional[Dict]:
    """Get detailed info about a specific character."""
    character = character.lower()
    return CHARACTER_VOICES.get(character)


# ============ CLI Usage Example ============
if __name__ == "__main__":
    print("🎤 Sukuna AI - Text-to-Speech Service")
    print("=" * 50)

    # List available characters
    print("\n📢 Available Characters:")
    for char, desc in list_characters().items():
        print(f"  • {char.upper()}: {desc}")

    # Example 1: Generate Sukuna's voice
    print("\n\n🗣️ Example 1 - Sukuna speaks:")
    sukuna_text = "KUKUKU... You dare challenge the King of Curses?!"
    file_path, error = generate_voice(sukuna_text, 'sukuna')
    if file_path:
        print(f"  ✅ Audio saved: {file_path}")
    else:
        print(f"  ❌ Error: {error}")

    # Example 2: Generate Gojo's voice
    print("\n\n🗣️ Example 2 - Gojo speaks:")
    gojo_text = "You're free. I am the strongest, after all."
    file_path, error = generate_voice(gojo_text, 'gojo')
    if file_path:
        print(f"  ✅ Audio saved: {file_path}")
    else:
        print(f"  ❌ Error: {error}")

    # Example 3: Invalid character (will error)
    print("\n\n🗣️ Example 3 - Invalid character:")
    file_path, error = generate_voice("Test", 'unknown_char')
    if error:
        print(f"  ❌ Error: {error}")

    print("\n" + "=" * 50)
    print("✨ TTS Service ready!")
