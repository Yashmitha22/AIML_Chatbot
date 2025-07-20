#!/usr/bin/env python3
"""
Microphone Troubleshooting and Fix Tool
"""
import speech_recognition as sr
import pyaudio

def list_all_microphones():
    print("🎤 AVAILABLE MICROPHONES")
    print("=" * 30)
    
    try:
        # List all audio devices
        p = pyaudio.PyAudio()
        print(f"Found {p.get_device_count()} audio devices:")
        
        mic_devices = []
        for i in range(p.get_device_count()):
            try:
                info = p.get_device_info_by_index(i)
                if info['maxInputChannels'] > 0:  # Input device (microphone)
                    mic_devices.append(i)
                    print(f"🎙️  Device {i}: {info['name']}")
                    print(f"    Channels: {info['maxInputChannels']}")
                    print(f"    Sample Rate: {int(info['defaultSampleRate'])} Hz")
                    print()
            except Exception as e:
                print(f"❌ Error reading device {i}: {e}")
        
        p.terminate()
        return mic_devices
        
    except Exception as e:
        print(f"❌ Error listing devices: {e}")
        return []

def test_specific_microphone(device_index):
    print(f"🧪 Testing Microphone {device_index}")
    print("-" * 30)
    
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone(device_index=device_index) as source:
            print(f"✅ Successfully opened microphone {device_index}")
            print("📢 Please be quiet for noise calibration (2 seconds)...")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            
            print("🗣️  Now say 'HELLO TESTING' clearly...")
            print("⏰ You have 8 seconds...")
            
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=5)
            text = recognizer.recognize_google(audio)
            
            print(f"✅ SUCCESS! Heard: '{text}'")
            return True
            
    except sr.WaitTimeoutError:
        print("⏰ Timeout - No speech detected")
    except sr.UnknownValueError:
        print("🔇 Audio detected but couldn't understand speech")
    except Exception as e:
        print(f"❌ Error with microphone {device_index}: {e}")
    
    return False

def find_working_microphone():
    print("🔍 FINDING WORKING MICROPHONE")
    print("=" * 35)
    
    mic_devices = list_all_microphones()
    
    if not mic_devices:
        print("❌ No microphone devices found!")
        return None
    
    print("Testing each microphone...")
    print()
    
    for device_index in mic_devices:
        if test_specific_microphone(device_index):
            print(f"🎉 WORKING MICROPHONE FOUND: Device {device_index}")
            return device_index
        print()
    
    return None

def create_fixed_voice_assistant(working_mic_index):
    """Create a version of voice assistant with the working microphone"""
    
    fixed_code = f'''#!/usr/bin/env python3
"""
Fixed Voice Assistant with Working Microphone
"""
import speech_recognition as sr
import pyttsx3
import os
import time
from dotenv import load_dotenv

class FixedVoiceAssistant:
    def __init__(self):
        load_dotenv()
        
        # Use the working microphone device
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(device_index={working_mic_index})  # Fixed microphone
        
        # Setup TTS with female voice
        self.tts_engine = pyttsx3.init(driverName='sapi5')
        voices = self.tts_engine.getProperty('voices')
        if len(voices) > 1:
            self.tts_engine.setProperty('voice', voices[1].id)  # Female voice
        self.tts_engine.setProperty('rate', 180)
        self.tts_engine.setProperty('volume', 1.0)
        
        print("✅ Fixed Voice Assistant initialized with working microphone!")
    
    def speak(self, text):
        print(f"🤖 Pari: {{text}}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def listen(self):
        try:
            with self.microphone as source:
                print("🎤 Listening... (Speak now)")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=10)
            
            text = self.recognizer.recognize_google(audio)
            print(f"👤 You said: {{text}}")
            return text.lower()
        except Exception as e:
            print(f"❌ Listen error: {{e}}")
            return None
    
    def run_simple_test(self):
        self.speak("Hello! I am Pari with fixed microphone. Say something to test.")
        
        while True:
            user_input = self.listen()
            if user_input:
                if 'stop' in user_input or 'quit' in user_input:
                    self.speak("Goodbye!")
                    break
                elif 'pari' in user_input:
                    self.speak("Yes, I heard you say Pari! The microphone is working!")
                else:
                    self.speak(f"I heard you say: {{user_input}}")
            else:
                print("No speech detected, trying again...")

if __name__ == "__main__":
    assistant = FixedVoiceAssistant()
    assistant.run_simple_test()
'''
    
    with open('fixed_voice_assistant.py', 'w') as f:
        f.write(fixed_code)
    
    print(f"📁 Created 'fixed_voice_assistant.py' with microphone {working_mic_index}")

def main():
    print("🔧 VOICE ASSISTANT MICROPHONE TROUBLESHOOTER")
    print("=" * 50)
    print()
    
    working_mic = find_working_microphone()
    
    if working_mic is not None:
        print(f"✅ SOLUTION FOUND!")
        print(f"Working microphone: Device {working_mic}")
        print()
        
        create_fixed_voice_assistant(working_mic)
        
        print("🎯 NEXT STEPS:")
        print("1. Run: python fixed_voice_assistant.py")
        print("2. Test if you can hear and speak with Pari")
        print("3. If it works, we can apply this fix to your main assistant")
        
    else:
        print("❌ NO WORKING MICROPHONE FOUND")
        print()
        print("🔧 TROUBLESHOOTING STEPS:")
        print("1. Check Windows Sound Settings:")
        print("   - Right-click speaker icon in taskbar")
        print("   - Choose 'Open Sound settings'")
        print("   - Check 'Input' section")
        print("   - Test your microphone there first")
        print()
        print("2. Check microphone permissions:")
        print("   - Windows Settings > Privacy & Security > Microphone")
        print("   - Enable microphone access for desktop apps")
        print()
        print("3. Try different microphone if available")

if __name__ == "__main__":
    main()
