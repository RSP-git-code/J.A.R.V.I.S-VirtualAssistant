#importing neccesary libraries
import speech_recognition as speech
import pyttsx3
import os
import pywhatkit
import datetime
import wikipedia
import requests
#Clearing the screen
os.system("cls")
listner = speech.Recognizer()
machine = pyttsx3.init()
def talk(text):
    machine.say(text)
    machine.runAndWait()
def input_instructions(mode):
    if mode == "written":
        return get_written_instructions()
    elif mode == "speech":
        try:
            with speech.Microphone() as origin:
                print("Listening...")
                user_speech = listner.listen(origin)
                instructions = listner.recognize_google(user_speech)
                instructions = instructions.lower()
                if "jarvis" in instructions:
                    instructions = instructions.replace('jarvis', '')
                return instructions
        except Exception as e:
            print("Error:", str(e))
            return ""
    else:
        print("Invalid mode input")
        return
def get_written_instructions():
    talk("Enter your command:")
    print("Enter your command:")
    instructions = input().strip()
    return instructions
def extract_location(instructions):
    if "in" in instructions:
        location = instructions.split("in")[-1].strip()
        return location
    else:
        return None
def jarvis_play():
    talk("Hello I am Jarvis how can I help you?")
    instructions = input_instructions(mode)

    if not instructions:
        talk("I didn't catch that. Could you please repeat?")
        return
    
    # Check if the user asked for weather or forecast
    if "weather" in instructions or "forecast" in instructions:
        city = extract_location(instructions) 
        if city:
            weather_info = get_weather(city)
            talk(weather_info)
            print(weather_info)
        else:
            talk("I couldn't understand the location. Please provide a valid city or country.")
            print("I couldn't understand the location. Please provide a valid city or country.")
    
    elif "play" in instructions:
        video = instructions.replace("play", "").strip()
        talk("Playing " + video)
        pywhatkit.playonyt(video)
    elif "time" in instructions:
        time = datetime.datetime.now().strftime('%H:%M%p')
        talk("Current Time: " + time)
        print("Current Time:", time)
    elif "date" in instructions:
        date = datetime.datetime.now().strftime("%m/%d/%y")
        date_format=datetime.datetime.now().strftime("%d/%m/%y")
        talk("Today's date: " + date)
        print("Today's date: " +date_format )
    elif "who are you" in instructions:
        talk("Hello! I'm JARVIS, your virtual assistant.")
        print("Hello! I'm JARVIS, your virtual assistant.")
    elif "translate" in instructions:
        from Translator import translate
        instructions=instructions.replace("jarvis","")
        instructions=instructions.replace("translate"," ")
        translate(instructions)
    elif "who is " in instructions:
        human = instructions.replace("who is", "").strip()
        try:
            info = wikipedia.summary(human, 2)
            talk(info)
            print(info)
        except wikipedia.exceptions.PageError:
            talk(f"Sorry, I couldn't find information about {human} on Wikipedia.")
            print(f"Sorry, I couldn't find information about {human} on Wikipedia.")
    elif "send msg" in instructions:
        send_message() 
    else:
        talk("Can you please repeat? ")
        print("Can you please repeat?")
# Function to get weather information with humorous precautions
def get_weather(city):
    API_KEY = #Enter your generated api key
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = BASE_URL + "q=" + city + "&appid=" + API_KEY + "&units=metric"
    try:
        response = requests.get(complete_url)
        if response.status_code == 200:
            data = response.json()
            main = data['main']
            temperature = main['temp']
            humidity = main['humidity']
            weather_desc = data['weather'][0]['description']
            weather_info = f"The temperature in {city} is {temperature}°C with {weather_desc}. Humidity is {humidity}%."
            if "rain" in weather_desc or "drizzle" in weather_desc:
                weather_info += " It's looking wet out there! Grab an umbrella or get ready to embrace your inner puddle jumper."
            elif "clear" in weather_desc:
                weather_info += " It's a sunny day! Time to show off those shades—and don't forget the sunscreen, unless you enjoy the lobster look."
            elif "snow" in weather_desc:
                weather_info += " Snow is coming! Dress like a marshmallow, or you'll turn into a popsicle out there."
            elif "cloud" in weather_desc:
                weather_info += " It's cloudy! Might not rain, but better safe than soggy—take a jacket, just in case."
            return weather_info
        else:
            return f"Sorry, I couldn't retrieve the weather information for {city}. Error code: 404"
    except requests.exceptions.RequestException as e:
        return f"Error: Unable to get weather data. {str(e)}"
# Function to send automated WhatsApp message
#To send automated message please log in in WhatsApp web and give  minimum time limit range eg:5 min 
def send_message():
    try:
        talk("Are you sending to an individual (I) or group (G)?")
        message_receiver = input("Are you sending to an individual (I) or group (G)? ").capitalize()

        if message_receiver == 'I':
            receiver = input("Enter the phone number of the receiver: ")
            message = input("Enter the message you want to send: ") 
            talk(f"Sending message to {receiver}")
            print(f"Sending message to {receiver}")
            hours = int(input("Input the hour for the automated message (24-hour format): "))
            minutes = int(input("Input the minute for the automated message: "))
            wait_time = int(input("Input the wait time (in seconds): "))
            pywhatkit.sendwhatmsg(receiver, message, hours, minutes, wait_time)
            print("Message sent successfully!")
            talk("Message sent successfully!")

        elif message_receiver == 'G':
            group = input("Enter the group name to send the message: ")
            message_group = input(f"Enter the message you want to send to {group}: ") 
            talk(f"Sending message to {group}")
            print(f"Sending message to {group}")
            hours = int(input("Input the hour for the automated message (24-hour format): "))
            minutes = int(input("Input the minute for the automated message: "))
            wait_time = int(input("Input the wait time (in seconds): "))
            pywhatkit.sendwhatmsg_to_group(group, message_group, hours, minutes, wait_time)
            print("Message sent successfully!")
            talk("Message sent successfully!")

        else:
            talk("Invalid input. Please enter 'I' for an individual or 'G' for a group.")
            print("Invalid input. Please enter 'I' for an individual or 'G' for a group.")

    except Exception as e:
        print(f"Error sending message: {str(e)}")
        talk(f"There was an error sending the message. Please try again later.")
talk("Enter the way to communicate with JARVIS (speech/written):")
mode = input("Enter the way to communicate with J.A.R.V.I.S (speech/written):\n").lower()
#This script is run directly, not when it is imported as a module
if __name__ == '__main__':
    jarvis_play()

