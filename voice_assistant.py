import speech_recognition as sr
import pyttsx3
import openai
from dotenv import load_dotenv
import os
import time
import threading
from typing import Optional

class VoiceAssistant:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self.setup_tts()
        
        # Initialize OpenAI client
        self.setup_openai()
        
        # Assistant state
        self.is_listening = False
        self.wake_word = "assistant"  # You can change this
        
    def setup_tts(self):
        """Configure text-to-speech settings"""
        voices = self.tts_engine.getProperty('voices')
        # Set voice (0 for male, 1 for female typically)
        if len(voices) > 1:
            self.tts_engine.setProperty('voice', voices[1].id)  # Female voice
        
        # Set speech rate (words per minute)
        self.tts_engine.setProperty('rate', 150)
        
        # Set volume (0.0 to 1.0)
        self.tts_engine.setProperty('volume', 0.9)
    
    def setup_openai(self):
        """Setup OpenAI API client"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'your_openai_api_key_here':
            print("⚠️  Please set your OpenAI API key in the .env file")
            self.openai_client = None
        else:
            self.openai_client = openai.OpenAI(api_key=api_key)
            print("✅ OpenAI API initialized successfully")
    
    def speak(self, text: str):
        """Convert text to speech"""
        print(f"🤖 Assistant: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def listen_for_wake_word(self) -> bool:
        """Listen for the wake word"""
        try:
            with self.microphone as source:
                print(f"👂 Listening for wake word '{self.wake_word}'...")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
            
            # Recognize speech
            text = self.recognizer.recognize_google(audio).lower()
            print(f"👤 Heard: {text}")
            
            return self.wake_word in text
            
        except sr.WaitTimeoutError:
            return False
        except sr.UnknownValueError:
            return False
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
            return False
    
    def listen_for_command(self) -> Optional[str]:
        """Listen for user command after wake word"""
        try:
            with self.microphone as source:
                print("🎤 Listening for your question...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
            
            # Recognize speech
            text = self.recognizer.recognize_google(audio)
            print(f"👤 You said: {text}")
            return text
            
        except sr.WaitTimeoutError:
            self.speak("I didn't hear anything. Please try again.")
            return None
        except sr.UnknownValueError:
            self.speak("Sorry, I couldn't understand what you said.")
            return None
        except sr.RequestError as e:
            self.speak("Sorry, there was an error with speech recognition.")
            print(f"❌ Speech recognition error: {e}")
            return None
    
    def get_ai_response(self, question: str) -> str:
        """Get response from AI API"""
        if not self.openai_client:
            return "Sorry, the AI service is not configured. Please check your API key."
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful voice assistant. Keep your responses concise and conversational, suitable for speech. Limit responses to 2-3 sentences unless specifically asked for more detail."},
                    {"role": "user", "content": question}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"❌ OpenAI API error: {e}")
            return "Sorry, I encountered an error while processing your request."
    
    def handle_command(self, command: str):
        """Process user command and respond"""
        command_lower = command.lower()
        
        # Handle special commands
        if any(word in command_lower for word in ['stop', 'exit', 'quit', 'goodbye']):
            self.speak("Goodbye! Have a great day!")
            return False
        
        elif 'time' in command_lower:
            current_time = time.strftime("%I:%M %p")
            self.speak(f"The current time is {current_time}")
            
        elif 'date' in command_lower:
            current_date = time.strftime("%B %d, %Y")
            self.speak(f"Today is {current_date}")
            
        else:
            # Get AI response for general questions
            self.speak("Let me think about that...")
            response = self.get_ai_response(command)
            self.speak(response)
        
        return True
    
    def run(self):
        """Main loop for the voice assistant"""
        self.speak("Hello! I'm your voice assistant. Say 'assistant' followed by your question to get started.")
        print(f"🚀 Voice Assistant is running. Say '{self.wake_word}' to activate.")
        print("💡 Try saying: 'Assistant, what is the weather like?' or 'Assistant, tell me a joke'")
        print("🛑 Say 'stop', 'exit', or 'quit' to end the session.\n")
        
        try:
            while True:
                # Listen for wake word
                if self.listen_for_wake_word():
                    self.speak("Yes, how can I help you?")
                    
                    # Listen for command
                    command = self.listen_for_command()
                    
                    if command:
                        # Process command
                        continue_running = self.handle_command(command)
                        if not continue_running:
                            break
                    
                    # Brief pause before listening again
                    time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 Voice Assistant stopped by user")
            self.speak("Goodbye!")

def main():
    """Main function to run the voice assistant"""
    assistant = VoiceAssistant()
    assistant.run()

if __name__ == "__main__":
    main()
