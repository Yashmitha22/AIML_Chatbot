#!/usr/bin/env python3
"""
Simple TTS Test - Check if you can hear voice output
"""
import pyttsx3
import time

def test_audio():
    print("🔊 Testing TTS Audio Output")
    print("=" * 30)
    
    # Initialize TTS
    tts_engine = pyttsx3.init()
    
    # Get voices
    voices = tts_engine.getProperty('voices')
    
    print(f"Found {len(voices)} voices:")
    for i, voice in enumerate(voices):
        print(f"  {i}: {voice.name}")
    
    # Test with maximum volume and slow speech
    tts_engine.setProperty('rate', 150)  # Slower
    tts_engine.setProperty('volume', 1.0)  # Maximum volume
    
    # Test default voice first
    print("\n🎵 Testing DEFAULT voice...")
    print("Listen carefully for: 'This is a test'")
    tts_engine.say("This is a test")
    tts_engine.runAndWait()
    
    response = input("Did you hear 'This is a test'? (y/n): ").strip().lower()
    if response in ['y', 'yes']:
        print("✅ Great! TTS is working!")
        
        # Now test female voice (Zira)
        if len(voices) > 1:
            print("\n👩 Testing FEMALE voice (Zira)...")
            tts_engine.setProperty('voice', voices[1].id)  # Zira
            print("Listen for: 'Hello, I am Pari with female voice'")
            tts_engine.say("Hello, I am Pari with female voice")
            tts_engine.runAndWait()
            
            response2 = input("Did you hear the female voice? (y/n): ").strip().lower()
            if response2 in ['y', 'yes']:
                print("✅ Perfect! Female voice works!")
                print(f"Female voice ID: {voices[1].id}")
                print("Your voice assistant should use Voice 1 (Zira)")
            else:
                print("❌ Female voice not working")
        
    else:
        print("❌ TTS not working. Check:")
        print("  1. Volume is turned up")
        print("  2. Speakers/headphones connected")
        print("  3. Windows audio services running")

if __name__ == "__main__":
    test_audio()
