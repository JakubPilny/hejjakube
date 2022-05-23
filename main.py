import pyaudio, pyttsx3, json, requests, wikipedia, random, os
from wit import Wit
import speech_recognition as sr
from os import path
from requests import get
from playsound import playsound
from datetime import datetime
from datetime import timedelta

def tts(response):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_csCZ_Jakub")
    engine.say(response)
    engine.runAndWait()

def weather(day):
    ip = get('https://ip.seeip.org').text
    key = [key]
    weatherapi = get("http://api.weatherapi.com/v1/forecast.json?key=" + key + "&q=" + ip + "&days=10&lang=cs")
    weatherjson = weatherapi.json()
    if (day == 0):
        current = weatherjson.get('current')
        currenttemperature = str(int(current.get('temp_c')))
        currentcondition = current.get('condition').get('text').lower()
        return("Aktuálně je " + currentcondition + " s teplotou " + currenttemperature + " stupňů.")
    try:
        forecastday = weatherjson.get('forecast').get('forecastday')[day - 1].get('day')
        maxtemperature = str(int(forecastday.get('maxtemp_c')))
        mintemperature = str(int(forecastday.get('mintemp_c')))
        condition = forecastday.get('condition').get('text').lower()
        forecasttext = condition + " s maximální teplotou " + maxtemperature + " stupňů a minimální teplotou " + mintemperature + " stupňů."
        days = ('pondělí', 'úterý', 'středu', 'čtvrtek', 'pátek', 'sobotu', 'neděli')
        dayofweek = (datetime.now() + timedelta(day - 1)).weekday()
    except Exception as e:
        return("Tak moc do budoucnosti nevidím.")
    if (day == 1):
        return("Dnes bude " + forecasttext)
    elif (day == 2):
        return("Zítra bude " + forecasttext)
    elif (day == 3):
        return("V " + days[dayofweek] + " bude " + forecasttext)
    return("Tak moc do budoucnosti nevidím.")

def wiki(value):
    wikipedia.set_lang("cs")
    search_term = ""
    try:
        return(wikipedia.summary(value, sentences=3))
    except Exception as e:
        try:
            suggest = wikipedia.suggest(value)
            return(wikipedia.summary(suggest, sentences=3))
        except Exception as e:
            return("")
    return("")

def mood():
    moods = ["Všechny nuly a jedničky sedí.", "Nemůže být líp.", "Dobře, doufám, že i tobě.", "Skvěle, díky za optání.", "Daří se mi dobře."]
    return(random.choice(moods))

def callback(recognizer, audio):
    try:
        words = r.recognize_google(audio, language='cs-CZ')
        if "hej jakube" in words.lower():
            try:
                words = words.lower().split("hej jakube ", 1)[1]
                wit(words)
            except Exception as e:
                print("")
    except sr.UnknownValueError:
        print("Google nerozpoznal audio.")
    except sr.RequestError as e:
        print("Nemohla být zaslána žádost na Google. {0}".format(e))

def wit(recognition):
    headers = {'authorization': 'Bearer BGGZW42I23GWLR27K442PVGDRQ3DDW6O'}
    data = requests.get('https://api.wit.ai/message?&q=(%s)' % recognition, headers = headers)
    commands(data)

def commands(resp):
    data = json.loads(resp.content)
    test = resp.json()
    result = json.dumps(test)
    if "time:time" in result:
        now = datetime.now()
        response = "Teď je " + str(now.hour) + "hodin a " + str(now.minute) + "minut."
    elif "date:date" in result:
        now = datetime.now()
        response = "Dnes je " + str(now.day) + "." + str(now.month) + "." + str(now.year)
    elif "date:day" in result:
        now = datetime.now()
        days = ('pondělí', 'úterý', 'středa', 'čtvrtek', 'pátek', 'sobota', 'neděle')
        response = "Dnes je " + days[now.weekday()] + " " + str(now.day) + "." + str(now.month) + "." + str(now.year)
    elif "weather:current" in result:
        response = weather(0)
    elif "weather:today" in result:
        response = weather(1)
    elif "weather:tomorrow" in result:
        response = weather(2)
    elif "weather:forecast" in result:
        days = ('pondělí', 'úterý', 'středu', 'čtvrtek', 'pátek', 'sobotu', 'neděli')
        value = data['entities']['weather:forecast'][0]['value']
        dayofweek = (datetime.now() + timedelta(days.index(value))).weekday()
        if (dayofweek == 0 or dayofweek == 1):
            response = weather(8)
        else:
            response = weather(dayofweek)
    elif "wikipedia:wikipedia" in result:
        value = data['entities']['wikipedia:wikipedia'][0]['value']
        response = wiki(value)
    elif "mood:mood" in result:
        response = mood()
    print(response)
    tts(response)
while True:
    os.system('cls')
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        callback(r,audio)
