about = "Hey, your Spartan here!"

# This is the main program
from dotenv import load_dotenv
import streamlit as st
import os 
import google.generativeai as genai
from gtts import gTTS
import speech_recognition as sr
import webbrowser as wb
import pyautogui as pg
import threading  
from search import *
from openings import *
from alarm import *
from volume_settings import *
from news import *
import tempfile
import pygame

# Load the environment variables
load_dotenv()

# Initialize pygame mixer for audio playback
pygame.mixer.init() 

def speak(audio):
    if audio:  # Check if audio is not empty
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
        speech.pause_threshold = 2
        speech.energy_threshold = 250
        audio = speech.listen(source, 0, 5)
        try:
            query = speech.recognize_google(audio, language='en-in')
            return query.lower()
        except Exception:
            speak("Speak Again!")
            return None

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(query):
    response = model.generate_content(query + "give answer in 2 lines only")
    return response.text

def process_query(query):
    if "bye" in query or "close your self" in query or "exit now" in query:  
        speak("Ok, Take Care, Have a good day")
        exit()

    elif "wait" in query:  # waiting function
        speak("Going to the wait mode, to return back, speak hello")
        print("Going to the wait mode, to return back, speak hello")
        wait()
            
    elif ".com" in query or ".co" in query or ".org" in query or ".in"  in query:  # opening the web portals
        openwebapp(query)

    elif "close" in query:  # closing 1 tab
        closewebapp(query)

    elif "open" in query:  # opens any app
        query = query.replace("open", "")
        pg.press("super")
        pg.typewrite(query)
        pg.sleep(2)
        pg.press("enter")

    elif "google" in query:   # to search on google
        search(query)

    elif "time" in query:   # to get the current time
        timesearch(query)

    elif "date" in query:  # to get the today's date
        datesearch(query)

    elif any(word in query for word in ["what", "why", "when", "where", "how", "who", "which"]):
        searchwhat(query)

    elif "youtube" in query:  # to search anything on youtube
        youtubesearch(query)

    elif "play" in query or "pause" in query:  # play/pause the video on youtube
        speak("Okay")
        pg.press("k")

    elif "mute video" in query:  # mute up the youtube video
        speak("Okay")
        pg.press("n")

    elif "volume" in query:  # increase/decrease the volume
        if "up" in query or "increase" in query:
            speak("Increasing volume")
            volume_up()
        elif "down" in query or "decrease" in query:
            speak("Decreasing volume")
            volume_down()
        else:
            pass

    elif "wikipedia" in query:  # search on wikipedia
        wikisearch(query)

    elif "temperature" in query or "weather" in query:  # search the current weather
        tempsearch(query)

    elif "alarm" in query:  # setting up the alarm
        alarm_time = input("Enter the time for the alarm (HH:MM *24 hour format): ")
        speak("Enter the time for the alarm ")
        sound_file = "alarmtone.wav"  
        speak(f"Alarm is set for {alarm_time}")
        # Run the alarm function in a separate thread
        alarm_thread = threading.Thread(target=set_alarm, args=(alarm_time, sound_file))
        alarm_thread.daemon = True  # Set as daemon thread so it exits when main program exits
        alarm_thread.start()
        print("If you close the program, the alarm would not ring then")
        speak("If you close the program, the alarm would not ring then")
        main_program()     # Run the main program

    elif "news" in query:  # getting latest news
        speak("Reading the news")
        print("Reading the news")
        read_news() 
            
    else:
        response = get_gemini_response(query)
        speak(response)

import streamlit as st
from PIL import Image
import base64

# Function to add a background image
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function to add background image
add_bg_from_local('assets/spartan_bg.jpg') # Replace 'assets/spartan_bg.jpg' with the path to your background image

# Set the page title and icon
st.set_page_config(page_title="Spartan")

# Function to center content
def center_content(content):
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; align-items: center; height: 100vh;">
            <div>{content}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Create centered header
header_html = '<h1>Spartan</h1>'
center_content(header_html)

# Create centered button and process the query
if st.button("Start Listening"):
    with st.spinner("Listening..."):
        query = takecommand()
        if query:
            st.write(f"You said: {query}")
            process_query(query)
        else:
            st.write("No valid input detected.")

# Create centered about section
about = "Hi, this is your virtual Assistant, how can I help you?"
center_content(about)

# Speak the about text
speak(about)

# Create centered image
image_path = 'assets/spartan1.jpg'
image = Image.open(image_path)

center_content(f'<img src="data:image/jpeg;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}" width="250"><p>Hi this is your Spartan</p>')



if __name__ == "__main__":
    st.write("Press the button to start the assistant.")
