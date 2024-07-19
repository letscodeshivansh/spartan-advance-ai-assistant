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
import sounddevice as sd
def speak(audio):
    tts = gTTS(text=audio, lang='en')
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts.save(fp.name + ".mp3")
        pygame.mixer.music.load(fp.name + ".mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue


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
    
