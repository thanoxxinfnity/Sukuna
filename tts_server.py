"""
Flask Server for Sukuna AI TTS API
Provides HTTP endpoints to generate character voices.

Run: python tts_server.py
Access: http://localhost:5000
"""

from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from tts_service import generate_voice, list_characters, get_character_info
import os
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

OUTPUT_DIR = Path('./output_audio')


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'service': 'Sukuna TTS Server',
        'version': '1.0.0'
    }), 200


@app.route('/api/characters', methods=['GET'])
def get_characters():
    """Get list of available characters."""
    try:
        characters = list_characters()
        return jsonify({
            'status': 'success',
            'characters': characters
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/character/<char_name>', methods=['GET'])
def get_character(char_name):
    """Get details about a specific character."""
    try:
        info = get_character_info(char_name)
        if not info:
            return jsonify({
                'status': 'error',
                'message': f'Character "{char_name}" not found'
            }), 404

        return jsonify({
            'status': 'success',
            'character': char_name,
            'info': info
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/tts', methods=['POST'])
def generate_tts():
    """
    Generate TTS audio from text.

    Request JSON:
    {
        "text": "Hello world",
        "character": "sukuna",
        "format": "mp3"
    }

    Response:
    - Success (200): Returns audio file
    - Error (400/500): Returns JSON error message
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No JSON data provided'
            }), 400

        text = data.get('text', '').strip()
        character = data.get('character', 'sukuna').lower()
        output_format = data.get('format', 'mp3')

        if not text:
            return jsonify({
                'status': 'error',
                'message': 'Text field is required'
            }), 400

        if output_format not in ['mp3', 'wav', 'ogg', 'flac']:
            return jsonify({
                'status': 'error',
                'message': f'Invalid format: {output_format}'
            }), 400

        # Generate audio
        file_path, error = generate_voice(text, character, output_format)

        if error:
            return jsonify({
                'status': 'error',
                'message': error
            }), 400

        # Send audio file
        return send_file(
            file_path,
            mimetype=f'audio/{output_format}',
            as_attachment=True,
            download_name=f'{character}_voice.{output_format}'
        )

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Server error: {str(e)}'
        }), 500


@app.route('/api/tts/url', methods=['POST'])
def generate_tts_url():
    """
    Generate TTS audio and return downloadable URL.

    Request JSON:
    {
        "text": "Hello world",
        "character": "sukuna",
        "format": "mp3"
    }

    Response:
    {
        "status": "success",
        "audio_url": "/download/audio/filename.mp3",
        "character": "sukuna",
        "text": "Hello world"
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No JSON data provided'
            }), 400

        text = data.get('text', '').strip()
        character = data.get('character', 'sukuna').lower()
        output_format = data.get('format', 'mp3')

        if not text:
            return jsonify({
                'status': 'error',
                'message': 'Text field is required'
            }), 400

        # Generate audio
        file_path, error = generate_voice(text, character, output_format)

        if error:
            return jsonify({
                'status': 'error',
                'message': error
            }), 400

        # Return URL instead of file
        relative_path = file_path.replace('\\', '/')  # Windows compatibility
        download_url = f"/download/{relative_path}"

        return jsonify({
            'status': 'success',
            'audio_url': download_url,
            'character': character,
            'text': text
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Server error: {str(e)}'
        }), 500


@app.route('/download/<path:filename>', methods=['GET'])
def download_audio(filename):
    """Download generated audio file."""
    try:
        file_path = Path(filename)

        # Security: prevent path traversal
        if '..' in filename or filename.startswith('/'):
            return jsonify({
                'status': 'error',
                'message': 'Invalid file path'
            }), 403

        # Check if file exists
        if not file_path.exists():
            return jsonify({
                'status': 'error',
                'message': 'File not found'
            }), 404

        # Get MIME type
        ext = file_path.suffix.lower()
        mime_types = {
            '.mp3': 'audio/mpeg',
            '.wav': 'audio/wav',
            '.ogg': 'audio/ogg',
            '.flac': 'audio/flac'
        }
        mime_type = mime_types.get(ext, 'audio/mpeg')

        return send_file(
            file_path,
            mimetype=mime_type,
            as_attachment=True,
            download_name=f'sukuna_{file_path.stem}.{ext.lstrip(".")}'
        )

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Download error: {str(e)}'
        }), 500


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found',
        'available_endpoints': [
            'GET /api/health',
            'GET /api/characters',
            'GET /api/character/<char_name>',
            'POST /api/tts (returns audio file)',
            'POST /api/tts/url (returns download URL)',
            'GET /download/<filepath>'
        ]
    }), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors."""
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500


if __name__ == '__main__':
    print("🚀 Starting Sukuna TTS Server...")
    print("📍 Server running at http://localhost:5000")
    print("\n📚 API Endpoints:")
    print("  • GET  /api/health                 - Health check")
    print("  • GET  /api/characters             - List all characters")
    print("  • GET  /api/character/<name>       - Get character info")
    print("  • POST /api/tts                    - Generate & return audio file")
    print("  • POST /api/tts/url                - Generate & return download URL")
    print("  • GET  /download/<filepath>        - Download audio file")
    print("\n⚙️  Make sure .env file has HF_TOKEN set")
    print("=" * 50 + "\n")

    app.run(debug=True, host='localhost', port=5000)
