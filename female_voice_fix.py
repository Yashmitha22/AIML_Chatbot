#!/usr/bin/env python3
"""
Alternative Female Voice Solution
"""
import pyttsx3
import time
import os

def try_female_voice():
    print("🎭 Trying Alternative Female Voice Setup")
    print("=" * 40)
    
    # Method 1: Force reinitialize for each voice test
    print("Method 1: Force reinitialization...")
    
    try:
        # Create new TTS instance specifically for female voice
        tts_engine = pyttsx3.init(driverName='sapi5')
        voices = tts_engine.getProperty('voices')
        
        if len(voices) > 1:
            # Force set female voice with different approach
            tts_engine.setProperty('voice', voices[1].id)
            tts_engine.setProperty('rate', 100)  # Very slow
            tts_engine.setProperty('volume', 1.0)
            
            # Try multiple test phrases
            test_phrases = [
                "Hello",
                "Testing female voice",
                "I am Pari"
            ]
            
            for phrase in test_phrases:
                print(f"🔊 Testing: '{phrase}'")
                tts_engine.say(phrase)
                tts_engine.runAndWait()
                time.sleep(1)
                
                heard = input(f"Did you hear '{phrase}' in female voice? (y/n): ").strip().lower()
                if heard in ['y', 'yes']:
                    print("✅ SUCCESS! Female voice is working!")
                    return True
            
            print("❌ Method 1 failed")
        
        # Method 2: Try Windows SAPI directly
        print("\nMethod 2: Windows SAPI direct...")
        import win32com.client
        
        try:
            sapi = win32com.client.Dispatch("SAPI.SpVoice")
            voices = sapi.GetVoices()
            
            for i in range(voices.Count):
                voice = voices.Item(i)
                if 'zira' in voice.GetDescription().lower():
                    print(f"Found Zira via SAPI: {voice.GetDescription()}")
                    sapi.Voice = voice
                    sapi.Speak("Hello, I am Pari with SAPI female voice")
                    
                    heard = input("Did you hear SAPI female voice? (y/n): ").strip().lower()
                    if heard in ['y', 'yes']:
                        print("✅ SUCCESS! SAPI female voice works!")
                        return True
            
            print("❌ Method 2 failed")
        
        except ImportError:
            print("❌ win32com not available - install with: pip install pywin32")
        except Exception as e:
            print(f"❌ SAPI error: {e}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Method 3: Use male voice but modify it
    print("\nMethod 3: Use available male voice (David)...")
    try:
        tts_engine = pyttsx3.init()
        tts_engine.setProperty('voice', voices[0].id)  # David
        tts_engine.setProperty('rate', 200)  # Faster for more feminine sound
        tts_engine.setProperty('volume', 1.0)
        
        print("🔊 Using David voice with modified settings...")
        tts_engine.say("Hello, I am Pari, your voice assistant")
        tts_engine.runAndWait()
        
        heard = input("Is this voice acceptable for now? (y/n): ").strip().lower()
        if heard in ['y', 'yes']:
            print("✅ Using David voice as workaround!")
            print("Voice Index: 0")
            print("Voice ID:", voices[0].id)
            return True
    
    except Exception as e:
        print(f"❌ Method 3 error: {e}")
    
    return False

if __name__ == "__main__":
    success = try_female_voice()
    if not success:
        print("\n🔧 SOLUTIONS TO TRY:")
        print("1. Restart Windows")
        print("2. Check Windows Settings > Time & Language > Speech")
        print("3. Try: sfc /scannow in admin command prompt")
        print("4. Reinstall Windows Speech Platform")
