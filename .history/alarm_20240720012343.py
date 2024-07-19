import datetime
import os
import time
import threading
from gtts import gTTS
import pygame
import tempfile
from playsound import playsound
# Initialize pygame mixer for audio playback
pygame.mixer.init()

def speak(audio):
    tts = gTTS(text=audio, lang='en')
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts.save(fp.name + ".mp3")
        pygame.mixer.music.load(fp.name + ".mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

def set_alarm(alarm_time, sound_file):
    alarm_hour, alarm_minute = map(int, alarm_time.split(":"))

    print("Alarm is set for {}:{}".format(alarm_hour, alarm_minute))

    while True:
        now = datetime.datetime.now()
        if now.hour == alarm_hour and now.minute == alarm_minute:
            print("Wake Up!")
            speak("Wake Up!")
            os.system("start " + sound_file)
            break
        time.sleep(1)
