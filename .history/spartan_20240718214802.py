import streamlit as st
import speech_recognition as sr
import os
from gtts import gTTS
import webbrowser as wb
import pyautogui as pg
import threading
from search import *
from openings import *
from alarm import *
from volume_settings import *
from news import *
import pygame
import pyttsx3 as pt

# Initialize pyttsx3 for speech synthesis
engine = pt.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 200)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takecommand():
    speech = sr.Recognizer()
    with sr.Microphone() as source:
        speech.pause_threshold = 2
        speech.energy_threshold = 250
        try:
            st.write("Recognising and Understanding...")
            audio = speech.listen(source, timeout=5)
            query = speech.recognize_google(audio, language='en-in')
            st.write("You said:", query, "\n")
        except sr.WaitTimeoutError:
            st.write("Listening timed out")
            return None
        except sr.RequestError:
            st.write("API unavailable")
            return None
        except sr.UnknownValueError:
            st.write("Unable to recognize speech")
            return None
        except Exception as e:
            st.write(f"An error occurred: {e}")
            return None
    return query

def get_gemini_response(query):
    if "bye" in query or "close yourself" in query or "exit now" in query:
        speak("Ok, Take Care, Have a good day")
        exit()

    elif "wait" in query:
        speak("Going to the wait mode, to return back, speak hello")
        print("Going to the wait mode, to return back, speak hello")
        wait()

    elif ".com" in query or ".co" in query or ".org" in query or ".in" in query:
        openwebapp(query)
        return

    elif "open" in query:
        query = query.replace("open", "")
        pg.press("super")
        pg.typewrite(query)
        pg.sleep(2)
        pg.press("enter")
        return

    elif "google" in query:
        search(query)
        return

    elif "time" in query:
        timesearch(query)
        return

    elif "date" in query:
        datesearch(query)
        return

    elif "youtube" in query:
        youtubesearch(query)
        return

    elif "play" in query or "pause" in query:
        speak("Okay")
        pg.press("k")
        return

    elif "mute video" in query:
        speak("Okay")
        pg.press("n")
        return

    elif "volume" in query:
        if "up" in query or "increase" in query:
            speak("Increasing volume")
            volume_up()
        elif "down" in query or "decrease" in query:
            speak("Decreasing volume")
            volume_down()
        else:
            pass

    elif "wikipedia" in query:
        wikisearch(query)
        return

    elif "temperature" in query or "weather" in query:
        tempsearch(query)
        return

    elif "alarm" in query:
        alarm_time = input("Enter the time for the alarm (HH:MM *24 hour format): ")
        speak("Enter the time for the alarm ")
        sound_file = "alarmtone.wav"
        speak(f"Alarm is set for {alarm_time}")
        alarm_thread = threading.Thread(target=set_alarm, args=(alarm_time, sound_file))
        alarm_thread.daemon = True
        alarm_thread.start()
        print("If you close the program, the alarm would not ring then")
        speak("If you close the program, the alarm would not ring then")
        main_program()

    elif "news" in query:
        speak("Reading the news")
        print("Reading the news")
        read_news()

    else:
        response = model.generate_content(query + " give answer in 2 lines only")
        return response.text

# Initialize Streamlit app
st.set_page_config(page_title="Spartan")
st.header("Meet Spartan: Your Ultimate Assistant!")

image_path = 'assets/spartan3.png'
st.image(image_path, caption='Mighty Assistance, Spartan Style', width=250)

# Start Listening button
if st.button("🎤"):
    with st.spinner("Listening..."):
        query = takecommand()
        if query:
            response = get_gemini_response(query)
            st.write(response)
        else:
            st.write("No valid input detected.")

# Text input for users who prefer typing
text_query = st.text_input("Or type your query here:")

if st.button("Submit Query"):
    if text_query:
        with st.spinner("Wait..."):
            response = get_gemini_response(text_query)
        if response:
            speak(response)
        else:
            st.write("Response Generated")
    else:
        st.write("No input provided.")

# Group the buttons and responses in an expander for better formatting
with st.expander("Response:"):
    if text_query:
        response = get_gemini_response(text_query)
        if response:
            st.write(response)
        else:
            st.write("Response Generated")
    else:
        st.write("No query provided.")

if __name__ == "__main__":
    st.write("Get Ready to Conquer Your Questions with Spartan!")
