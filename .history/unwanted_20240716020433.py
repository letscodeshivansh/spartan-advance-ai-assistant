from dotenv import load_dotenv
import streamlit as st
import os 
import google.generativeai as genai
import pyttsx3 as pt
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
import playsound
from gtts import gTTS
# Load the environment variables
load_dotenv()

# Initialize text-to-speech engine
engine = pt.init()
voices = engine.getProperty("voices")
engine.setProperty("voices", voices[1].id)
engine.setProperty("rate", 200)

def speak(audio):
    # Create a temporary audio file
    with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
        tts = gTTS(text=audio, lang='en')
        tts.save(f"{tmp_file.name}.mp3")
        playsound.playsound(f"{tmp_file.name}.mp3")

def takecommand():  # Function to take queries
    speech = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        speech.pause_threshold = 2
        speech.energy_threshold = 250
        audio = speech.listen(source, 0, 5)
        try:
            print("Recognizing...")
            query = speech.recognize_google(audio, language='en-in')
            print("You asked:", query)
            return query.lower()
        except Exception:
            speak("Speak Again!")
            print("Sorry, I didn't get that.")
            return None

# Configure the Generative AI with the API key from the environment variable
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(query):
    response = model.generate_content(query)
    return response.text

def perform_task(query):  # Main program that works according to queries
    if "bye" in query or "close" in query or "exit" in query:
        speak("Okay, take care, have a good day!")
        return

    if "wait" in query:
        speak("Going to wait mode. To return, say hello.")
        print("Going to wait mode. To return, say hello.")
        return

    if ".com" in query or ".co" in query or ".org" in query or ".in" in query:
        openwebapp(query)
    elif "close" in query:
        closewebapp(query)
    elif "open" in query:
        app_name = query.replace("open", "").strip()
        pg.press("super")
        pg.typewrite(app_name)
        pg.sleep(2)
        pg.press("enter")
    elif "google" in query:
        search(query)
    elif "time" in query:
        timesearch(query)
    elif "date" in query:
        datesearch(query)
    elif any(word in query for word in ["what", "why", "when", "where", "how", "who", "which"]):
        searchwhat(query)
    elif "youtube" in query:
        youtubesearch(query)
    elif "play" in query or "pause" in query:
        speak("Okay")
        pg.press("k")
    elif "mute video" in query:
        speak("Okay")
        pg.press("n")
    elif "volume" in query:
        if "up" in query or "increase" in query:
            speak("Increasing volume")
            volume_up()
        elif "down" in query or "decrease" in query:
            speak("Decreasing volume")
            volume_down()
    elif "wikipedia" in query:
        wikisearch(query)
    elif "temperature" in query or "weather" in query:
        tempsearch(query)
    elif "alarm" in query:
        alarm_time = st.text_input("Enter the alarm time (HH:MM in 24-hour format):")
        if alarm_time:
            sound_file = "alarmtone.wav"
            speak(f"Alarm is set for {alarm_time}")
            # Start alarm in a separate thread
            alarm_thread = threading.Thread(target=set_alarm, args=(alarm_time, sound_file))
            alarm_thread.daemon = True
            alarm_thread.start()
            print("If you close the program, the alarm will not ring.")
            speak("If you close the program, the alarm will not ring.")
    elif "news" in query:
        speak("Reading the news")
        print("Reading the news")
        read_news()
    else:
        speak(get_gemini_response(query))

# Initialize Streamlit app
st.set_page_config(page_title="Your Assistant")
st.header("Your Virtual Assistant")

# About section
about = "Hi, this is your virtual Assistant, how can I help you?"
if st.button("Tell me about yourself"):
    st.write(about)
    speak(about)

if st.button("Start Listening"):
    with st.spinner("Listening..."):
        query = takecommand()
        if query:
            st.write(f"You said: {query}")
            perform_task(query)
        else:
            st.write("No valid input detected.")

# Run the Streamlit app
if __name__ == "__main__":
    st.write("Press the button to start the assistant.")
