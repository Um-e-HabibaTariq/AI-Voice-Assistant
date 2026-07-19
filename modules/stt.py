import whisper

print("Loading Whisper model... (This may take a minute the first time)")

model = whisper.load_model("base")

def speech_to_text(audio_path="audio/input.wav"):
    print("Converting speech to text...")

    result = model.transcribe(audio_path)

    text = result["text"].strip()

    print("\nYou said:")
    print(text)

    return text


if __name__ == "__main__":
    speech_to_text()
