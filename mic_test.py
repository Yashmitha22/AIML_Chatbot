#!/usr/bin/env python3
"""
Microphone and Speech Recognition Test
"""
import speech_recognition as sr
import time

def test_microphone():
    print("🎤 MICROPHONE & SPEECH RECOGNITION TEST")
    print("=" * 45)
    
    # Initialize speech recognizer
    recognizer = sr.Recognizer()
    
    # Test microphone access
    print("1. Testing microphone access...")
    try:
        with sr.Microphone() as source:
            print("✅ Microphone found and accessible")
            print(f"🎙️  Default microphone: {source.device_index}")
            
            # Test ambient noise calibration
            print("\n2. Calibrating for ambient noise...")
            print("📢 Please be quiet for 2 seconds...")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            print("✅ Noise calibration complete")
            
            # Test speech recognition multiple times
            for test_num in range(3):
                print(f"\n3.{test_num+1} Speech Recognition Test {test_num+1}/3")
                print("🗣️  Please say 'Pari' clearly...")
                print("⏰ You have 10 seconds...")
                
                try:
                    # Listen for speech
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                    print("🔄 Processing what you said...")
                    
                    # Try to recognize
                    text = recognizer.recognize_google(audio)
                    print(f"✅ SUCCESS! I heard: '{text}'")
                    
                    # Check if it contains "Pari"
                    if 'pari' in text.lower():
                        print("🎉 PERFECT! 'Pari' was detected correctly!")
                        return True
                    else:
                        print("⚠️  I heard you, but didn't detect 'Pari'")
                        
                except sr.WaitTimeoutError:
                    print("⏰ Timeout - No speech detected")
                except sr.UnknownValueError:
                    print("🔇 Could not understand the audio")
                except sr.RequestError as e:
                    print(f"❌ Speech recognition error: {e}")
                
                if test_num < 2:  # Don't wait after the last test
                    print("⏳ Waiting 2 seconds before next test...")
                    time.sleep(2)
            
            print(f"\n📊 TEST SUMMARY:")
            print("If you had trouble, try:")
            print("1. Speak louder and clearer")
            print("2. Check microphone volume in Windows settings")
            print("3. Make sure microphone isn't muted")
            print("4. Try different microphone if available")
            
            return False
            
    except Exception as e:
        print(f"❌ Microphone error: {e}")
        print("\n🔧 TROUBLESHOOTING:")
        print("1. Check if microphone is connected")
        print("2. Check Windows microphone permissions")
        print("3. Test microphone in other applications")
        return False

def test_quick_speech():
    print(f"\n🚀 QUICK PARI TEST")
    print("=" * 20)
    print("🗣️  Say 'Pari' in the next 5 seconds...")
    
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            text = recognizer.recognize_google(audio)
            print(f"Result: '{text}'")
            if 'pari' in text.lower():
                print("✅ SUCCESS! Pari detected!")
            else:
                print("⚠️  Didn't detect Pari")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Starting microphone diagnostic...")
    success = test_microphone()
    
    if not success:
        test_quick_speech()
        
    print(f"\n{'='*50}")
    print("🎯 If all tests passed, your voice assistant should work!")
    print("🎯 If tests failed, fix the microphone issue first.")
