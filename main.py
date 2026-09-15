from dataclasses import dataclass
from music_generator import MusicGenerator

'''
Defaults:

    - TTS Model: pyttsx3
    - TTS Model Voices:
        - pyttsx3:
            - gmw/en-us
        - kokoro:
            af_heart
'''


@dataclass
class RadioSegment:
    name: str
    min_duration_minutes: int
    max_duration_minutes: int


class TTSGeneration:
    def __init__(self, provider: str = "pyttsx3", voice: str | None = None):
        self.provider = provider
        self.voice = voice
        self.tts = self.load_audio_config(provider)

    @staticmethod
    def load_audio_config(provider: str):
        if provider == "kokoro":
            from kokoro_tts import generate_kokoro_audio
            return generate_kokoro_audio

        if provider == "pyttsx3":
            from pyttsx3_tts import generate_pyttsx3_audio
            return generate_pyttsx3_audio

        raise ValueError(f"Unsupported audio provider: {provider}")

    def generate_audio(self, text: str, output_file: str = "output_tts.wav"):
        return self.tts(
            text=text,
            voice=self.voice,
            output_file=output_file,
        )