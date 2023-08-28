from gtts import gTTS
from playsound import playsound


text = "UWU"
file_name = 'samplesound/sample6.mp3'
tts_en = gTTS(text=text, lang ='en')
tts_en.save(file_name)


playsound(file_name) 
