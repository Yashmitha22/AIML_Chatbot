#!/usr/bin/env python3
"""
Simple voice test to check if TTS is audible
"""
import pyttsx3
import time

def test_voice():
    print("🔊 Testing voice output...")
    
    # Initialize TTS engine
    tts_engine = pyttsx3.init()
    
    # Configure voice
    voices = tts_engine.getProperty('voices')
    if len(voices) > 1:
        # Use Zira (female voice)
        tts_engine.setProperty('voice', voices[1].id)
        print(f"✅ Using voice: {voices[1].name}")
    
    # Set properties for maximum audibility
    tts_engine.setProperty('rate', 150)  # Slower rate for clarity
    tts_engine.setProperty('volume', 1.0)  # Maximum volume
    
    # Test messages
    test_messages = [
        "Hello! This is a voice test.",
        "Can you hear me clearly?", 
        "I am Pari, your voice assistant.",
        "If you can hear this, your voice output is working perfectly!"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n🎤 Test {i}: {message}")
        tts_engine.say(message)
        tts_engine.runAndWait()
        print("✅ Speech completed")
        time.sleep(1)
    
    print("\n🎯 Voice test completed!")
    print("📢 If you heard all 4 messages, your TTS is working correctly!")

if __name__ == "__main__":
    test_voice()
