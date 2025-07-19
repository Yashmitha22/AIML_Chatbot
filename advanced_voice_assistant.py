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
        self.wake_word = "Pari"
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
    
    def listen_with_timeout(self, timeout: int = 2, phrase_time_limit: int = 8) -> Optional[str]:
        """Enhanced listening with better error handling"""
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                # Shorter ambient noise adjustment for faster response
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
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
                {"role": "system", "content": "You are Pari, a friendly and helpful voice assistant. Keep responses concise and conversational, suitable for speech. Always be warm and personable. Limit responses to 2-3 sentences unless asked for more detail. Always respond as if you're speaking out loud to the user."}
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
    

    def process_question(self, question: str) -> str:
        """Process question using available APIs or fallback"""
        # Always try local responses first for better reliability
        local_response = self.try_local_response(question)
        if local_response:
            return local_response
        
        # If no local response found, try API
        if self.apis['openai']['available']:
            try:
                return self.get_openai_response(question)
            except Exception as e:
                print(f"❌ API failed, using fallback: {e}")
                return self.get_fallback_response(question)
        else:
            return self.get_fallback_response(question)
    
    def try_local_response(self, question: str) -> Optional[str]:
        """Try to find a local response for common questions"""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! I'm Pari, your voice assistant. How can I help you today?"
        
        elif any(word in question_lower for word in ['how are you', 'how do you do']):
            return "I'm doing wonderful, thank you for asking! I'm excited to help you. How are you doing?"
        
        elif 'weather' in question_lower:
            return "I don't have access to current weather data right now, but I recommend checking your local weather app or asking about a specific location online."
        
        elif any(word in question_lower for word in ['joke', 'funny', 'tell me a joke']):
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the scarecrow win an award? He was outstanding in his field!",
                "Why don't eggs tell jokes? They'd crack each other up!",
                "What do you call a fake noodle? An impasta!",
                "Why did the math book look so sad? Because it had too many problems!",
                "What do you call a bear with no teeth? A gummy bear!",
                "Why don't programmers like nature? It has too many bugs!"
            ]
            import random
            return random.choice(jokes)
        
        elif any(word in question_lower for word in ['thank you', 'thanks']):
            return "You're very welcome! I'm always happy to help. Is there anything else you'd like to know?"
        
        elif any(word in question_lower for word in ['name', 'who are you', 'what is your name']):
            return "I'm Pari, your personal voice assistant! I'm here to help answer your questions, tell jokes, give you the time and date, and have conversations with you."
        
        elif any(word in question_lower for word in ['what can you do', 'help', 'capabilities']):
            return "I can tell you the time and date, share jokes, answer questions, and have conversations with you! Just say Pari followed by what you need."
        
        elif any(word in question_lower for word in ['good morning', 'good afternoon', 'good evening']):
            current_hour = int(time.strftime("%H"))
            if current_hour < 12:
                return "Good morning! I hope you're having a wonderful start to your day. How can I assist you?"
            elif current_hour < 18:
                return "Good afternoon! It's lovely to hear from you. What can I help you with today?"
            else:
                return "Good evening! I hope you've had a great day. How can I help you tonight?"
        
        return None
    
    def get_fallback_response(self, question: str) -> str:
        """Fallback response when no other options work"""
        return "I'm sorry, I don't have access to that information right now. But I can help with basic questions, tell jokes, give you the time and date, or just chat with you!"
    
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
        self.speak("Hello! I'm Pari, your advanced voice assistant. I'm ready to help you with anything you need!")
        print(f"🚀 Voice Assistant 'Pari' is running!")
        print(f"💬 Say '{self.wake_word}' followed by your question")
        print("🔧 Special commands: 'time', 'date', 'clear history', 'stop'")
        print("🛑 Say 'Pari stop' or 'Pari quit' to exit\n")
        
        try:
            while True:
                # Listen for wake word + command in one go
                user_input = self.listen_with_timeout(timeout=3, phrase_time_limit=15)
                
                if user_input:
                    user_input_lower = user_input.lower()
                    print(f"🔍 Checking for wake word in: '{user_input_lower}'")
                    
                    # Define wake words based on the set wake_word
                    wake_words = [self.wake_word.lower(), f'hey {self.wake_word.lower()}']
                    wake_found = False
                    command = ""
                    
                    # Check if any wake word is present
                    for wake in wake_words:
                        if wake in user_input_lower:
                            wake_found = True
                            # Extract command after wake word
                            if wake in user_input_lower:
                                parts = user_input_lower.split(wake, 1)
                                if len(parts) > 1:
                                    command = parts[1].strip()
                                else:
                                    command = ""
                            break
                    
                    if wake_found:
                        print(f"✅ Wake word detected! Command: '{command}'")
                        print("🛑 Stopped listening - Processing your request...")
                        
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
                        
                        print("👂 Ready to listen again...")
                        
                    else:
                        print("⚠️  Wake word not detected. Try saying 'Pari' or 'Hey Pari' first.")
                
                # Brief pause before listening again
                time.sleep(0.5)
                
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
