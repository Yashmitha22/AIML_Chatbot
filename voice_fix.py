#!/usr/bin/env python3
"""
Voice Diagnosis and Fix Tool
"""
import pyttsx3
import time

def diagnose_and_fix():
    print("🔧 Voice Diagnosis Tool")
    print("=" * 25)
    
    tts_engine = pyttsx3.init()
    voices = tts_engine.getProperty('voices')
    
    print("Testing each voice individually...")
    
    for i, voice in enumerate(voices):
        print(f"\n🎭 Voice {i}: {voice.name}")
        
        try:
            # Reset engine for each voice
            tts_engine = pyttsx3.init()
            tts_engine.setProperty('voice', voice.id)
            tts_engine.setProperty('rate', 120)  # Very slow
            tts_engine.setProperty('volume', 1.0)  # Max volume
            
            # Test with simple text
            test_text = f"Voice {i} test"
            print(f"🔊 Speaking: '{test_text}'")
            
            tts_engine.say(test_text)
            tts_engine.runAndWait()
            time.sleep(0.5)  # Pause between tests
            
            heard = input(f"Did you hear Voice {i}? (y/n): ").strip().lower()
            if heard in ['y', 'yes']:
                print(f"✅ Voice {i} WORKS: {voice.name}")
                if 'zira' in voice.name.lower():
                    print("🎉 FEMALE VOICE FOUND AND WORKING!")
                    print(f"Use this in your assistant:")
                    print(f"Voice Index: {i}")
                    print(f"Voice ID: {voice.id}")
                    return i, voice.id
            else:
                print(f"❌ Voice {i} not working: {voice.name}")
        
        except Exception as e:
            print(f"❌ Error with Voice {i}: {e}")
    
    print("\n🤔 If no voices worked properly, try:")
    print("1. Restart your computer")
    print("2. Check Windows Speech settings")
    print("3. Update Windows")
    
    return None, None

if __name__ == "__main__":
    diagnose_and_fix()
