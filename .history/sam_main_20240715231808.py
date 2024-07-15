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
import os
import threading  
from search import *
from openings import *
from alarm import *
from volume_settings import *
from news import *

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
            print("You had said:",query,"\n")     # english of India

        except Exception as e:
            speak("speak Again !")
            print("Sorry I did'nt get what you said")
            return "None"

        return query
def wait():  # wait function
    start() 

def alarm(query):   # alarm function
    timehere = open("Alarmtext.txt","a")
    timehere.write(query)
    timehere.close()
    os.startfile("alarm.py")

def start():  # the start function of assistant
    while True:
        query=takecommand().lower()     # if no .lower(), it can get confused between upper case and lower case 
        if "hello" in query or "hey" in query or "hi" in query or "sam" in query:
            speak("Hi, this is your virtual assistant, how can i help you ?")
            main_program()
        else:
            start()

def main_program():  # the main program that works according to our queries
    while True:                                                                 
        query=takecommand().lower()  
        
        if "tell me about you" in query:  # intro function
            print(about)
            speak(about)

        elif "bye" in query or "close your self" in query or "exit now" in query:   # to make the program exit or end
            speak("ok, Take Care, Have a good day")
            exit()

        elif "wait" in query:  # waiting function
            speak("going to the wait mode,to return back, speak hello")
            print("going to the wait mode,to return back, speak hello")
            wait()

        elif any(word in query for word in ["nice", "good", "excellent", "fine", "better", "happy", "marvelous"]):
            speak(" oh nice, i am also good. how may i help you?")

        elif "thank" in query or "thanks" in query:
            speak("you'r welcome")

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
        
        elif any(word in query for word in ["fuck", "sex", "porn", "sexy", "gay", "lesbian", "sexo"]):
            speak("Sorry bro, we are in public")
        else:
            pass


start()

'''
to get the voices and index, use the following code:
n=#the number of voices installed-1
for i in range(n):
    print(voices[i])
'''
# engine.say("Hello, myself sam")
# engine.runAndWait()
                






