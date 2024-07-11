import pyttsx3 as pt
import speech_recognition as sr
import requests
from bs4 import BeautifulSoup
import warnings

engine=pt.init()
voices=engine.getProperty("voices")

#setting up the voice for assistant
engine.setProperty("voices",voices[1].id)
engine.setProperty("rate",200)

#making it to say something when program runs
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takecommand():
    speech=sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        speech.pause_threshold=2     # time for it to pause and litsen to us
        speech.energy_threshold=250                                                  # power of voice it hears( low->nearby voices can also be heared, high->we have to shout)
        audio=speech.listen(source,0,5)                                                  # time for which it will listen to us and the resets after the time(in secs)
        try:                                                                             # exception handling
            print("Recognising and Understanding...")
            query=speech.recognize_google(audio,language='en-in')  
            print("You had said:",query,"\n")                                           # english of India

        except Exception as e:
            print("Speak Again")
            return "None"

        return query

def get_news():
    url = 'https://news.google.com/rss'
    response = requests.get(url)
    try:
        soup = BeautifulSoup(response.content, 'lxml')
    except Exception:
        warnings.filterwarnings("ignore", category=UserWarning, message=".*looks like you're parsing an XML document using an HTML parser.*")
        soup = BeautifulSoup(response.content, 'html.parser')    
    headlines = soup.find_all('item', limit=5)
    news_list = []
    for headline in headlines:
        news_list.append(headline.title.text)
    return news_list

def read_news():
    news_list = get_news()
    engine.say("Here are the top news headlines")
    engine.runAndWait()
    for news in news_list:
        print(news)
        speak(news)

