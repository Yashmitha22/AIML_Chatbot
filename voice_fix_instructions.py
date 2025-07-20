#!/usr/bin/env python3
"""
Voice Assistant Fix Instructions
Since female voice (Zira) works, here's what you need to change in your advanced_voice_assistant.py
"""

print("🎯 VOICE ASSISTANT FIX INSTRUCTIONS")
print("=" * 50)
print()

print("✅ GOOD NEWS: Female voice (Zira) works!")
print("✅ Voice Index: 1")
print("✅ Voice Name: Microsoft Zira Desktop - English (United States)")
print()

print("🔧 TO FIX YOUR VOICE ASSISTANT:")
print("=" * 35)
print()

print("1. In your advanced_voice_assistant.py file, find the setup_tts() function")
print()

print("2. Replace the voice selection part with this code:")
print("-" * 50)
print("""
def setup_tts(self):
    \"\"\"Configure text-to-speech with better settings\"\"\"
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
""")
print("-" * 50)
print()

print("3. KEY CHANGES:")
print("   - Add driverName='sapi5' to pyttsx3.init()")
print("   - Force use voices[1] (female voice)")
print("   - Remove the voice search loop")
print()

print("4. Test by running your voice assistant and saying:")
print("   'Pari, what is your name?'")
print()

print("🎉 This should give you the female voice you want!")

# Create the exact replacement code in a separate file for easy copying
replacement_code = '''
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
'''

with open('setup_tts_replacement.txt', 'w') as f:
    f.write(replacement_code)

print("📄 I've also saved the replacement code to 'setup_tts_replacement.txt'")
print("   You can copy from there if needed.")
