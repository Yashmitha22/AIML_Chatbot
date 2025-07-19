#!/usr/bin/env python3
"""
Alternative Voice Assistant with Multiple API Support
This version supports different AI services and has additional features.
"""

import speech_recognition as sr
import pyttsx3
import requests
import json
from dotenv import load_dotenv
import os
import time
from typing import Optional, Dict, Any

class AdvancedVoiceAssistant:
    def __init__(self):
        load_dotenv()
        
        # Initialize speech components
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        
        # Setup TTS
        self.setup_tts()
        
        # API configurations
        self.setup_apis()
        
        # Assistant settings
        self.wake_word = "hey assistant"
        self.conversation_history = []
        
    def setup_tts(self):
        """Configure text-to-speech with better settings"""
        voices = self.tts_engine.getProperty('voices')
        if len(voices) > 0:
            # Try to find a female voice
            for i, voice in enumerate(voices):
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            else:
                self.tts_engine.setProperty('voice', voices[0].id)
        
        self.tts_engine.setProperty('rate', 180)
        self.tts_engine.setProperty('volume', 0.8)
    
    def setup_apis(self):
        """Setup multiple API options"""
        self.apis = {
            'openai': {
                'key': os.getenv('OPENAI_API_KEY'),
                'available': False
            },
            'google': {
                'key': os.getenv('GOOGLE_API_KEY'),
                'available': False
            }
        }
        
        # Check which APIs are available
        for api_name, config in self.apis.items():
            if config['key'] and config['key'] != f'your_{api_name}_api_key_here':
                config['available'] = True
                print(f"✅ {api_name.upper()} API configured")
            else:
                print(f"⚠️  {api_name.upper()} API not configured")
    
    def speak(self, text: str):
        """Enhanced speak function with better formatting"""
        # Clean up text for better speech
        text = text.replace('*', '').replace('#', '').replace('`', '')
        print(f"🤖 Assistant: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def listen_with_timeout(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """Enhanced listening with better error handling"""
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                # Dynamic ambient noise adjustment
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                # Listen with specified timeout
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            
            # Try to recognize speech
            text = self.recognizer.recognize_google(audio)
            print(f"👤 You said: {text}")
            return text.strip()
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("🔇 Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
            self.speak("Sorry, I'm having trouble with speech recognition.")
            return None
    
    def get_openai_response(self, question: str) -> str:
        """Get response from OpenAI API"""
        try:
            import openai
            client = openai.OpenAI(api_key=self.apis['openai']['key'])
            
            # Add context from conversation history
            messages = [
                {"role": "system", "content": "You are a helpful voice assistant. Keep responses concise and conversational. Limit to 2-3 sentences unless asked for more detail."}
            ]
            
            # Add recent conversation history
            for msg in self.conversation_history[-4:]:  # Last 4 exchanges
                messages.extend(msg)
            
            messages.append({"role": "user", "content": question})
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=200,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content.strip()
            
            # Store conversation
            self.conversation_history.append([
                {"role": "user", "content": question},
                {"role": "assistant", "content": answer}
            ])
            
            return answer
            
        except Exception as e:
            print(f"❌ OpenAI API error: {e}")
            return "I'm sorry, I encountered an error while processing your request."
    
    def get_local_response(self, question: str) -> str:
        """Fallback responses when no API is available"""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! How can I help you today?"
        
        elif any(word in question_lower for word in ['how are you', 'how do you do']):
            return "I'm doing well, thank you for asking! How are you?"
        
        elif 'weather' in question_lower:
            return "I don't have access to weather data right now, but you can check your local weather app or website."
        
        elif 'joke' in question_lower:
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the scarecrow win an award? He was outstanding in his field!",
                "Why don't eggs tell jokes? They'd crack each other up!"
            ]
            import random
            return random.choice(jokes)
        
        elif any(word in question_lower for word in ['thank you', 'thanks']):
            return "You're welcome! Is there anything else I can help you with?"
        
        else:
            return "I'm sorry, I don't have access to external information right now. Please make sure your API key is configured for more advanced responses."
    
    def process_question(self, question: str) -> str:
        """Process question using available APIs or fallback"""
        if self.apis['openai']['available']:
            return self.get_openai_response(question)
        else:
            return self.get_local_response(question)
    
    def handle_special_commands(self, command: str) -> tuple[bool, bool]:
        """Handle special commands. Returns (should_continue, was_special_command)"""
        command_lower = command.lower()
        
        if any(word in command_lower for word in ['stop', 'exit', 'quit', 'goodbye', 'bye']):
            self.speak("Goodbye! It was nice talking with you!")
            return False, True
        
        elif any(word in command_lower for word in ['time', 'what time']):
            current_time = time.strftime("%I:%M %p")
            self.speak(f"The current time is {current_time}")
            return True, True
        
        elif any(word in command_lower for word in ['date', 'what date', 'today']):
            current_date = time.strftime("%A, %B %d, %Y")
            self.speak(f"Today is {current_date}")
            return True, True
        
        elif 'clear history' in command_lower:
            self.conversation_history = []
            self.speak("I've cleared our conversation history.")
            return True, True
        
        return True, False
    
    def run(self):
        """Main assistant loop"""
        self.speak("Hello! I'm your advanced voice assistant. I'm ready to help you.")
        print(f"🚀 Voice Assistant is running!")
        print(f"💬 Say '{self.wake_word}' followed by your question")
        print("🔧 Special commands: 'time', 'date', 'clear history', 'stop'")
        print("🛑 Say 'stop' or 'quit' to exit\n")
        
        try:
            while True:
                # Listen for wake word + command in one go
                user_input = self.listen_with_timeout(timeout=1, phrase_time_limit=15)
                
                if user_input:
                    user_input_lower = user_input.lower()
                    
                    # Check if wake word is present
                    if any(wake in user_input_lower for wake in [self.wake_word, 'assistant', 'hey assistant']):
                        # Extract command after wake word
                        command = user_input_lower
                        for wake in [self.wake_word, 'assistant', 'hey assistant']:
                            if wake in command:
                                command = command.split(wake, 1)[-1].strip()
                                break
                        
                        if command:
                            # Handle special commands
                            should_continue, was_special = self.handle_special_commands(command)
                            
                            if not should_continue:
                                break
                            
                            if not was_special:
                                # Process as regular question
                                print("🤔 Processing your question...")
                                response = self.process_question(command)
                                self.speak(response)
                        else:
                            self.speak("Yes, how can I help you?")
                
                # Brief pause to prevent excessive CPU usage
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n🛑 Voice Assistant stopped by user")
            self.speak("Goodbye!")

def main():
    """Main function"""
    print("🎙️  Advanced Voice Assistant")
    print("=" * 50)
    assistant = AdvancedVoiceAssistant()
    assistant.run()

if __name__ == "__main__":
    main()
