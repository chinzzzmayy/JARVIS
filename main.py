import google.generativeai as ai
import pyttsx3 as speak
import speech_recognition as sr
import os


def Configure():
	ai.configure(api_key="YOUR_API_KEY")
	global model; model = ai.GenerativeModel("gemini-1.5-flash")

	global engine; engine = speak.init()

	global recognizer; recognizer = sr.Recognizer()

	

	global history; history = []
	instructionsText = 'Avoid adding any asterisks. Use "continue" to end the paragraph (continue in the last word, dont continue with a fullstop) if I provide a question like "make a reminder", which makes me have the need to give a second field, such as the time. This does not mean that you have to use continue for only a reminder. And also for the continue word, dont use any capital letters. JARVIS, THE MCUS VIRTUAL ASSISTANT, IS YOU. Normally, you,re not in the MCU anymore. In the event that I say "make a file" or anything similar, you must return the file as the only output. The response should begin with "file with content" and then include the content if I instruct you to create a file with the content or anything associated with it.'
	instructions = model.generate_content(instructionsText)
	history.append(f"User: {instructionsText}")
	history.append(f"JARVIS: {instructions.text}")
	print("Okay, Got it!")

def getSpeech():
	global source
	with sr.Microphone() as source:
		recognizer.adjust_for_ambient_noise(source, duration=1)
		try:
			print("Waiting for JARVIS command...")
			getJarvis = recognizer.listen(source)
			text = recognizer.recognize_google(getJarvis)
			text = text.lower()

			if "jarvis" in text:
				print("Continue with the question/command...")
				audio = recognizer.listen(source, timeout=10)

				global textMain
				textMain = recognizer.recognize_google(audio)
				
			elif "exit" in text:
				engine.say("Have a nice day sire!")
				raise Exception("Exiting function due to 'exit' command")
		except sr.UnknownValueError:
			print("Sorry, I couldn't understand the audio.")
		except sr.RequestError:
			print("There was an error with the speech recognition service.")
		except sr.WaitTimeoutError:
			print("Timeout: No speech detected.")

def answer():
	global history
	mainUserInput = f"{textMain}"
	history.append(f"User: {textMain}")
	history_text = "\n".join(history)
	global response; response = model.generate_content(f"{history_text}\n{mainUserInput}")

	response_text = response.text
	history.append(f"JARVIS: {response_text}")

	print(response_text)
	engine.say(response_text)

	engine.runAndWait()


def makeFile():
	os.system("echo. > fileByJarvis.txt")


def makeFileWithContent(content):
	with open("FileWithContent.txt", "w") as file:
		file.write(content)


def main():
	Configure()
	
	while 1:
		getSpeech()
		answer()
		if "making file" in response.text.lower():
			makeFile()
		if "file with content" in response.text.lower():
			makeFileWithContent(response.text[17:])
		
main()
