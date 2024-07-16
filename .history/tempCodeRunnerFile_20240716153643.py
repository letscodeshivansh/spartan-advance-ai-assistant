from gtts import gTTS
import pygame
import tempfile

# Initialize pygame mixer for audio playback
pygame.mixer.init()

def speak(audio):
    tts = gTTS(text=audio, lang='en')
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts.save(fp.name + ".mp3")
        pygame.mixer.music.load(fp.name + ".mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

# Example usage
if __name__ == "__main__":
    speak("Hi, this is your virtual Assistant, how can I help you?")
