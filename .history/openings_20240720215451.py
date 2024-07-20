import os
import pyautogui as pg
import webbrowser as wb
from gtts import gTTS
import pygame
import tempfile
import streamlit as st


def openwebapp(query):
    if ".com" in query or ".co" in query or ".org" in query or ".in" in query:
        query = query.replace('open', "").replace(" ", '')
        wb.open(f"https://www.{query}")

def closewebapp(query):
    if "one tab" in query or "1 tab" in query or "tab" in query:
        st.write('closing the tab')
        
