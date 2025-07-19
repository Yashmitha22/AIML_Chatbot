"""
Simple Test Script for Voice Assistant Components
Run this to test individual components before using the full voice assistant.
"""

import sys
import os

def test_imports():
    """Test if all required packages are installed"""
    print("🧪 Testing imports...")
    
    try:
        import speech_recognition as sr
        print("✅ speech_recognition - OK")
    except ImportError as e:
        print(f"❌ speech_recognition - FAILED: {e}")
        return False
    
    try:
        import pyttsx3
        print("✅ pyttsx3 - OK")
    except ImportError as e:
        print(f"❌ pyttsx3 - FAILED: {e}")
        return False
    
    try:
        import openai
        print("✅ openai - OK")
    except ImportError as e:
        print(f"❌ openai - FAILED: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv - OK")
    except ImportError as e:
        print(f"❌ python-dotenv - FAILED: {e}")
        return False
    
    try:
        import requests
        print("✅ requests - OK")
    except ImportError as e:
        print(f"❌ requests - FAILED: {e}")
        return False
    
    print("✅ All imports successful!\n")
    return True

def test_tts():
    """Test text-to-speech"""
    print("🧪 Testing text-to-speech...")
    
    try:
        import pyttsx3
        engine = pyttsx3.init()
        
        # Get available voices
        voices = engine.getProperty('voices')
        print(f"📢 Found {len(voices)} voice(s):")
        for i, voice in enumerate(voices):
            print(f"  {i}: {voice.name} ({voice.id})")
        
        # Test speech
        print("🎵 Testing speech output...")
        engine.say("Hello! This is a test of the text to speech system.")
        engine.runAndWait()
        print("✅ Text-to-speech test completed!\n")
        return True
        
    except Exception as e:
        print(f"❌ Text-to-speech test failed: {e}\n")
        return False

def test_microphone():
    """Test microphone access"""
    print("🧪 Testing microphone access...")
    
    try:
        import speech_recognition as sr
        
        r = sr.Recognizer()
        mic = sr.Microphone()
        
        # List available microphones
        mic_list = sr.Microphone.list_microphone_names()
        print(f"🎤 Found {len(mic_list)} microphone(s):")
        for i, name in enumerate(mic_list):
            print(f"  {i}: {name}")
        
        # Test microphone access
        with mic as source:
            print("🔧 Adjusting for ambient noise... Please wait.")
            r.adjust_for_ambient_noise(source, duration=2)
        
        print("✅ Microphone test completed!\n")
        return True
        
    except Exception as e:
        print(f"❌ Microphone test failed: {e}\n")
        return False

def test_speech_recognition():
    """Test speech recognition with user input"""
    print("🧪 Testing speech recognition...")
    
    try:
        import speech_recognition as sr
        
        r = sr.Recognizer()
        mic = sr.Microphone()
        
        print("🎤 Please say 'Hello World' when prompted...")
        input("Press Enter when ready to start recording...")
        
        with mic as source:
            print("🔴 Recording... Say 'Hello World' now!")
            audio = r.listen(source, timeout=10, phrase_time_limit=5)
        
        print("🔄 Recognizing speech...")
        text = r.recognize_google(audio)
        print(f"👤 You said: '{text}'")
        
        if 'hello' in text.lower() and 'world' in text.lower():
            print("✅ Speech recognition test passed!\n")
            return True
        else:
            print("⚠️  Speech recognition worked, but didn't detect 'Hello World' exactly.\n")
            return True
            
    except sr.WaitTimeoutError:
        print("❌ Speech recognition test failed: Timeout (no speech detected)\n")
        return False
    except sr.UnknownValueError:
        print("❌ Speech recognition test failed: Could not understand audio\n")
        return False
    except sr.RequestError as e:
        print(f"❌ Speech recognition test failed: {e}\n")
        return False
    except Exception as e:
        print(f"❌ Speech recognition test failed: {e}\n")
        return False

def test_api_key():
    """Test API key configuration"""
    print("🧪 Testing API key configuration...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        openai_key = os.getenv('OPENAI_API_KEY')
        
        if not openai_key:
            print("⚠️  No OPENAI_API_KEY found in .env file")
            return False
        elif openai_key == 'your_openai_api_key_here':
            print("⚠️  Please replace the placeholder OPENAI_API_KEY in .env file with your actual key")
            return False
        elif openai_key.startswith('sk-'):
            print("✅ OpenAI API key format looks correct")
            
            # Test API connection (optional)
            try:
                import openai
                openai.api_key = openai_key
                
                # Simple test call
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": "Say hello"}],
                    max_tokens=5
                )
                print("✅ API key is working!\n")
                return True
                
            except Exception as e:
                print(f"⚠️  API key configured but test call failed: {e}")
                print("   This might be due to insufficient credits or network issues.\n")
                return False
        else:
            print("⚠️  API key format doesn't look like a valid OpenAI key")
            return False
            
    except Exception as e:
        print(f"❌ API key test failed: {e}\n")
        return False

def main():
    """Run all tests"""
    print("🚀 Voice Assistant Component Tests")
    print("=" * 50)
    
    tests = [
        ("Package Imports", test_imports),
        ("Text-to-Speech", test_tts),
        ("Microphone Access", test_microphone),
        ("API Key Configuration", test_api_key),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except KeyboardInterrupt:
            print("\n🛑 Testing interrupted by user")
            return
        except Exception as e:
            print(f"❌ {test_name} failed with unexpected error: {e}")
            results.append((test_name, False))
    
    # Optional speech recognition test
    print("🎤 Optional: Would you like to test speech recognition? (requires speaking)")
    response = input("Type 'y' or 'yes' to test speech recognition: ").lower().strip()
    
    if response in ['y', 'yes']:
        try:
            sr_result = test_speech_recognition()
            results.append(("Speech Recognition", sr_result))
        except KeyboardInterrupt:
            print("\n🛑 Speech recognition test skipped")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your voice assistant should work correctly.")
        print("   You can now run: python voice_assistant.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above and:")
        print("   1. Make sure all packages are installed: pip install -r requirements.txt")
        print("   2. Check your .env file has the correct API key")
        print("   3. Ensure your microphone is working and permissions are granted")

if __name__ == "__main__":
    main()
