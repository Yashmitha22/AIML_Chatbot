# Voice Assistant Setup and Usage Guide

## Overview
This project contains a voice-activated AI assistant that can listen to your questions and respond using AI APIs. The assistant supports speech-to-text, AI processing, and text-to-speech capabilities.

## Files Included
- `voice_assistant.py` - Basic voice assistant with OpenAI integration
- `advanced_voice_assistant.py` - Enhanced version with multiple API support and better features
- `requirements.txt` - Required Python packages
- `.env` - Environment variables (API keys)

## Setup Instructions

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup API Keys
Edit the `.env` file and add your API key:
```
OPENAI_API_KEY=your_actual_openai_api_key_here
```

To get an OpenAI API key:
1. Go to https://platform.openai.com/
2. Create an account or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy and paste it into the `.env` file

### 3. Install PyAudio (for Windows)
PyAudio might need special installation on Windows:
```bash
pip install pipwin
pipwin install pyaudio
```

## Usage

### Basic Voice Assistant
```bash
python voice_assistant.py
```

### Advanced Voice Assistant
```bash
python advanced_voice_assistant.py
```

## How to Use
1. Run the script
2. Wait for the "Listening for wake word" message
3. Say "Assistant" or "Hey Assistant" followed by your question
4. The assistant will respond with speech

### Example Commands
- "Assistant, what is the weather like?"
- "Assistant, tell me a joke"
- "Assistant, what time is it?"
- "Assistant, what's the date today?"
- "Assistant, explain machine learning"
- "Assistant, stop" (to exit)

## Features

### Basic Assistant
- Wake word activation
- Speech recognition
- OpenAI GPT integration
- Text-to-speech response
- Basic time/date commands

### Advanced Assistant
- Multiple API support
- Conversation history
- Better error handling
- Enhanced voice settings
- More special commands
- Fallback responses when API is unavailable

## Troubleshooting

### Common Issues
1. **Microphone not working**: Check microphone permissions and ensure it's properly connected
2. **Speech recognition errors**: Ensure good audio quality and speak clearly
3. **API errors**: Verify your API key is correct and has sufficient credits
4. **PyAudio installation issues**: Use the pipwin method mentioned above

### Audio Settings
- The assistant adjusts for ambient noise automatically
- Speak clearly and at normal volume
- Ensure your microphone is not muted

## Customization

### Change Wake Word
In the code, modify:
```python
self.wake_word = "your custom wake word"
```

### Adjust Speech Settings
Modify TTS settings in the `setup_tts()` method:
```python
self.tts_engine.setProperty('rate', 150)  # Speech rate
self.tts_engine.setProperty('volume', 0.9)  # Volume level
```

### Add Custom Commands
Add new conditions in the `handle_command()` or `handle_special_commands()` methods.

## API Alternatives
You can also use other AI services by modifying the code:
- Google's Gemini API
- Anthropic's Claude API
- Azure OpenAI
- Local AI models (Ollama, etc.)

## Security Notes
- Keep your API keys secure and never commit them to version control
- The `.env` file is included in `.gitignore` by default
- Monitor your API usage to avoid unexpected charges

## Next Steps
- Add more specialized commands
- Integrate with smart home devices
- Add calendar/reminder functionality
- Implement continuous conversation mode
- Add support for different languages
