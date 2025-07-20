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
        self.is_awake = False  # State to track if assistant is active
        
    def setup_tts(self):
        """Configure text-to-speech with better settings"""
        try:
            # Force reinitialize TTS for female voice
            self.tts_engine = pyttsx3.init(driverName='sapi5')
            
            voices = self.tts_engine.getProperty('voices')
            print(f"🔊 Found {len(voices)} voice(s)")
            
            if len(voices) > 1:
                # FORCE use female voice (Zira - Index 1)
                self.tts_engine.setProperty('voice', voices[1].id)
                print(f"✅ Selected FEMALE voice: {voices[1].name}")
            else:
                print("❌ Female voice not available, using default")
            
            # Set speech properties for clear female voice
            self.tts_engine.setProperty('rate', 180)
            self.tts_engine.setProperty('volume', 1.0)  # Maximum volume
            print("✅ TTS configured successfully")
            
        except Exception as e:
            print(f"❌ TTS setup error: {e}")
            # Fallback initialization
            try:
                self.tts_engine = pyttsx3.init()
                voices = self.tts_engine.getProperty('voices')
                if len(voices) > 1:
                    self.tts_engine.setProperty('voice', voices[1].id)  # Force female
                self.tts_engine.setProperty('rate', 180)
                self.tts_engine.setProperty('volume', 1.0)
                print("✅ TTS reinitialized with female voice")
            except Exception as e2:
                print(f"❌ TTS reinit failed: {e2}")
    
    def setup_apis(self):
        """Setup multiple API options"""
        # Check for Gemini API key first (preferred name)
        gemini_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        
        self.apis = {
            'openai': {
                'key': os.getenv('OPENAI_API_KEY'),
                'available': False
            },
            'google': {
                'key': gemini_key,
                'available': False
            }
        }
        
        # Check which APIs are available
        for api_name, config in self.apis.items():
            if config['key'] and config['key'] != f'your_{api_name}_api_key_here':
                config['available'] = True
                if api_name == 'google':
                    print(f"✅ Google Gemini API configured")
                else:
                    print(f"✅ {api_name.upper()} API configured")
            else:
                if api_name == 'google':
                    print(f"⚠️  Google Gemini API not configured")
                else:
                    print(f"⚠️  {api_name.upper()} API not configured")
    
    def speak(self, text: str):
        """Enhanced speak function with better formatting and reliability"""
        if not text:
            return
            
        # Clean up text for better speech
        text = text.replace('*', '').replace('#', '').replace('`', '')
        text = text.replace('\\n', ' ').replace('\\t', ' ')
        text = text.replace('_', ' ').replace('-', ' ')
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        print(f"🤖 Pari: {text}")
        print("🔊 Speaking now...")  # Clear indication that voice is starting
        
        try:
            # Ensure TTS engine is ready
            self.tts_engine.stop()  # Stop any current speech
            time.sleep(0.1)  # Brief pause
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            print("✅ Voice output completed")
            time.sleep(0.2)  # Brief pause after speech
        except Exception as e:
            print(f"❌ Speech error: {e}")
            # Try to reinitialize TTS if there's an error
            try:
                print("🔄 Reinitializing voice engine...")
                self.tts_engine = pyttsx3.init()
                self.setup_tts()
                time.sleep(0.1)
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                print("✅ Voice output completed after reinit")
            except Exception as e2:
                print(f"❌ Voice still failed: {e2}")
                print("🔧 Please check your audio system!")
    
    def listen_with_timeout(self, timeout: int = 3, phrase_time_limit: int = 15) -> Optional[str]:
        """Enhanced listening with better error handling"""
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                # Shorter ambient noise adjustment for faster response
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Listen with specified timeout
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            
            print("🔄 Processing speech...")
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
    
    def get_google_gemini_response(self, question: str) -> str:
        """Get response from Google Gemini API"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.apis['google']['key'])
            
            model = genai.GenerativeModel('gemini-pro')
            
            # Create a conversational prompt
            prompt = f"""You are Pari, a friendly voice assistant. Please respond to this question in a conversational way, as if you're speaking out loud. Keep your response to 2-3 sentences and be warm and helpful.

Question: {question}"""
            
            response = model.generate_content(prompt)
            
            if response.text:
                answer = response.text.strip()
                
                # Store conversation
                self.conversation_history.append([
                    {"role": "user", "content": question},
                    {"role": "assistant", "content": answer}
                ])
                
                print(f"✅ Got Gemini response: {answer[:50]}...")
                return answer
            else:
                return "I'm sorry, I didn't get a proper response from the AI service."
            
        except Exception as e:
            print(f"❌ Google Gemini API error: {e}")
            return "I'm sorry, I had trouble connecting to the Google Gemini service."

    def process_question(self, question: str) -> str:
        """Process question using available APIs or fallback"""
        # Always try local responses first for better reliability
        local_response = self.try_local_response(question)
        if local_response:
            return local_response
        
        # If no local response found, try APIs in order of preference
        if self.apis['google']['available']:
            try:
                return self.get_google_gemini_response(question)
            except Exception as e:
                print(f"❌ Google API failed, trying OpenAI: {e}")
        
        if self.apis['openai']['available']:
            try:
                return self.get_openai_response(question)
            except Exception as e:
                print(f"❌ OpenAI API failed, using fallback: {e}")
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
        
        if any(word in command_lower for word in ['stop listening', 'go to sleep', 'cancel']):
            self.is_awake = False
            self.speak("Okay, I'll go back to sleep. Just say my name if you need me.")
            return True, True
        
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
        """Main assistant loop with improved two-step listening"""
        self.speak(f"Hello! I'm {self.wake_word}, your voice assistant. You can say my name followed by your question, or just say my name first and then ask.")
        print(f"🚀 Voice Assistant '{self.wake_word}' is running!")
        print(f"💬 Two ways to use me:")
        print(f"   1. Say '{self.wake_word}' then wait, then ask your question")
        print(f"   2. Say '{self.wake_word}, what is your name?' (all at once)")
        print("🛑 Say 'Pari stop' or 'Pari quit' to exit\n")
        
        try:
            while True:
                if not self.is_awake:
                    # 1. Listen for wake word
                    print(f"👂 Listening for wake word '{self.wake_word}'...")
                    user_input = self.listen_for_wake_word()
                    if user_input and self.wake_word.lower() in user_input.lower():
                        self.is_awake = True
                        self.speak("Yes, how can I help you?")
                    elif user_input:
                        # Check if they said "Pari" with their question
                        if self.wake_word.lower() in user_input.lower():
                            # Extract the question part after "Pari"
                            question_part = user_input.lower().replace(self.wake_word.lower(), "").strip()
                            if question_part:
                                print(f"🎯 Wake word + question detected: {user_input}")
                                self.speak("Yes, I heard you!")
                                # Process the question immediately
                                response = self.process_question(question_part)
                                if response:
                                    self.speak(response)
                                else:
                                    self.speak("I'm sorry, I couldn't process that question.")
                                continue
                            else:
                                self.is_awake = True
                                self.speak("Yes, how can I help you?")
                        else:
                            # If they said something but not the wake word, check if it might be a question
                            if any(word in user_input.lower() for word in ['what', 'how', 'when', 'where', 'why', 'who', 'tell', 'can']):
                                print(f"📢 Detected question without wake word: {user_input}")
                                self.speak(f"I heard you ask '{user_input}', but please say my name Pari first. Try saying 'Pari, {user_input}'")
                else:
                    # 2. Listen for command
                    print("🎤 Listening for your command...")
                    command = self.listen_for_command()
                    
                    if command:
                        print(f"🎯 Processing command: {command}")
                        # Process the command
                        should_continue, was_special = self.handle_special_commands(command)
                        
                        if not should_continue:
                            break # Exit loop
                        
                        if not was_special:
                            print("🤔 Processing your question...")
                            response = self.process_question(command)
                            print(f"📝 Response ready: {response[:50]}...")
                            if response:
                                self.speak(response)
                            else:
                                self.speak("I'm sorry, I couldn't process that question.")
                        
                        # Stay awake for a bit longer to allow follow-up questions
                        print("💭 Staying awake for follow-up questions...")
                        
                    else:
                        # No command heard, go back to sleep after 2 failed attempts
                        print("🔇 No command heard, going back to sleep...")
                        self.is_awake = False
                        self.speak("I didn't hear anything. Say Pari to wake me up again.")

                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n🛑 Voice Assistant stopped by user")
            self.speak("Goodbye!")

    def listen_for_wake_word(self) -> Optional[str]:
        """Listens specifically for the wake word."""
        return self.listen_with_timeout(timeout=8, phrase_time_limit=5)

    def listen_for_command(self) -> Optional[str]:
        """Listens for a command after being woken up."""
        return self.listen_with_timeout(timeout=8, phrase_time_limit=20)

def main():
    """Main function"""
    print("🎙️  Advanced Voice Assistant")
    print("=" * 50)
    assistant = AdvancedVoiceAssistant()
    assistant.run()

if __name__ == "__main__":
    main()
