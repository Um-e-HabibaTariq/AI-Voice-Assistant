import sounddevice as sd
from scipy.io.wavfile import write
import os

SAMPLE_RATE = 44100
DURATION = 5

def record_audio(filename="audio/input.wav"):
    """
    Record audio from microphone and save as WAV file.
    """

    os.makedirs("audio", exist_ok=True)

    print("🎤 Recording... Speak now!")

    recording = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    write(filename, SAMPLE_RATE, recording)

    print(f"✅ Audio saved to {filename}")

    return filename


