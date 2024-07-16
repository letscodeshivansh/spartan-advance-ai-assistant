import os
import pyautogui as pg
import webbrowser as wb
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

def openwebapp(query):
    if ".com" in query or ".co" in query or ".org" in query or ".in" in query:
        query = query.replace('open', "").replace(" ", '')
        speak(query)
        wb.open(f"https://www.{query}")

def closewebapp(query):
    if "one tab" in query or "1 tab" in query or "tab" in query:
        speak('closing the tab')
        pg.hotkey("ctrl", "w")  # to close any tab, we can type ctrl+w, this will close the tab
