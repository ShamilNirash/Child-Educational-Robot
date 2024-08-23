import RPi.GPIO as GPIO
from time import sleep
import speech_recognition as sr
from speech_recognition import Microphone, Recognizer
import pygame
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
from threading import Thread
import random
import time

# GPIO setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)

# Initialize recognizer and pygame
recog = Recognizer()
mic = Microphone()
pygame.mixer.init()

# File paths
welcome_sound_file = "./sounds/welcome song.mp3"
victory_sound_file = "./sounds/victory sound.mp3"
defeat_sound_file = "./sounds/defeat sound.mp3"
end_sound_file = "./sounds/end sound.mp3"
aplphabet_song_file="./sounds/Alphabet song.mp3"
anime_song_file="./sounds/anime song.mp3"
calc_song_file="./sounds/calc song.mp3"
        

def speak(text, lang='en', rate=1):
    tts = gTTS(text=text, lang=lang)
    with BytesIO() as fp:
        tts.write_to_fp(fp)
        fp.seek(0)
        audio = AudioSegment.from_mp3(fp)
        audio = audio._spawn(audio.raw_data, overrides={"frame_rate": int(audio.frame_rate * rate)})
        audio = audio.set_frame_rate(audio.frame_rate)
        play(audio)

def play_background_sound(sound_file, volume):
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
            recog.adjust_for_ambient_noise(mic, duration=1)
            print("waiting ...")
            audio = recog.listen(mic)
            print(audio)
        recognized = recog.recognize_google(audio)
        recognized = recognized.lower()
        print(recognized)
        return recognized
    except sr.UnknownValueError as e:
        print(e)
        return "error"

def stopPlaying(message):
    soundStart(end_sound_file, 0.4)
    time.sleep(2)
    speak(message)
    time.sleep(1)
    stop_background_sound()

def victoryMessage(message):
    soundStart(victory_sound_file, 1)
    time.sleep(3)
    stop_background_sound()
    speak(message)

def errorMessage(message):
    soundStart(defeat_sound_file, 1)
    time.sleep(2)
    stop_background_sound()
    speak(message)

def englishAlphabetTest():
    soundStart(aplphabet_song_file, 0.4)
    time.sleep(1)
    speak("Welcome to the letters  game. I'll give you a letter, and you need to tell a word that starts with it. let's play")
    stop_background_sound()

    while True:
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z']
        random_number = random.randint(0, 25)
        speak(f"Can you say a word starting with letter {alphabet[random_number]}")
        # Adjust the recognizer sensitivity to ambient noise
        englishWord = speechToTxtGet()
        if englishWord == 'error':
            errorMessage("Can't recognize the word")
            continue
        if englishWord == 'stop':
            stopPlaying("Thanks for playing. Goodbye")
            return
        print("You said ", englishWord)
        if englishWord[0] == alphabet[random_number]:
            victoryMessage(f"Great. You said {englishWord}. It's correct")
        else:
            errorMessage(f"No. It is wrong. It starts with letter {englishWord[0]}")

def math_quiz():
    soundStart(calc_song_file, 0.4)
    time.sleep(2)
    speak("Welcome to the Maths game! I'll asked you some math questions, and your get to solve them. Let's start..")
    time.sleep(1)
    stop_background_sound()
    operations = ['plus', 'minus', 'times', 'divided by']
    isBelowTen = True
    while True:
        while isBelowTen:
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
            if answer > 10 or answer < 0:
                isBelowTen = False

        speak(f"What is {num1} {operation} {num2}?")
        user_response = speechToTxtGet()
        print(user_response)

        if user_response == 'stop':
            stopPlaying("Thanks for playing! Goodbye!")
            time.sleep(1)
            return
        if user_response:
            try:
                user_answer = float(user_response)
                if user_answer == answer:
                    victoryMessage(f"Great job! {num1} {operation} {num2} is {answer}.")
                    isBelowTen = True
                else:
                    errorMessage(f"Oops! The correct answer is {answer}.")
                    isBelowTen = True
            except ValueError:
                errorMessage("Sorry, I couldn't understand the number. Please try again.")

def animal_sound_game():
    soundStart(anime_song_file, 0.4)
    time.sleep(2)
    speak("Welcome to the animal game! I'll play and animal sound, and you should guess which animal made it. Let's start..")
    time.sleep(1)
    stop_background_sound()
    animal_sounds = {
        "cow": "./sounds/animal game/cow.wav",
        "dog": "./sounds/animal game/dog.wav",
        "cat": "./sounds/animal game/cat.wav",
        "sheep": "./sounds/animal game/sheep.wav",
        "chicken": "./sounds/animal game/chicken.wav",
        "bird": "./sounds/animal game/bird.wav",
        "eagle": "./sounds/animal game/eagle.wav",
        "horse": "./sounds/animal game/horse.wav",
        "goat": "./sounds/animal game/goat.wav",
        "elephant": "./sounds/animal game/elephant.wav"
    }

    while True:
        animal, sound_file = random.choice(list(animal_sounds.items()))
        speak("What animal makes this sound?")
        soundStart(sound_file, 1)
        time.sleep(4)
        stop_background_sound()
        time.sleep(1)
        guess = speechToTxtGet()

        if guess == 'stop':
            stopPlaying("Thanks for playing! Goodbye!")
            time.sleep(1)
            welcomeSpeech()
        elif guess == 'error':
            errorMessage("Sorry, I couldn't understand the word. Please try again.")
        elif guess == animal:
            victoryMessage(f"Correct! A {animal} makes that sound.")
        else:
            errorMessage(f"Oops! The correct answer is {animal}. A {animal} makes that sound.")

def welcomeSpeech():
    isFirst = True
    soundStart(welcome_sound_file, 0.3)
    time.sleep(2)
    speak("Hi,I'm Buu.Can I know your name buddy? ")
    time.sleep(1)
    stop_background_sound()
    childName = speechToTxtGet()
    soundStart(welcome_sound_file, 0.3)
    time.sleep(1)
    speak(f"Hello {childName}. Let's have some fun today")
    time.sleep(1)
    stop_background_sound()
    while True:
        isNotDetected=True
        speak("We have three super cool games to play.  letters, Maths, animal. Which one do you want to play? ")
        while isNotDetected:
            isNotDetected=False
            gameNumber = speechToTxtGet()
            print(gameNumber)
            if gameNumber == 'stop':
                stopPlaying("Goodbye. See you next time")
                break
            if gameNumber == 'letter' or  gameNumber== 'letters':
                englishAlphabetTest()
            elif gameNumber == 'maths' or gameNumber=='math':
                math_quiz()
            elif gameNumber == 'animal' or gameNumber == 'animals':
                animal_sound_game()
            else:
                speak("ohh ohh. I couldn't get it.Say again")
                isNotDetected=True

if __name__ == '__main__':
    englishAlphabetTest()