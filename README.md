Here’s a comprehensive README for your project:

---

# AI Voice Assistant

An intelligent voice assistant that listens to user input, transcribes it using AssemblyAI, generates responses using OpenAI's Chat API, and speaks the responses back using ElevenLabs. Designed to provide concise and resourceful answers in a conversational style.

## Features
- **Speech Recognition**: Captures user voice input via a microphone.
- **Transcription**: Transcribes audio input into text using AssemblyAI.
- **AI Chat**: Generates intelligent and concise responses using OpenAI's GPT model.
- **Text-to-Speech**: Converts AI-generated responses into speech using ElevenLabs.
- **Interactive Conversation**: Maintains a conversation history for context-aware responses.

## Installation

### Prerequisites
1. Python 3.7+
2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```
3. Environment variables for API keys:
   - `ASSEMBLYAI_API_KEY`: Your AssemblyAI API key.
   - `OPENAI_API_KEY`: Your OpenAI API key.
   - `ELEVENLABS_API_KEY`: Your ElevenLabs API key.

### Required Libraries
Add these to your `requirements.txt` file:
```plaintext
assemblyai
openai
requests
speechrecognition
pydub
```

### Setup Environment Variables
Create a `.env` file in the project directory and add your API keys:
```plaintext
ASSEMBLYAI_API_KEY=your_assemblyai_key
OPENAI_API_KEY=your_openai_key
ELEVENLABS_API_KEY=your_elevenlabs_key
```

## Usage

1. **Run the Assistant**:
   ```bash
   python main.py
   ```
2. **Interact**:
   - Speak into the microphone when prompted.
   - Say "exit," "quit," or "bye" to end the session.

## File Structure
- `main.py`: Contains the `AI_Assistant` class and main execution logic.
- `.env`: Stores API keys (excluded from version control).
- `requirements.txt`: Lists required Python libraries.

## How It Works
1. **Listening**:
   - Captures your voice through the microphone using `speech_recognition`.
2. **Transcription**:
   - Sends the audio to AssemblyAI to transcribe it into text.
3. **Chat Completion**:
   - Uses OpenAI's GPT model to generate responses based on the conversation history.
4. **Audio Response**:
   - Converts the AI's response into speech using ElevenLabs and plays it back.

## Configuration
- **Voice Settings**: Customize the ElevenLabs voice by modifying:
  ```python
  "voice_settings": {
      "stability": 0.1,
      "similarity_boost": 0.3,
      "style": 0.2
  }
  ```
- **System Prompt**: Adjust the assistant's personality and behavior in:
  ```python
  self.full_transcription = [
      {"role": "system", "content": "You are a college student..."}
  ]
  ```

## Limitations
- Requires an active internet connection for API requests.
- Ensure microphone and audio playback are configured correctly on your system.

## Contributing
Feel free to fork this repository and submit pull requests for improvements or additional features.

## License
This project is licensed under the [MIT License](LICENSE).

## Acknowledgments
- **AssemblyAI** for transcription services.
- **OpenAI** for intelligent chat capabilities.
- **ElevenLabs** for realistic text-to-speech synthesis.

---

