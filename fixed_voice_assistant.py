#!/usr/bin/env python3
"""
Fixed Voice Assistant with Working Microphone Device 0
"""
import speech_recognition as sr
import pyttsx3
import os
import time
from dotenv import load_dotenv

class FixedVoiceAssistant:
    def __init__(self):
        load_dotenv()
        
        # Use the working microphone device 0
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(device_index=0)  # Fixed to working microphone
        
        # Setup TTS with female voice
        self.tts_engine = pyttsx3.init(driverName='sapi5')
        voices = self.tts_engine.getProperty('voices')
        if len(voices) > 1:
            self.tts_engine.setProperty('voice', voices[1].id)  # Female voice (Zira)
            print(f"Selected voice: {voices[1].name}")
        self.tts_engine.setProperty('rate', 180)
        self.tts_engine.setProperty('volume', 1.0)
        
        print("Fixed Voice Assistant initialized with working microphone!")
    
    def speak(self, text):
        print(f"Pari: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def listen(self):
        try:
            with self.microphone as source:
                print("Listening... (Speak now)")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=10)
            
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.WaitTimeoutError:
            print("Timeout - no speech detected")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except Exception as e:
            print(f"Listen error: {e}")
            return None
    
    def run_test(self):
        self.speak("Hello! I am Pari with the fixed microphone. Say something to test.")
        
        test_count = 0
        while test_count < 5:  # Limit tests
            user_input = self.listen()
            if user_input:
                if 'stop' in user_input or 'quit' in user_input:
                    self.speak("Goodbye!")
                    break
                elif 'pari' in user_input:
                    self.speak("Yes! I heard you say Pari! The microphone is working perfectly!")
                    break
                elif 'hello' in user_input:
                    self.speak("Hello! Great to hear you clearly!")
                elif 'test' in user_input:
                    self.speak("Test successful! I can hear and understand you!")
                else:
                    self.speak(f"I heard you say: {user_input}")
                test_count += 1
            else:
                print("No speech detected, trying again...")
                test_count += 1
        
        self.speak("Microphone test complete!")

if __name__ == "__main__":
    print("Starting Fixed Voice Assistant...")
    assistant = FixedVoiceAssistant()
    assistant.run_test()
