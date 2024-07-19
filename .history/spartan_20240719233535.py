import streamlit as st
import os
import google.generativeai as genai
import threading  
from alarm import set_alarm, speak
import sounddevice as sd
import queue
import tempfile
import pygame
import numpy as np
from dotenv import load_dotenv
import speech_recognition as sr
import pyautogui as pg
from search import *
from openings import *
from volume_settings import *
from news import *

# Load the environment variables
load_dotenv()

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Function to speak text using gTTS
def speak(audio, lang='en'):
    if audio:
        tts = gTTS(text=audio, lang=lang, slow=False)
        with tempfile.NamedTemporaryFile(delete=True) as fp:
            tts.save(fp.name + ".mp3")
            pygame.mixer.music.load(fp.name + ".mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                continue

# Function to capture voice command using sounddevice
def takecommand():
    q = queue.Queue()

    def callback(indata, frames, time, status):
        q.put(indata.copy())

    with sd.InputStream(samplerate=16000, channels=1, callback=callback):
        st.write("Listening...")
        audio_data = []
        while True:
            data = q.get()
            audio_data.append(data)
            if len(audio_data) > 160:  # About 5 seconds of audio
                break
        audio_data = np.concatenate(audio_data, axis=0)
        return audio_data

# Configure generative AI model
def initialize_genai(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(query):
    response = model.generate_content(query + " give answer briefly")
    return response

# Initialize Streamlit app
st.set_page_config(page_title="Spartan")
st.header("Meet Spartan: Your Ultimate Assistant!")

image_path = 'assets/spartan3.png'
st.image(image_path, caption='Mighty Assistance, Spartan Style', width=250)

# Ask for personal API key
api_key = st.text_input("Enter your personal API key:")
submit_api = st.button("Submit Key")

if submit_api and not api_key:
    st.warning("Please enter your personal API key to proceed.")
    st.stop()

if api_key:
    try:
        # Initialize generative AI model
        model = initialize_genai(api_key)
    except Exception as e:
        st.error("Error initializing AI model. Please check your API key.")
        st.stop()

    chat = model.start_chat(history=[])
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # Text input for users who prefer typing
    text_query = st.text_input("Enter Your Query:")
    submit = st.button("Ask")

    if submit and text_query:
        response = get_gemini_response(text_query)
        st.session_state['chat_history'].append(("You: ", text_query))
        st.subheader("Here's Your Answer:")
        if response:
            st.write(response.text)
            st.session_state['chat_history'].append(("Bot: ", response.text))
        else:
            st.write("No valid response.")

    # Handle setting the alarm
    with st.expander("Set Alarm"):
        alarm_time = st.text_input("Enter the time for the alarm (HH:MM *24 hour format): ")
        if alarm_time:
            speak("Enter the time for the alarm")
        submit_time = st.button("Set Alarm")
        if submit_time and alarm_time:
            st.write(f"Alarm is being set on {alarm_time}")
            sound_file = "alarmtone.wav"  
            alarm_thread = threading.Thread(target=set_alarm, args=(alarm_time, sound_file))
            alarm_thread.daemon = True  # Set as daemon thread so it exits when main program exits
            alarm_thread.start()

    with st.expander("Chat History"):
        for role, text in st.session_state['chat_history']:
            st.write(f"{role} {text}")

else:
    st.stop()

if __name__ == "__main__":
    st.write("Get Ready to Conquer Your Questions with Spartan!")
