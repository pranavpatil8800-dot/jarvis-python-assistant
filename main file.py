import speech_recognition as sr
from plyer import notification
import pyautogui
import time
from gtts import gTTS
import playsound
import os
import random
import pywhatkit

#   TEXT-TO-SPEECH
def speak(text):
    try:
        filename = f"voice_{random.randint(1000,9999)}.mp3"
        tts = gTTS(text=text, lang='en', tld='co.in')  
        tts.save(filename)

        playsound.playsound(filename)
        os.remove(filename)

    except Exception as e:
        print("TTS Error:", e)


#   SPEECH RECOGNITION 
recognizer = sr.Recognizer()

def command():
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = recognizer.listen(source)

            text = recognizer.recognize_google(audio, language='en-in')
            print("Heard:", text)
            return text.lower()

        except sr.UnknownValueError:
            print("Didn't catch that. Try again...")
        except Exception as e:
            print("Recognition Error:", e)


#    MAIN BRAIN
def main_process():

    while True:
        request = command()

        #     OPEN APPLICATIONS
        if request.startswith("open "):
            app = request.replace("open", "").strip()

            if app:
                speak(f"Opening {app}")

                pyautogui.press("super")
                time.sleep(0.4)
                pyautogui.typewrite(app)
                time.sleep(0.8)
                pyautogui.press("enter")

            time.sleep(1.2)
            continue

        #     GENERAL COMMANDS
        if "hello" in request:
            speak("Hey! I'm veeoola. What can I do for you?")

        elif "add new task" in request:
            task = request.replace("add new task", "").strip()

            if task:
                speak(f"Adding task: {task}")
                with open("new task.txt", "a") as file:
                    file.write(task + "\n")

        elif "speak list" in request:
            try:
                with open("new task.txt", "r") as file:
                    tasks = file.read().strip()

                if tasks:
                    speak("Your tasks are: " + tasks)
                else:
                    speak("Your task list is empty.")

            except FileNotFoundError:
                speak("You don't have a task list yet.")

        elif "show work" in request:
            try:
                with open("new task.txt", "r") as file:
                    tasks = file.read().strip()

                if tasks:
                    notification.notify(
                        title="Today's Tasks",
                        message=tasks,
                        timeout=5
                    )
                else:
                    speak("Your task list is empty.")

            except:
                speak("I couldn't find your task list.")


       

        elif "send whatsapp" in request:
            speak("Who do you want to send the message to?")
            number = command()  

            # Convert spoken digits to real phone number
            number = number.replace(" ", "")
            number = "+91" + number 

            speak("What is the message?")
            msg = command()

            speak(f"Sending message to {number}")
            pywhatkit.sendwhatmsg_instantly(number, msg)
            speak("Message sent")

#   START ASSISTANT
main_process()
