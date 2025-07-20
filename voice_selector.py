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
        gender = "Female" if any(keyword in voice.name.lower() for keyword in ['zira', 'female', 'woman']) else "Male"
        print(f"  Gender: {gender}")
        print()
    
    # Test each voice
    test_text = "Hello, I am Pari, your voice assistant. How do you like my voice?"
    
    for i, voice in enumerate(voices):
        print(f"🔊 Testing Voice {i}: {voice.name}")
        try:
            tts_engine.setProperty('voice', voice.id)
            tts_engine.setProperty('rate', 180)
            tts_engine.setProperty('volume', 1.0)
            tts_engine.say(test_text)
            tts_engine.runAndWait()
            response = input(f"Do you like Voice {i} ({voice.name})? (y/n): ").lower().strip()
            if response in ('y', 'yes'):
                print(f"✅ Great! You selected: {voice.name}")
                print(f"Voice ID: {voice.id}")
                print(f"Voice Index: {i}")
                print()
                print("To use this voice in your assistant, remember:")
                print(f"- Voice Index: {i}")
                print(f"- Voice ID: {voice.id}")
                return i, voice.id, voice.name
            print()
        except Exception as e:
            print(f"❌ Error testing voice {i}: {e}")
            print()
    
    print("No voice selected. Using default.")
    if voices:
        return 0, voices[0].id, voices[0].name
    else:
        return None, None, None

if __name__ == "__main__":
    select_voice()
def setup_tts(self):
    try:
        # Force reinitialize TTS for female voice
        self.tts_engine = pyttsx3.init(driverName='sapi5')
        
        voices = self.tts_engine.getProperty('voices')
        if len(voices) > 1:
            # FORCE use female voice (Zira - Index 1)
            self.tts_engine.setProperty('voice', voices[1].id)
            print(f"✅ Selected FEMALE voice: {voices[1].name}")
        
        self.tts_engine.setProperty('rate', 180)
        self.tts_engine.setProperty('volume', 1.0)
        print("✅ TTS configured successfully")
        
    except Exception as e:
        print(f"❌ TTS setup error: {e}")