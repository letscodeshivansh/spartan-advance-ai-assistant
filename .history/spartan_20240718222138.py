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

def speak(audio, lang='en'):
    if audio:
        tts = gTTS(text=audio, lang=lang, slow=False)
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

# Function to initialize generative AI model
def initialize_genai(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")

# State variables
api_key = None
api_key_entered = False

# Input for API key

if not api_key_entered:
    api_key = st.text_input("Enter your personal API key:")
    submit_api = api_key_input.button("Submit Key")
else:
    api_key_input.empty()  # Clear the API key input section if already submitted

# Handle API key submission
if submit_api:
    if not api_key:
        st.warning("Please enter your personal API key to proceed.")
    else:
        api_key_entered = True
        # Initialize the generative AI model
        model = initialize_genai(api_key)

# Main application functionality
if api_key_entered:
    # Start Listening button
    if st.button("🎤"):
        with st.spinner("Listening..."):
            query = takecommand()  # Assume `takecommand()` is defined elsewhere
            if query:
                response = get_gemini_response(query)  # Assume `get_gemini_response()` is defined elsewhere
                st.write(response if response else "No valid response.")
            else:
                st.write("No valid input detected.")
            
    # Text input for users who prefer typing
    text_query = st.text_input("Or type your query here:")

    if st.button("Submit Query"):
        if text_query:
            with st.spinner("Wait..."):
                response = get_gemini_response(text_query)  # Assume `get_gemini_response()` is defined elsewhere
                if response:
                    speak(response)  # Assume `speak()` is defined elsewhere
                    st.write(response)
                else:
                    st.write("No valid response.")
        else:
            st.write("No input provided.")

    # Group the buttons and responses in an expander for better formatting
    with st.expander("Response:"):
        if text_query:
            response = get_gemini_response(text_query)  # Assume `get_gemini_response()` is defined elsewhere
            if response:
                st.write(response)
            else:
                st.write("No valid response.")
        else:
            st.write("No query provided.")

# Display a message if API key input is empty initially
if not api_key_entered and not submit_api:
    st.warning("Please enter your personal API key.")

if __name__ == "__main__":
    st.write("Get Ready to Conquer Your Questions with Spartan!")