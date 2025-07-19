import speech_recognition as sr
import webbrowser
import pyttsx3
import wikipedia 
import requests
import musiclibrary  # Ensure this exists

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "0fb2df630b324c629e95f3d6320595d2"  # Replace with a secure method if needed

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    """Process the user's voice command."""
    c = c.lower()

    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open instagram" in c:
        webbrowser.open("https://instagram.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif c.startswith("play"):
        song = c.split(" ", 1)[1]
        if song in musiclibrary.music:
            webbrowser.open(musiclibrary.music[song])
        else:
            speak(f"Sorry, I couldn't find {song} in the music library.")
    elif "news" in c:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            articles = r.json().get('articles', [])
            for article in articles[:5]:  # Limit to first 5 news headlines
                speak(article['title'])
    elif "who is" in c or "what is" in c or "tell me about" in c:
        query = c.replace("who is", "").replace("what is", "").replace("tell me about", "").strip()
        try:
            summary = wikipedia.summary(query, sentences=2)  # Fetch 2-sentence summary
            speak(summary)
            print(summary)
        except wikipedia.exceptions.DisambiguationError as e:
            speak("There are multiple results. Can you be more specific?")
        except wikipedia.exceptions.PageError:
            speak("Sorry, I couldn't find any information on that.")
    elif "exit" in c or "stop" in c:
        speak("Goodbye!")
        exit()

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for 'Jarvis'...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            
            word = recognizer.recognize_google(audio).lower()
            if word == "jarvis":
                speak("Yes, how can I assist you?")
                with sr.Microphone() as source:
                    print("Listening for command...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source)
                
                command = recognizer.recognize_google(audio)
                processCommand(command)

        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError:
            print("Could not request results; check your internet connection.")
        except Exception as e:
            print(f"Error: {e}")
