import speech_recognition as sr
import webbrowser
import pyttsx3
from groq import Groq
import time
import os



def jarvis():
    print("hello")
    # Load Groq API key
    client = Groq(api_key=os.getenv('api_key'))

    recognizer = sr.Recognizer()

    def speak(text):
        try:
            engine = pyttsx3.init()
            
            # ✅ Adjust speaking rate (default ~200 wpm)
            engine.setProperty("rate", 160)   # slower = clearer
            
            # ✅ Set volume (0.0 to 1.0)
            engine.setProperty("volume", 1.0)
            
            # ✅ Pick a smoother voice (loop through available voices and choose)
            voices = engine.getProperty("voices")
            for v in voices:
                if "zira" in v.name.lower():     # Microsoft Zira (female, smooth)
                    engine.setProperty("voice", v.id)
                    break
                elif "david" in v.name.lower():  # Microsoft David (male, smooth)
                    engine.setProperty("voice", v.id)
                    break
                elif "mark" in v.name.lower():   # Some systems have Mark (clear male)
                    engine.setProperty("voice", v.id)
                    break
            
            engine.say(text)
            engine.runAndWait()
        except Exception as err:
            print(f"Speech error: {err}")

    def processcommand(c):
        c = c.lower()

        if "sat shri akaal" in c:
            speak("Sat Shri Akaal Resham") 
        
        elif "who made You" in c:
            speak("I was created by Resham Singh")

        elif "open google" in c:
            webbrowser.open_new_tab("https://google.com")

        elif "open youtube" in c:
            webbrowser.open_new_tab("https://youtube.com")

        elif "open personal gmail" in c:
            webbrowser.open_new_tab("https://mail.google.com/mail/u/0/#inbox")

        elif "open chitkara gmail" in c:
            webbrowser.open_new_tab("https://mail.google.com/mail/u/1/#inbox")

        elif "open chat gpt" in c:
            webbrowser.open_new_tab("https://chatgpt.com")

        elif "open facebook" in c:
            webbrowser.open_new_tab("https://facebook.com")

        elif "open linkedin" in c:
            webbrowser.open_new_tab("https://linkedin.com")

        else:
            # Let Groq LLM handle it
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "You are a virtual asistant named jarvis skilled in general tasks like alexa and Google cloud. Give short responses please"},
                        {"role": "user", "content": c}
                    ]
                )
                answer = response.choices[0].message.content
                print("Jarvis:", answer)
                speak(answer)
            except Exception as e:
                print(f"Groq Error: {e}")
                speak("Sorry, I had trouble connecting to Groq.")


    if __name__ == "__main__":
        speak("Initializing Jarvis.....")
        active = False  # Jarvis starts inactive
        last_used = time.time()

        while True:
            try:
                with sr.Microphone() as source:
                    print("Listening...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                word = recognizer.recognize_google(audio).lower()
                print("You said:", word)

                if not active:
                    if "jarvis" in word:
                        active = True
                        last_used = time.time()
                        speak("Yes, I'm here")
                        print("Jarvis Activated...")
                else:
                    if "goodbye jarvis" in word or "jarvis shutdown" in word:
                        speak("Goodbye. Powering off.")
                        break
                    else:
                        processcommand(word)
                        last_used = time.time()

                    if time.time() - last_used > 60:
                        speak("No activity detected. Shutting down.")
                        break

            except Exception as e:
                if active and (time.time() - last_used > 60):
                    speak("No activity detected. Shutting down.")
                    break
                print("Error:", e)

jarvis()