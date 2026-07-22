from gtts import gTTS
import os

# Try importing pygame
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False


def speak(text):
    """
    Convert text to speech.
    Locally: Plays the audio.
    Cloud: Saves the audio only.
    """

    os.makedirs("audio", exist_ok=True)

    filename = "audio/output.mp3"

    tts = gTTS(text=text, lang="en")
    tts.save(filename)

    if PYGAME_AVAILABLE:
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            continue

        pygame.mixer.quit()

    return filename