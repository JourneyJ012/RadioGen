import pyttsx3


def generate_pyttsx3_audio(
    text: str,
    voice: str | None = "gmw/en-us",
    output_file: str = "output.wav",
):
    engine = pyttsx3.init()
    voice = voice if voice is not None else "gmw/en-us"

    voices = engine.getProperty("voices")

    for v in voices:
        if v.id == voice:
            engine.setProperty("voice", v.id)
            break
    else:
        raise ValueError(f"Voice not found: {voice}")

    engine.save_to_file(text, output_file)
    engine.runAndWait()

    return output_file