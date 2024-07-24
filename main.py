import speech_recognition
from speech_recognition import Microphone, Recognizer
import pyttsx3
import random
import pygame
from threading import Thread
import time

welcome_sound_file = "./sounds/welcome song.mp3"
victory_sound_file = "./sounds/victory sound.mp3"
defeat_sound_file = "./sounds/defeat sound.mp3"
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


def play_background_sound(sound_file, volume):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)


def stop_background_sound():
    pygame.mixer.music.stop()


def decrease_volume(step=0.01, delay=0.1):
    while pygame.mixer.music.get_volume() > 0.4:
        current_volume = pygame.mixer.music.get_volume()
        new_volume = max(0, current_volume - step)
        if new_volume <= 0.4:
            continue
        pygame.mixer.music.set_volume(new_volume)
        time.sleep(delay)


def soundStart(sound_file, rate):
    sound_thread = Thread(target=play_background_sound, args=(sound_file, rate))
    sound_thread.start()


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
    sound_thread = Thread(target=play_background_sound, args=(welcome_sound_file, 0.4))
    sound_thread.start()
    time.sleep(1)
    speak("Welcome to alphabet game.")
    while (True):
        sound_thread = Thread(target=play_background_sound, args=(welcome_sound_file, 0.4))
        sound_thread.start()
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z']
        random_number = random.randint(0, 25)
        speak(f"can you say a word starting with letter {alphabet[random_number]}")

        # Adjust the recognizer sensitivity to ambient noise
        englishWord = speechToTxtGet()
        stop_background_sound()
        if englishWord == 'error':
            speak("can't recognise the word")
            continue
        if englishWord == 'stop':
            speak("Ok, Now we go to main menu")
            return
        print("you said ", englishWord)
        if englishWord[0] == alphabet[random_number]:
            stop_background_sound()
            soundStart(victory_sound_file,1)
            time.sleep(4)
            stop_background_sound()
            speak(f"Great. you said {englishWord}. Its correct")
        else:
            soundStart(defeat_sound_file,1)
            time.sleep(2)
            stop_background_sound()
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
    isFirst = True
    soundStart(welcome_sound_file, 1)
    time.sleep(2)
    speak("Hello Welcome to the Kids Adventure.")
    while True:
        if isFirst:
            decrease_volume_thread = Thread(target=decrease_volume, args=(0.01, 0.1))  # Decrease by 0.01 every 0.1 seconds
            decrease_volume_thread.start()
            time.sleep(3)
            isFirst=False
        soundStart(welcome_sound_file, 0.4)
        speak("If you want the alphabet game say number 1, If You want the maths game say number 2, If you want to "
              "stop say stop")
        gameNumber = speechToTxtGet()
        stop_background_sound()
        print(gameNumber)
        if gameNumber == 'stop':
            speak("Ok Good Bye")
            time.sleep(1)
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
