import speech_recognition
from speech_recognition import Microphone, Recognizer
import pyttsx3
import random

# Initialize recognizer
recog = Recognizer()
mic = Microphone(device_index=0)
tts_engine = pyttsx3.init()
speech_rate = tts_engine.getProperty('rate')
new_speech_rate = 150
tts_engine.setProperty('rate', new_speech_rate)
voices = tts_engine.getProperty('voices')
tts_engine.setProperty('voice', voices[0].id)
recognized = ''


def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()


def speechToTxtGet():
    try:
        with mic:
            print("waiting ...")
            audio = recog.listen(mic)
            print(audio)

        recognized = recog.recognize_google(audio)
        recognized = recognized.lower()
        return recognized
    except speech_recognition.UnknownValueError as e:
        print(e)
        return "error"


def englishAlphabetTest():
    while (True):
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z']
        random_number = random.randint(0, 25)
        speak(f"can you say a word starting with letter {alphabet[random_number]}")

        # Adjust the recognizer sensitivity to ambient noise
        englishWord = speechToTxtGet();
        if englishWord=='error':
            speak("can't recognise the word")
            continue
        if englishWord == 'stop':
            speak("Ok, Now we go to main menu")
            return
        print("you said ", englishWord)
        if englishWord[0] == alphabet[random_number]:
            speak(f"Great. you said {englishWord}. Its correct")
        else:
            speak(f"no. it is wrong. it start with letter {englishWord[0]}")


def welcomeSpeech():
    speak("Hello Welcome to the Kids Adventure.")
    while (True):
        speak("If you want the alphabet game say number 1, If You want the maths game say number 2, If you want to "
              "stop say stop")
        gameNumber = speechToTxtGet()
        print(gameNumber)
        if gameNumber == 'stop':
            speak("Ok Good Bye");
            break
        if gameNumber == 'number one' or gameNumber == 'number 1':
            englishAlphabetTest()
        elif gameNumber == 'number two' or gameNumber == 'number 2':
            speak("not build")
        else:
            speak("say again")


if __name__ == '__main__':
    welcomeSpeech()
