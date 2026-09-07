from kokoro import KPipeline
from IPython.display import display, Audio
import soundfile as sf
import torch

def generate_kokoro_audio(text: str, voice: str | None = None, output_file: str = "output.wav"):
    pipeline = KPipeline(lang_code="a")
    generator = pipeline(text, voice=voice if voice is not None else "af_heart")

    for _, (_, _, audio) in enumerate(generator):
        sf.write(output_file, audio, 24000)

    return output_file