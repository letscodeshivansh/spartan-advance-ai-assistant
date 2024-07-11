import pywhatkit as pw
import wikipedia as wk
import pyttsx3 as pt
import speech_recognition as sr
import webbrowser as wb
from bs4 import BeautifulSoup
import requests
import datetime 

engine=pt.init()
voices=engine.getProperty("voices")
engine.setProperty("voices",voices[1].id)
engine.setProperty("rate",200)

                                                                                      
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takecommand():
    speech=sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        speech.pause_threshold=2                                                         
        speech.energy_threshold=250                                                  
        audio=speech.listen(source,0,5)                                                  
        try:                                                                            
            print("Recognising and Understanding...")
            query=speech.recognize_google(audio,language='en-in')  
            print("You had said:",query,"\n")                                          

        except Exception as e:
            print("Speak Again")
            return "None"

        return query
def search(query):   # google search 
    if "google" in query:
        query=query.replace("hey","")
        query=query.replace("eva","")
        query=query.replace("can you","")
        query=query.replace("google","")
        query=query.replace("why","")
        query=query.replace("what","")
        query=query.replace("when","")
        query=query.replace("where","")
        query=query.replace("how","")
        query=query.replace("search","")
        engine.say("so, i found this")
        engine.runAndWait()

        try:
            pw.search(query)
            result=wk.summary(query,sentences=3)
            engine.say(result)
            engine.runAndWait()
            print(result)
        except:
            print("")
            

def youtubesearch(query):  #to search anything on youtube
    if "youtube" in query:
        engine.say("searching on youtube")
        engine.runAndWait()
        query=query.replace("hey","")   
        query=query.replace("eva","")
        query=query.replace("can you","")
        query=query.replace("google","")
        query=query.replace("search","")
        query=query.replace("youtube","")
        query=query.replace("video","")
        query=query.replace("play","")
        query=query.replace("on","")
        web="https://www.youtube.com/results?search_query="+query    # to get searched in the search section
        wb.open(web)
        # pw.playonyt(query)  ->we can run this if we want to play the first video in the searched list
        engine.say("done")
        engine.runAndWait()

def wikisearch(query):  #wikipedia
    if 'wikipedia' in query:
        engine.say("searching on wikipedia")
        engine.runAndWait()
        query=query.replace("hey","")
        query=query.replace("search","")
        query=query.replace("wikipedia","")
        query=query.replace("eva","")
        try:
            result=wk.summary(query,sentences=5)
            engine.say("results on wikipedia are...")
            engine.runAndWait()
            print(result)
            engine.say(result)
            engine.runAndWait()
        except:
            print("No page found on wikipedia")
            engine.say("No page found on wikipedia")
            engine.runAndWait()

def tempsearch(query):  # searching for the temperature
    if "temperature" in query or "weather" in query:
        query=query.replace("what","")
        query=query.replace("is","")
        link="https://www.google.com/search?q="+query
        result=requests.get(link)
        data=BeautifulSoup(result.text,"html.parser")
        temp=data.find("div",class_="BNeawe").text
        engine.say(query)
        engine.runAndWait()
        engine.say(temp)
        engine.runAndWait()
        print(temp)
def timesearch(query):  # searching for the current time
    if "time" in query:
        query=query.replace("what","")
        query=query.replace("is","")
        query=query.replace("the","")
        time=datetime.datetime.now().strftime("%H:%M")
        engine.say(time)
        engine.runAndWait()
        print(time)

def datesearch(query):    # searching for the current time
    if "date" in query:
        query=query.replace("what","")
        query=query.replace("is","")
        query=query.replace("the","")
        time=datetime.datetime.now().strftime("%d:%m:%Y")
        engine.say(time)
        engine.runAndWait()
        print(time)

def searchwhat(query):   # google search 
    if any(word in query for word in ["what", "why", "when", "where", "how", "who", "which"]):
        query=query.replace("hey","")
        query=query.replace("eva","")
        query=query.replace("can you","")
        query=query.replace("google","")
        query=query.replace("why","")
        query=query.replace("what","")
        query=query.replace("when","")
        query=query.replace("where","")
        query=query.replace("how","")
        query=query.replace("is","")
        query=query.replace("search","")
        engine.say("so, i found this")
        engine.runAndWait()

        try:
            # pw.search(query)
            result=wk.summary(query,sentences=3)
            print(result)
            engine.say(result)
            engine.runAndWait()
            
        except:
            print("")
        
        








        
