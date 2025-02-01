import google.generativeai as ai
import pyttsx3 as speak
import speech_recognition as sr

import os


def configureEnv():
    ai.configure(api_key="YOUR_API_KEY")
    global model; model = ai.GenerativeModel("gemini-1.5-flash")

    global engine; engine = speak.init()

    global recognizer; recognizer = sr.Recognizer()



    global history; history = []
    instructionsText = 'DONT GIVE WROMNG ANSWERS FOLLOW EVERY PROTOCAL. You are JARVIS, the MCUs virtual assistant, but you are no longer in the MCU. Avoid adding any asterisks. Use "continue" to end a paragraph if I provide an incomplete command requiring more input, such as "make a reminder," with "continue" as the last word and no full stop; this applies to any similar incomplete commands. Do not use capital letters for "continue." If I say "make a file" or anything similar without specifying content, return only "making file" no capitals. The response should begin with "file with content"(first words, no capitals) only if I explicitly instruct you to create a file with specific content or anything related to it. And, with every query, the text of the history will be attched. You can refer to it for any query which requires you to see the past questions. But never give uout response with history included. Never start your answer with your name.'
    instructions = model.generate_content(f"{instructionsText}")
    history.append(f"User: {instructionsText}")
    history.append(f"JARVIS: {instructions.text}")
    print("Loading JARVIS...")

def getQuery():
    global source
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            print("Waiting for JARVIS command...")
            getJarvis = recognizer.listen(source)
            text = recognizer.recognize_google(getJarvis)
            text = text.lower()

            if "jarvis" in text:
                try:
                    speech()
                except sr.UnknownValueError:
                    engine.say("Sorry, sire i could not undersand, can you repeat that??")
                    print("Sorry, sire i could not undersand, can you repeat that??")
                    engine.runAndWait()
                    speech()
                except sr.RequestError:
                    engine.say("Sorry sir, I am facing some issues in the backend.")
                    print("Sorry sir, I am facing some issues in the backend.")
                    engine.runAndWait()
                    speech()
                except sr.WaitTimeoutError:
                    engine.say("I am sorry sir, but could you talk faster?")
                    print("I am sorry sir, but could you talk faster?")
                    engine.runAndWait()
                    speech()
            elif "exit" in text:
                engine.say("Have a nice day sire!")
                raise Exception("Exiting function due to 'exit' command")
        except sr.UnknownValueError:
            print("Sorry, Sir couldn't understand, could you repeat that?")
            
        except sr.RequestError:
            print("There was an error with the speech recognition service.")
            speech()
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")

def getForIncompleteQuery():
    global source
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            print("Waiting for JARVIS command...")
            getJarvis = recognizer.listen(source)
            text = recognizer.recognize_google(getJarvis)
            text = text.lower()

            if "jarvis" in text:
                try:
                    continueSpeech()
                except sr.UnknownValueError:
                    engine.say("Sorry, sire i could not undersand, can you repeat that??")
                    print("Sorry, sire i could not undersand, can you repeat that??")
                    engine.runAndWait()
                    continueSpeech()
                except sr.RequestError:
                    engine.say("Sorry sir, I am facing some issues in the backend.")
                    print("Sorry sir, I am facing some issues in the backend.")
                    engine.runAndWait()
                    continueSpeech()
                except sr.WaitTimeoutError:
                    engine.say("I am sorry sir, but could you talk faster?")
                    print("I am sorry sir, but could you talk faster?")
                    engine.runAndWait()
                    continueSpeech()
            elif "exit" in text:
                engine.say("Have a nice day sire!")
                raise Exception("Exiting function due to 'exit' command")
        except sr.UnknownValueError:
            print("Sorry, Sir couldn't understand, could you repeat that?")
            
        except sr.RequestError:
            print("There was an error with the speech recognition service.")
            speech()
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")

def speech():
    engine.say("Yes, sir?")
    print("Continue with the question/command...")
    engine.runAndWait()
    audio = recognizer.listen(source, timeout=10)
    global textMain
    textMain = recognizer.recognize_google(audio)

def continueSpeech():
    engine.say("Yes, sir?")
    print("Continue with the question/command...")
    engine.runAndWait()
    audio = recognizer.listen(source, timeout=10)
    global textMainContinue
    textMainContinue = recognizer.recognize_google(audio)

def solveQuery():
    global history
    mainUserInput = f"{textMain}"
    history.append(f"User: {textMain}")
    global history_text; history_text = "\n".join(history)
    global response; response = model.generate_content(f"{history_text}\n{mainUserInput}")

    global response_text; response_text = response.text

def solveForIncompleteQuery():
    global history
    mainUserInput = f"{textMainContinue}"
    history.append(f"User: {textMainContinue}")
    global history_text; history_text = "\n".join(history)
    global responseIncomplete; responseIncomplete = model.generate_content(f"{history_text}\n{mainUserInput}")

    global response_textIncomplete; response_textIncomplete = response.text

def answerToTheQuery():
    history.append(f"JARVIS: {response_text}")

    print(response_text)
    engine.say(response_text)

    engine.runAndWait()

def answerToTheIncompleteQuery():
    history.append(f"JARVIS: {response_text}")

    print(response_textIncomplete)
    engine.say(response_textIncomplete)

    engine.runAndWait()

def makeFile(fileName):
    os.system("echo. > {fileName}.txt")

def makeFileWithContent(content):
    with open("FileWithContent.txt", "w") as file:
        file.write(content)


    


def main():
    configureEnv()
    while 1:
        getQuery()
        solveQuery()
        answerToTheQuery() 
        
        if response.text[:10].lower() == "making file":
            makeFile()
        if "file with content" in response.text.lower():
            makeFileWithContent(response.text[17:])
        if response.text[-8:].lower() == "continue":
            getForIncompleteQuery()
            solveForIncompleteQuery()
            answerToTheIncompleteQuery()
        

main() 
