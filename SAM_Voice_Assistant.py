import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import pyjokes
import random
import os
import json

phrases = ["Alright what's next", "What else can I help you with", "Is there anything else?"]

def speak(audio):
    engine = pyttsx3.init()
    voice = engine.getProperty('voices')
    engine.setProperty('volume', 1)
    engine.setProperty('voice', voice[0].id)
    engine.say(audio)
    engine.runAndWait()
    del(engine)


def greet():
    # Hour in military time
    current_hour = datetime.datetime.now().hour
    if 1 <= current_hour < 12:
        speak("Good morning sir, Welcome Back")
        print("Good morning sir, Welcome Back")
    elif 12 <= current_hour <= 19:
        speak("Good afternoon sir, Welcome Back")
        print("Good afternoon sir, Welcome Back")
    elif 19 < current_hour < 24:
        speak("Good Evening sir, Welcome Back")
        print("Good Evening sir, Welcome Back")
    else:
        speak("Error in getting time")
    
    assistant_name = "SAM"
    speak(f"{assistant_name} here, at your service. How may I assist you?")

def time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"It is currently {current_time}")
    print(f"It is currently: {current_time}")

def date():
    current_date = datetime.datetime.now().strftime("%A, %B %d %Y")
    speak(f"Today is {current_date}")
    print(f"Today is {current_date}")


def listener():
    r = sr.Recognizer()
    

    with sr.Microphone() as source:
        print("Listening...")
        audio_text = r.listen(source, phrase_time_limit=30)
        print("Message Received")

        try:
            print("You said: " + r.recognize_google(audio_text))
            query = r.recognize_google(audio_text).lower()
            # speak("You said: " + r.recognize_google(audio_text))
            return query.lower()
        except:
            print("Sorry, I did not get that")


file = "TODO_list.json"

def load_file():
    if not os.path.exists(file) or os.path.getsize(file) == 0:
        return []
    with open(file, "r") as f:
        return json.load(f)


def save_list(todo):
    with open(file, "w") as f:
        json.dump(todo, f, indent=4)


def show_list():
    todo = load_file()
    if not todo:
        speak("Your TODO List is empty")
    else:
        speak("Here is your TODO list")
        for idx, task in enumerate(todo, start=1):
            print(f"{idx}. {task}")
            speak(task)


def list_listener():
    r = sr.Recognizer()
    todo = load_file()

    with sr.Microphone() as source:
        print("Would you like to add something to your TODO list?")
        speak("Would you like to add something into your todo list?")

        answer = listener()
        if "yes" in answer:
            print("What would you like to add to your TODO?")
            speak("What would you like to add to your TODO?")
            msg_text = r.listen(source, phrase_time_limit=30)
        

            try:
                msg = r.recognize_google(msg_text)
                print(f"You're message to be added was: {msg}")
                todo.append(msg)
                save_list(todo)
                speak(f"You now have {len(todo)} things to do")
            except Exception as e:
                print(f"Sorry didn't get that. Error: {e}")


num_words = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10
}

def extract_number(text):
    text = text.lower()
    for word, num in num_words.items():
        if word in text:
            return num
    digits = ''.join(filter(str.isdigit, text))
    if digits:
        return int(digits)
    return None


def remove_task():
    todo = load_file()

    if not todo:
        speak("Your list is empty. Nothing to remove.")
        return
    
    show_list()
    speak("Which task number would you like to remove?")
    try:
        choice = listener()
        if not choice:
            speak("I didn't catch that")
            return
        
        number = extract_number(choice)
        if number is None:
            speak("Please say a valid task number")
            return
        
        if 1 <= number <= len(todo):
            speak(f"Are you sure you want to remove task number {number}")
            confirm = listener()

            if confirm and "yes" in confirm.lower():
                removed_task = todo.pop(number - 1)
                save_list(todo)
                speak(f"You removed: {removed_task}")
            else:
                speak("Task removal cancelled")
        else:
            speak("That task number is out of range")
    except ValueError:
        speak("Please say a valid task number")
    except Exception as e:
        print(f"Error removing task: {e}")
        speak("I ran into a problem while removing this task")


    



def wiki_search():
        r = sr.Recognizer()
        with sr.Microphone() as source:

            try:
                print("What would you like to search for...")
                speak("What would you like to search for?")
                search_query = r.listen(source)

                search_text = r.recognize_google(search_query)

                print(f"Searching wikipedia for {search_text}...")
                speak(f"Searching wikipedia for {search_text}...")
                result = wikipedia.summary(search_text, sentences = 2)
                speak(result)
                print(result)

            except wikipedia.exceptions.DisambiguationError:
                speak("Multiple results found. Please be more specific.")
            except Exception:
                speak("I couldn't find anything on Wikipedia related to that")


def jokester():
    joke = pyjokes.get_joke()
    print(joke)

    try:
        speak(joke)
    except Exception as e:
        print(f"Speak failed: {e}")




if __name__ == "__main__":
    greet()

    while True:
        query = listener()

        if not query:
            continue

        #DEBUG line
        print(f"Query is -> {query}")

        if "time" in query:
            time()
            num = random.randint(0,len(phrases) - 1)
            print(f"num was: {num}")
            speak(phrases[num])
            continue
        elif "date" in query:
            date()
            num = random.randint(0,len(phrases) - 1)
            print(f"num was: {num}")
            speak(phrases[num])
            continue
        elif "search" in query:
            wiki_search()
            num = random.randint(0,len(phrases) - 1)
            print(f"num was: {num}")
            speak(phrases[num])
            continue
        elif "stop" in query or "shutdown" in query:
            break
        elif "joke" in query.lower():
            jokester()
            speak('Was I funny?')
            num = random.randint(0,len(phrases) - 1)
            print(f"num was: {num}")
            speak(phrases[num])
        elif "to do list" in query:
            list_listener()
            speak("Would you like to view everything on your TODO list?")
            response = listener()
            if "yes" in response:
                show_list()
                num = random.randint(0, len(phrases) - 1)
                speak(phrases[num])
            else:
                speak("Ok, moving on")
                num = random.randint(0, len(phrases) - 1)
                speak(phrases[num])
        elif "remove task" in query or "delete task" in query:
            remove_task()
            





