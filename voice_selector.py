#!/usr/bin/env python3
"""
Voice Selector - Choose your preferred voice
"""
import pyttsx3
import time

def select_voice():
    print("🎤 Voice Selection Tool")
    print("=" * 40)
    
    # Initialize TTS engine
    tts_engine = pyttsx3.init()
    
    # Get all available voices
    voices = tts_engine.getProperty('voices')
    
    if not voices:
        print("❌ No voices found!")
        return
    
    print(f"🔊 Found {len(voices)} voice(s):")
    print()
    
    # List all voices with details
    for i, voice in enumerate(voices):
        print(f"Voice {i}:")
        print(f"  Name: {voice.name}")
        print(f"  ID: {voice.id}")
        print(f"  Gender: {'Female' if 'zira' in voice.name.lower() or 'female' in voice.name.lower() or i == 1 else 'Male'}")
        print()
    
    # Test each voice
    test_text = "Hello, I am Pari, your voice assistant. How do you like my voice?"
    
    for i, voice in enumerate(voices):
        print(f"🔊 Testing Voice {i}: {voice.name}")
        tts_engine.setProperty('voice', voice.id)
        tts_engine.setProperty('rate', 180)
        tts_engine.setProperty('volume', 1.0)
        
        tts_engine.say(test_text)
        tts_engine.runAndWait()
        
        response = input(f"Do you like Voice {i} ({voice.name})? (y/n): ").lower().strip()
        if response == 'y' or response == 'yes':
            print(f"✅ Great! You selected: {voice.name}")
            print(f"Voice ID: {voice.id}")
            print(f"Voice Index: {i}")
            print()
            print("To use this voice in your assistant, remember:")
            print(f"- Voice Index: {i}")
            print(f"- Voice ID: {voice.id}")
            return i, voice.id, voice.name
        print()
    
    print("No voice selected. Using default.")
    return 0, voices[0].id, voices[0].name

if __name__ == "__main__":
    select_voice()
