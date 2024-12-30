import os
import assemblyai as aai
import openai
import requests
import speech_recognition as sr
from io import BytesIO
import time

class AI_Assistant:
    def __init__(self):
        # API keys from environment variables
        aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

        # Voice settings
        self.voice_id = "ytqZwNZlrJjetYyjllP1"

        # Speech recognizer
        self.recognizer = sr.Recognizer()

        # Initial system prompt
        self.full_transcription = [
            {"role": "system", "content": "You are a college student who is resourceful, efficient, and keeps answers concise."},
        ]

    def listen(self):
        """
        Capture and transcribe user speech using AssemblyAI.
        """
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)

        try:
            print("Recognizing speech...")
            audio_data = audio.get_wav_data()

            # Upload audio to AssemblyAI
            headers = {'authorization': aai.settings.api_key}
            response = requests.post(
                'https://api.assemblyai.com/v2/upload',
                headers=headers,
                data=audio_data
            )
            response.raise_for_status()
            audio_url = response.json()['upload_url']

            # Request transcription
            transcript_response = requests.post(
                'https://api.assemblyai.com/v2/transcript',
                headers=headers,
                json={'audio_url': audio_url}
            )
            transcript_response.raise_for_status()
            transcript_id = transcript_response.json()['id']

            # Poll for transcription result with exponential backoff
            delay = 1
            while True:
                transcript_result = requests.get(
                    f'https://api.assemblyai.com/v2/transcript/{transcript_id}',
                    headers=headers
                )
                transcript_result.raise_for_status()
                result_json = transcript_result.json()
                if result_json['status'] == 'completed':
                    transcript = result_json['text']
                    print(f"You said: {transcript}")
                    return transcript
                elif result_json['status'] == 'failed':
                    raise Exception("Transcription failed")
                time.sleep(delay)
                delay = min(delay * 2, 30)  # Cap delay at 30 seconds
        except Exception as e:
            print(f"Failed to recognize speech: {e}")
            return None

    def chat(self):
        """
        Engage in a chat conversation using OpenAI's Chat API.
        """
        print("AI Assistant: Nice to meet you! My name is Aiden, and I am your Voice Assistant. How may I assist you?")
        while True:
            user_input = self.listen()
            if user_input is None:
                continue

            if user_input.lower() in ["exit", "quit", "bye"]:
                print("AI Assistant: Goodbye!")
                break

            self.full_transcription.append({"role": "user", "content": user_input})

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=self.full_transcription
                )
                ai_text = response.choices[0].message['content']
                print(f"AI Assistant: {ai_text}")
                self.generate_audio(ai_text)
            except Exception as e:
                print(f"An error occurred: {e}")

    def generate_audio(self, text):
        """
        Generate audio using ElevenLabs API.
        """
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
            headers = {
                "xi-api-key": self.elevenlabs_api_key,
                "Content-Type": "application/json"
            }
            data = {
                "text": text,
                "voice_settings": {
                    "stability": 0.1,
                    "similarity_boost": 0.3,
                    "style": 0.2
                }
            }
            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                audio_buffer = BytesIO(response.content)

                # Play the audio using pydub
                from pydub import AudioSegment
                from pydub.playback import play
                audio_segment = AudioSegment.from_file(audio_buffer, format="mp3")
                play(audio_segment)
            else:
                print(f"Failed to generate audio: {response.status_code} {response.text}")
        except Exception as e:
            print(f"Failed to generate audio: {e}")


if __name__ == "__main__":
    ai_assistant = AI_Assistant()
    ai_assistant.chat()
