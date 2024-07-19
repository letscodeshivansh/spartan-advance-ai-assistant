import pywhatkit as pw
import wikipedia as wk
from gtts import gTTS
import speech_recognition as sr
import webbrowser as wb
from bs4 import BeautifulSoup
import requests
import datetime
import pygame
import tempfile
import sounddevice as sd
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


def search(query):  # google search
    if "google" in query:
        query = query.replace("hey", "").replace("eva", "").replace("can you", "").replace("google", "").replace("why", "").replace("what", "").replace("when", "").replace("where", "").replace("how", "").replace("search", "")
        speak("so, I found this")
        try:
            pw.search(query)
            result = wk.summary(query, sentences=3)
            speak(result)
            print(result)
        except:
            print("")

def youtubesearch(query):  # to search anything on youtube
    if "youtube" in query:
        speak("searching on youtube")
        query = query.replace("hey", "").replace("eva", "").replace("can you", "").replace("google", "").replace("search", "").replace("youtube", "").replace("video", "").replace("play", "").replace("on", "")
        web = "https://www.youtube.com/results?search_query=" + query
        wb.open(web)
        speak("done")

def wikisearch(query):  # wikipedia
    if 'wikipedia' in query:
        speak("searching on wikipedia")
        query = query.replace("hey", "").replace("search", "").replace("wikipedia", "").replace("eva", "")
        try:
            result = wk.summary(query, sentences=5)
            speak("results on wikipedia are...")
            print(result)
            speak(result)
        except:
            print("No page found on wikipedia")
            speak("No page found on wikipedia")

def tempsearch(query):  # searching for the temperature
    if "temperature" in query or "weather" in query:
        query = query.replace("what", "").replace("is", "")
        link = "https://www.google.com/search?q=" + query
        result = requests.get(link)
        data = BeautifulSoup(result.text, "html.parser")
        temp = data.find("div", class_="BNeawe").text
        speak(query)
        speak(temp)

def timesearch(query):  # searching for the current time
    if "time" in query:
        query = query.replace("what", "").replace("is", "").replace("the", "")
        time = datetime.datetime.now().strftime("%H:%M")
        speak(time)
        print(time)

def datesearch(query):  # searching for the current date
    if "date" in query:
        query = query.replace("what", "").replace("is", "").replace("the", "")
        date = datetime.datetime.now().strftime("%d:%m:%Y")
        speak(date)
        print(date)

def searchwhat(query):  # google search
    if any(word in query for word in ["what", "why", "when", "where", "how", "who", "which"]):
        query = query.replace("hey", "").replace("eva", "").replace("can you", "").replace("google", "").replace("why", "").replace("what", "").replace("when", "").replace("where", "").replace("how", "").replace("is", "").replace("search", "")
        speak("so, I found this")
        try:
            result = wk.summary(query, sentences=3)
            print(result)
            speak(result)
        except:
            print("")
