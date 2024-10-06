from googletrans import Translator
from gtts import gTTS
import os
import pyttsx3
import googletrans
machine = pyttsx3.init()
def talk(text):
    machine.say(text)
    machine.runAndWait()
def translate(instructions):
    talk("Translating the sentence...")
    translator = Translator()
    try:
        # Prompt the user to choose the  required language
        talk("Choose the language in which you want to translate:")
        print("Choose the language in which you want to translate:")
        # Displaying the language codes available
        print(googletrans.LANGUAGES)
        print("Please look in the available languages dictionary and enter the code correctly:\n")
        req_lang = input("To Language (code):\n")  
        # Translate the given text
        text_to_translate = translator.translate(instructions, src="auto", dest=req_lang)
        translated_text = text_to_translate.text
        talk(f"Translation: {translated_text}")
        print(f"Translated Text: {translated_text}")
        # Use Google Text-to-Speech (gTTS) to speak the translated text
        speak = gTTS(text=translated_text, lang=req_lang, slow=False)
        #saving the audio file
        speak.save("translated_output.mp3") 
         # Automatically playing  the translated text 
        os.system("start translated_output.mp3") 
    except Exception as e:
        talk("Sorry, I am unable to translate the sentence. Please try again.")
        print(f"Error: Unable to translate. {str(e)}")
