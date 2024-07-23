from speech_recognition import Microphone, Recognizer
import pyttsx3
import random
# Initialize recognizer
recog=Recognizer()
mic=Microphone(device_index=0)
little=''
tts_engine = pyttsx3.init()
speech_rate = tts_engine.getProperty('rate')
new_speech_rate = 150
tts_engine.setProperty('rate', new_speech_rate)
voices = tts_engine.getProperty('voices')
tts_engine.setProperty('voice', voices[1].id)
recognized=''
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()
# Capture audio from the microphone
speak("Hello Welcome to the alphabet Adventure")
while(recognized!='stop'):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    random_number = random.randint(0, 25)
    speak(f"can you say a word starting with letter {alphabet[random_number]}")
    with mic:
        print("waiting ...")
        audio=recog.listen(mic)
        print(audio)
        # Adjust the recognizer sensitivity to ambient noise
    recognized=recog.recognize_google(audio)
    recognized=recognized.lower()
    print("you said ", recognized)
    if(recognized[0]==alphabet[random_number]):
        speak(f"Great. you said {recognized}. Its correct")
    else:
        speak(f"no it start with letter {recognized[0]}")



