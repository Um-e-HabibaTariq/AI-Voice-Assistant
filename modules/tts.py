from gtts import gTTS
import pygame
import os
import time

def speak(text):
    os.makedirs("audio", exist_ok=True)

    filename = "audio/output.mp3"

    tts = gTTS(text=text, lang="en")
    tts.save(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.5)

    pygame.mixer.quit()


if __name__ == "__main__":
    speak("Hello! I am your AI Voice Assistant.")