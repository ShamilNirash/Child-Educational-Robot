import speech_recognition
from speech_recognition import Microphone, Recognizer
import pyttsx3
import random
import pygame

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

def play_sound(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue


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

def math_quiz():
    speak("Welcome to the math quiz! Let's start..")
    operations = ['plus', 'minus', 'times', 'divided by']
    
    while True:
        while True:
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            operation = random.choice(operations)
            
            if operation == 'plus':
                answer = num1 + num2
            elif operation == 'minus':
                answer = num1 - num2
            elif operation == 'times':
                answer = num1 * num2
            elif operation == 'divided by':
                answer = num1 / num2
            
            if answer >= 10 or answer < 0:
                break

        speak(f"What is {num1} {operation} {num2}?")
        user_response = speechToTxtGet()
        
        if user_response == 'stop':
            speak("Thanks for playing! Goodbye!")
            break
        
        if user_response:
            try:
                user_answer = float(user_response)
                if user_answer == answer:
                    speak(f"Great job! {num1} {operation} {num2} is {answer}.")
                else:
                    speak(f"Oops! The correct answer is {answer}.")
            except ValueError:
                speak("Sorry, I couldn't understand the number. Please try again.")

def animal_sound_game():
    speak("Welcome to the animal sounds guessing game! Let's start..")
    animal_sounds = {
        "cow": "Sounds/cow.wav",
        "dog": "Sounds/dog.wav",
        "cat": "Sounds/cat.wav",
        "sheep": "Sounds/sheep.wav",
        "duck": "Sounds/duck.wav",
        "bird": "Sounds/bird.wav",
        "chicken": "Sounds/chicken.wav",
        "horse": "Sounds/horse.wav",
        "owl": "Sounds/owl.wav"
    }
    
    while True:
        animal, sound_file = random.choice(list(animal_sounds.items()))
        speak("What animal makes that sound?")
        play_sound(sound_file)
        guess = speechToTxtGet()

        if guess == 'stop':
            speak("Thanks for playing! Goodbye!")
            welcomeSpeech()
            break
        
        if guess == animal:
            speak(f"Correct! A {animal} makes that sound.")
        else:
            speak(f"Oops! The correct answer is {animal}. A {animal} makes that sound.")


def welcomeSpeech():
    speak("Hello Welcome to the Kids Adventure.")
    while (True):
        speak("If you want to play alphabet game say number 1, If You want to play maths game say number 2, If you want to "
              "play animal sound guessing game say number 3, if you want to stop say stop")
        gameNumber = speechToTxtGet()
        print(gameNumber)
        if gameNumber == 'stop':
            speak("Ok Good Bye")
            break
        if gameNumber == 'number one' or gameNumber == 'number 1':
            englishAlphabetTest()
        elif gameNumber == 'number two' or gameNumber == 'number 2':
            math_quiz()
        elif gameNumber == 'number three' or gameNumber == 'number 3':
            animal_sound_game()
        else:
            speak("say again")

if __name__ == '__main__':
    welcomeSpeech()
