import speech_recognition as sr
import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import pygame
import tempfile
import warnings
import streamlit as st
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

def takecommand():
    speech = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        speech.pause_threshold = 2     # time for it to pause and listen to us
        speech.energy_threshold = 250   # power of voice it hears (low->nearby voices can also be heard, high->we have to shout)
        audio = speech.listen(source, 0, 5)     # time for which it will listen to us and then reset (in secs)
        try:  # exception handling
            print("Recognising and Understanding...")
            query = speech.recognize_google(audio, language='en-in')  
            print("You had said:", query, "\n")  # English of India
        except Exception as e:
            print("Speak Again")
            return "None"
        return query

def get_news():
    url = 'https://news.google.com/rss'
    response = requests.get(url)
    try:
        soup = BeautifulSoup(response.content, 'lxml')
    except Exception:
        warnings.filterwarnings("ignore", category=UserWarning, message=".*looks like you're parsing an XML document using an HTML parser.*")
        soup = BeautifulSoup(response.content, 'html.parser')
    headlines = soup.find_all('item', limit=5)
    news_list = []
    for headline in headlines:
        news_list.append(headline.title.text)
    return news_list

def read_news():
    news_list = get_news()
    speak("Here are the top news headlines")
    st.write("Here are the top news headlines")
    for news in news_list:
        st.write(news)
    
