import os
import tempfile
import datetime
import requests
import pygame
from bs4 import BeautifulSoup
from gtts import gTTS
import speech_recognition as sr
import webbrowser as wb

# # Initialize pygame mixer for audio playback
# pygame.mixer.init()

def speak(audio):
    tts = gTTS(text=audio, lang='en')
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts.save(fp.name + ".mp3")
        pygame.mixer.music.load(fp.name + ".mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

def search(query):  # Google search
    if "google" in query:
        query = query.replace("hey", "").replace("eva", "").replace("can you", "").replace("google", "").replace("why", "").replace("what", "").replace("when", "").replace("where", "").replace("how", "").replace("search", "")
        st.write("so, I found this")
        try:
            import pywhatkit as pw
            result = pw.search(query)
            import wikipedia as wk
            summary = wk.summary(query, sentences=3)
            st.write("summary")
        except ImportError as e:
            st.write(f"Error importing modules: {e}")
        except Exception as e:
            st.write(f"An error occurred: {e}")

def youtubesearch(query):  # Search anything on YouTube
    if "youtube" in query:
        st.write("searching on youtube")
        query = query.replace("hey", "").replace("eva", "").replace("can you", "").replace("google", "").replace("search", "").replace("youtube", "").replace("video", "").replace("play", "").replace("on", "")
        web = "https://www.youtube.com/results?search_query=" + query
        wb.open(web)
        st.write("done")

def wikisearch(query):  # Wikipedia search
    if 'wikipedia' in query:
        st.write("searching on wikipedia")
        query = query.replace("hey", "").replace("search", "").replace("wikipedia", "").replace("eva", "")
        try:
            import wikipedia as wk
            result = wk.summary(query, sentences=5)
            st.write("Here is your results")
        except ImportError as e:
            st.write(f"Error importing Wikipedia module: {e}")
        except Exception as e:
            st.write("No page found on Wikipedia")

def tempsearch(query):  # Search for the temperature
    if "temperature" in query or "weather" in query:
        query = query.replace("what", "").replace("is", "")
        link = "https://www.google.com/search?q=" + query
        result = requests.get(link)
        data = BeautifulSoup(result.text, "html.parser")
        try:
            temp = data.find("div", class_="BNeawe").text
            st.write(temp)
        except AttributeError:
            st.write("Could not retrieve temperature information.")

def timesearch(query):  # Search for the current time
    if "time" in query:
        query = query.replace("what", "").replace("is", "").replace("the", "")
        time = datetime.datetime.now().strftime("%H:%M")
        st.write(time)


def datesearch(query):  # Search for the current date
    if "date" in query:
        query = query.replace("what", "").replace("is", "").replace("the", "")
        date = datetime.datetime.now().strftime("%d:%m:%Y")
        speak(date)
        print(date)

def searchwhat(query):  # Google search for specific questions
    if any(word in query for word in ["what", "why", "when", "where", "how", "who", "which"]):
        query = query.replace("hey", "").replace("eva", "").replace("can you", "").replace("google", "").replace("why", "").replace("what", "").replace("when", "").replace("where", "").replace("how", "").replace("is", "").replace("search", "")
        speak("so, I found this")
        try:
            import wikipedia as wk
            result = wk.summary(query, sentences=3)
            print(result)
            speak(result)
        except ImportError as e:
            print(f"Error importing Wikipedia module: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
