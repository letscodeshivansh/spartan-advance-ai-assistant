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
    response = model.generate_content(query + "give answer in 2 lines only")
    
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

    
            
    else:
        response = get_gemini_response(query)
        speak(response)

# Initialize Streamlit app
st.set_page_config(page_title="Spartan")
st.header("Meet Spartan: Your Ultimate Assistant!")

image_path = 'assets/spartan3.png'
st.image(image_path, caption='Mighty Assistance, Spartan Style', width=250)


# Start Listening button
if st.button("🔊"):
    with st.spinner("Listening..."):
        query = takecommand()
        if query:
            response = get_gemini_response(query)
            # st.write(response)
        else:
            st.write("No valid input detected.")
            
# Text input for users who prefer typing
text_query = st.text_input("Or type your query here:")

if st.button("Submit Query"):
    if text_query:
        with st.spinner("Wait..."):
            response = get_gemini_response(text_query)
            speak(response)
            st.subheader("Response: ")
            for word in response:
                st.write(word.text)
            # st.write(response)
    else:
        st.write("No input provided.")

# Group the buttons and responses in an expander for better formatting
with st.expander("Assistant Response"):
    if text_query:
        st.write(chunk.text)
        
    
# st.write(about)
# speak(about)

if __name__ == "__main__":
    st.write("Get Ready to Conquer Your Questions with Spartan!")




