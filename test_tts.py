#!/usr/bin/env python3
"""
Test script for Sukuna TTS Service
Quick testing of character voice generation
"""

import sys
from tts_service import generate_voice, list_characters, get_character_info


def print_header(text):
    """Print a formatted header."""
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}\n")


def test_basic_generation():
    """Test basic voice generation for each character."""
    print_header("Test 1: Basic Voice Generation")

    test_cases = [
        ("sukuna", "KUKUKU! You dare challenge the King of Curses?!"),
        ("gojo", "I am the strongest, after all."),
        ("megumi", "Let's do this together."),
        ("yuji", "I won't lose! Not to you!"),
    ]

    for character, text in test_cases:
        print(f"🗣️  Generating {character.upper()}'s voice...")
        print(f"   Text: \"{text}\"")

        file_path, error = generate_voice(text, character)

        if file_path:
            print(f"   ✅ Success! Saved to: {file_path}")
        else:
            print(f"   ❌ Error: {error}")
        print()


def test_invalid_character():
    """Test error handling for invalid character."""
    print_header("Test 2: Invalid Character Handling")

    print("Attempting to generate voice for non-existent character 'unknown'...")
    file_path, error = generate_voice("Test", "unknown")

    if error:
        print(f"✅ Correctly caught error: {error}")
    else:
        print(f"❌ Should have failed but didn't!")


def test_empty_text():
    """Test error handling for empty text."""
    print_header("Test 3: Empty Text Handling")

    print("Attempting to generate voice with empty text...")
    file_path, error = generate_voice("", "sukuna")

    if error:
        print(f"✅ Correctly caught error: {error}")
    else:
        print(f"❌ Should have failed but didn't!")


def test_long_text():
    """Test error handling for text that's too long."""
    print_header("Test 4: Text Length Validation")

    long_text = "a" * 1001  # Exceeds 1000 char limit

    print(f"Attempting to generate voice with {len(long_text)} character text...")
    file_path, error = generate_voice(long_text, "sukuna")

    if error:
        print(f"✅ Correctly caught error: {error}")
    else:
        print(f"❌ Should have failed but didn't!")


def test_character_list():
    """Test listing available characters."""
    print_header("Test 5: Available Characters")

    characters = list_characters()
    print(f"Found {len(characters)} characters:\n")

    for char, description in characters.items():
        info = get_character_info(char)
        print(f"📍 {char.upper()}")
        print(f"   Description: {description}")
        print(f"   Pitch: {info.get('pitch', 'N/A')}")
        print(f"   Speed: {info.get('speed', 'N/A')}")
        print()


def test_special_characters():
    """Test text with special characters."""
    print_header("Test 6: Special Characters in Text")

    special_texts = [
        ("sukuna", "What's up, bro?"),
        ("gojo", "I'm 10/10, no cap!"),
        ("megumi", "It's... complicated."),
        ("yuji", "We can't give up!!!"),
    ]

    for character, text in special_texts:
        print(f"Testing {character} with: \"{text}\"")
        file_path, error = generate_voice(text, character)

        if file_path:
            print(f"   ✅ Generated: {file_path}")
        else:
            print(f"   ❌ Error: {error}")
        print()


def test_different_formats():
    """Test different output formats."""
    print_header("Test 7: Different Audio Formats")

    formats = ['mp3', 'wav', 'ogg', 'flac']
    text = "Testing different formats"

    for fmt in formats:
        print(f"Attempting to generate {fmt.upper()} format...")
        file_path, error = generate_voice(text, "sukuna", fmt)

        if file_path:
            print(f"   ✅ Generated: {file_path}")
        else:
            print(f"   ⚠️  Note: {error}")
        print()


def run_all_tests():
    """Run all tests."""
    print("\n")
    print("🎤" * 30)
    print("SUKUNA AI - TTS SERVICE TEST SUITE")
    print("🎤" * 30)

    try:
        test_character_list()
        test_basic_generation()
        test_invalid_character()
        test_empty_text()
        test_long_text()
        test_special_characters()
        test_different_formats()

        print_header("✨ All Tests Complete!")
        print("Check output_audio/ directory for generated files.\n")

    except Exception as e:
        print(f"\n❌ Test suite failed: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()
