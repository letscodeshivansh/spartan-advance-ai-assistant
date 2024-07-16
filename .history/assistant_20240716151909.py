about = "Hi, this is your virtual Assistant, how can I help you ?"

# This is the main program
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

# Load the environment variables
load_dotenv()

engine = pt.init()
voices = engine.getProperty("voices")
engine.setProperty("voices", voices[1].id)
engine.setProperty("rate", 200)

def speak(audio):
    engine.say(audio)
    #engine.runAndWait()

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
            speak("speak Again!")
            return None

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(query):
    response = model.generate_content(query)
    return response.text

def process_query(query): # the main program that works according to our queries
    if "bye" in query or "close your self" in query or "exit now" in query:   # to make the program exit or end
        speak("ok, Take Care, Have a good day")
        exit()

    elif "wait" in query:  # waiting function
        speak("going to the wait mode,to return back, speak hello")
        print("going to the wait mode,to return back, speak hello")
        wait()
            
    elif ".com" in query or ".co" in query or ".org" in query or ".in"  in query:  # opening the web portals
        openwebapp(query)

    elif "close" in query:  # closing 1 tab
        closewebapp(query)

    elif "open" in query:  # opens any app
        query=query.replace("open","")
        pg.press("super")
        pg.typewrite(query)
        pg.sleep(2)
        pg.press("enter")

    elif "google" in query:   # to search on google
        search(query)

    elif "time" in query:   # to get the current time
        timesearch(query)

    elif "date" in query:  # to get the todays date
        datesearch(query)

    elif any(word in query for word in ["what", "why", "when", "where", "how", "who", "which"]):
        searchwhat(query)

    elif "youtube" in query:  # to search anything on youtube
        youtubesearch(query)

    elif "play" in query or "pause" in query:  #play/pause the video on youtube
        speak("okay")
        pg.press("k")

    elif "mute video" in query:  # mute up the youtube video
        speak("okay")
        pg.press("n")

    elif "volume" in query:  # increase/decrease the volume
        if "up" in query or "increase" in query:
            speak("increasing volume")
            volume_up()
        elif "down" in query or "decrease" in query:
            speak("decreasing volume")
                volume_down()
            else:
                pass

        elif "wikipedia" in query:  # search on wikipedia
            wikisearch(query)

        elif "temperature" in query or "weather" in query:  # serch the current weather
            tempsearch(query)

        elif "alarm" in query:  # setting up the alrm
            alarm_time = input("Enter the time for the alarm (HH:MM *24 hour format): ")
            speak("Enter the time for the alarm ")
            sound_file = "alarmtone.wav"  
            speak(f"alarm is set for {alarm_time}")
            # Run the alarm function in a separate thread
            alarm_thread = threading.Thread(target=set_alarm, args=(alarm_time, sound_file))
            alarm_thread.daemon = True  # Set as daemon thread so it exits when main program exits
            alarm_thread.start()
            print("if you close the program, alarm would not ring then")
            speak("if you close the program, alarm would not ring then")
            main_program()     # Run the main program

        elif "news" in query:  # getting latest news
            speak("reading the news")
            print("Reading the news")
            read_news() 
            
        else:
            speak(get_gemini_response(query))

# Initialize Streamlit app
st.set_page_config(page_title="Your Assistant")
st.header("Your Virtual Assistant")


if st.button("Start Listening"):
    with st.spinner("Listening..."):
        query = takecommand()
        if query:
            st.write(f"You said: {query}")
            response = process_query(query)
            st.write(f"Assistant: {response}")
            speak(response)
        else:
            st.write("No valid input detected.")

if st.button("Tell me about yourself"):
    st.write(about)
    speak(about)

# Run the Streamlit app
if __name__ == "__main__":
    st.write("Press the button to start the assistant.")
