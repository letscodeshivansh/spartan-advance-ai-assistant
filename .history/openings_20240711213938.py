import os
import pyautogui as pg
import webbrowser as wb 
import pyttsx3 as pt
engine=pt.init()
voices=engine.getProperty("voices")
engine.setProperty("voices",voices[1].id)
engine.setProperty("rate",200)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def openwebapp(query):
    if ".com" in query or ".co" in query or ".org" in query or ".in"  in query:
        query=query.replace('open',"")
        query=query.replace(" ",'')
        speak(query)
        wb.open(f"https://www.{query}")

def closewebapp(query):
    if "one tab" in query or "1 tab" in query or "tab" in query:
        speak('closing the tab')
        pg.hotkey("ctrl","w") # to close any tab, we can type ctrl+w, this will close the tab
        
    














        


    
