import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def convert_audio_to_text(file_path):
    try:
        audio_file = open(file_path, "rb")

        transcript = client.audio.transcriptions.create(
            model="gpt-4o-mini-tts",  # Whisper v3 compatible newer endpoint
            file=audio_file
        )

        return transcript.text

    except Exception as e:
        print("Speech Error:", e)
        return None
