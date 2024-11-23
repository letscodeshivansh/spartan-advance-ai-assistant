from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from gtts import gTTS
import speech_recognition as sr
import webbrowser as wb
import threading
from search import search, youtubesearch, wikisearch, tempsearch, timesearch, datesearch, searchwhat
from alarm import *
from news import *
# from openings import *
import tempfile
import pygame
import sounddevice as sd
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(query):
    if ".com" in query or ".co" in query or ".org" in query or ".in" in query:
        openwebapp(query)
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
        try:
            import pyautogui as pg
            speak("Okay")
            pg.press("k")
        except ImportError:
            speak("Controlling media is not supported in this environment.")
        return
    elif "wikipedia" in query:
        wikisearch(query)
        return
    elif "temperature" in query or "weather" in query:
        tempsearch(query)
        return
    elif "alarm" in query:
        alarm_time = st.text_input("Enter the time for the alarm (HH:MM *24 hour format): ")
        if alarm_time:
            speak("Enter the time for the alarm")
        submit_time = st.button("Set Alarm")
        if submit_time and alarm_time:
            st.write(f"Alarm is being set on {alarm_time}")
            sound_file = "alarmtone.wav"
            alarm_thread = threading.Thread(target=set_alarm, args=(alarm_time, sound_file))
            alarm_thread.daemon = True
            alarm_thread.start()
    elif "news" in query:
        return "news"
    else:
        response = model.generate_content(query + "give answer briefly")
        return response.text

# Initialize Streamlit app
st.set_page_config(page_title="Spartan")
st.header("Meet Spartan: Your Ultimate Assistant!")

image_path = 'assets/spartan3.png'
st.image(image_path, caption='Mighty Assistance, Spartan Style', width=250)

# Add source for API key
st.markdown("""
**Don't have an API key?**
Get your Google Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
""")

# Ask for personal API key
api_key = st.text_input("Enter your personal API key:")
submit_api = st.button("Submit Key")

if submit_api and not api_key:
    st.warning("Please enter your personal API key to proceed.")
    st.stop()

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat(history=[])
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    query = st.text_input("Enter Your Query:")
    submit = st.button("Ask")
    if submit and query:
        response = get_gemini_response(query)
        st.session_state['chat_history'].append(("You: ", query))
        st.subheader("Here's Your Answer:")
        if response:
            st.write(response)
            if response == "news":
                latest_news = get_news()  
                for newslines in latest_news:
                    st.write(newslines)
                   
            elif isinstance(response, str):
                st.session_state['chat_history'].append(("Bot: ", response))
            else:
                for chunk in response:
                    st.write(chunk)
                    st.session_state['chat_history'].append(("Bot: ", chunk))
        else:
            st.write("Response Generated")
    with st.expander("Chat History"):
        for role, text in st.session_state['chat_history']:
            st.write(f"{role} {text}")
else:
    st.stop()

if __name__ == "__main__":
    st.write("Get Ready to Conquer Your Questions with Spartan!")
