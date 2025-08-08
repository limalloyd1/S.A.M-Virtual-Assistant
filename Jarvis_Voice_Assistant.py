import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia



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



if __name__ == "__main__":
    greet()

    while True:
        query = listener()

        if "time" in query:
            time()
            speak("What else would you like to do?")
            continue
        elif "date" in query:
            date()
            speak("What else would you like to do?")
            continue
        elif "search" in query:
            wiki_search()
            speak("What else would you like to do?")
            continue
        elif "stop" or "shutdown" in query:
            break
        elif listening == False:
            break

    

# TODO: Make wiki_search() functionality work more consistently 



# greet()

# time()

# listener()





