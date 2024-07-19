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
import pyttsx3 as pt

# Load the environment variables
load_dotenv()


engine=pt.init()
voices=engine.getProperty("voices")
#setting up the voice for assistant
engine.setProperty("voices",voices[1].id)
engine.setProperty("rate",200)

def speak(audio):   #making a speak function to say something as desired
    engine.say(audio)
    engine.runAndWait()


def takecommand():   # function to take your queries
    speech=sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        speech.pause_threshold=2    # time for it to pause and litsen to us
        speech.energy_threshold=250    # power of voice it hears( low->nearby voices can also be heared, high->we have to shout)
        audio=speech.listen(source,0,5)     # time for which it will listen to us and the resets after the time(in secs)
        try:     # exception handling
            print("Recognising and Understanding...")
            query=speech.recognize_google(audio,language='en-in')  
            st.write("You had said:",query,"\n")     # english of India

        except Exception as e:
            print("Speak Again")
            return "None"

        return query
    
    
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(query):
    
    if "bye" in query or "close your self" in query or "exit now" in query:  
        speak("Ok, Take Care, Have a good day")
        exit()
        return
    
    elif "wait" in query:  # waiting function
        speak("Going to the wait mode, to return back, speak hello")
        print("Going to the wait mode, to return back, speak hello")
        wait()
        
    elif ".com" in query or ".co" in query or ".org" in query or ".in"  in query:  # opening the web portals
        openwebapp(query)
        return 
    
    elif "open" in query:  # opens any app
        query = query.replace("open", "")
        pg.press("super")
        pg.typewrite(query)
        pg.sleep(2)
        pg.press("enter")
        return
     
    elif "google" in query:   # to search on google
        search(query)
        return 

    elif "time" in query:   # to get the current time
        timesearch(query)
        return

    elif "date" in query:  # to get the today's date
        datesearch(query)
        return

    elif "youtube" in query:  # to search anything on youtube
        youtubesearch(query)
        return

    elif "play" in query or "pause" in query:  # play/pause the video on youtube
        speak("Okay")
        pg.press("k")
        return 

    elif "mute video" in query:  # mute up the youtube video
        speak("Okay")
        pg.press("n")
        return

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
        return

    elif "temperature" in query or "weather" in query:  # search the current weather
        tempsearch(query)
        return

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
        response = model.generate_content(query + "give answer in 2 lines only")
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
with st.expander("Response: "):
    if text_query:
        response = get_gemini_response(text_query)
        if response:
            st.write(response)
        else:
            st.write("Response Generated")
    else:
        st.write("No query provided.")
        
    
# st.write(about)
# speak(about)

if __name__ == "__main__":
    st.write("Get Ready to Conquer Your Questions with Spartan!")


    
    
    
    
    




