engine=pt.init()
voices=engine.getProperty("voices")

#setting up the voice for assistant
engine.setProperty("voices",voices[1].id)
engine.setProperty("rate",200)