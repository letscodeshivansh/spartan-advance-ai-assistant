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

        class Solution {
public:
    void dfs(TreeNode* node, string& path,  int p, int q, string& lcatostart, string& lcatodest){
        if(node == NULL) return;
        if(node->val == p) lcatostart = path;
        if(node->val == q) lcatodest = path;

        path.push_back('L');
        dfs(node->left, path, p, q, lcatostart, lcatodest);
        path.pop_back();

        path.push_back('R');
        dfs(node->left, path, p, q, lcatostart, lcatodest);
        path.pop_back();

    }
    string getDirections(TreeNode* root, int start, int dest) {
        string path = "";
        string lcatostart;
        string lcatodest;
        dfs(root, path, start, dest, lcatostart, lcatodest);
        
        int commonlen = 0, i = 0, j = 0;
        while(i < lcatostart.length() && j < lcatodest.length()){
            if(lcatostart[i] == lcatodest[j]){
                commonlen++;
                i++;
                j++;
            }else break;
        }
        lcatostart = lcatostart.substr(commonlen, lcatostart.length() - commonlen);
        lcatodest = lcatodest.substr(commonlen, lcatodest.length() - commonlen);

        for(auto ch: lcatostart) ch ='U';
        return lcatostart + lcatodest;
    }
};

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
