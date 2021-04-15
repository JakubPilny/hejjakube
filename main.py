from wit import Wit
import pyaudio
import pyttsx3
import speech_recognition as sr
from os import path
import os
from requests import get
import json
from playsound import playsound
import datetime
import requests
import wikipedia

def tts(response):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_csCZ_Jakub")
    engine.say(response)
    engine.runAndWait()

def weather(call,additional):
    ip = get('https://ip.seeip.org').text
    key = [key]
    api = call + key + "&q=" + ip + additional + "&lang=cs"
    weatherplain = get(api)
    wjson = weatherplain.json()
    if "current" in call:
        temperature = wjson.get('current').get('temp_c')
        condition = wjson.get('current').get('condition').get('text').lower()
        weather = condition + " s teplotou " + str(temperature) + " stupňů."
    else:
        maxtemperature = str(wjson.get('forecast').get('forecastday')[0].get('day').get('maxtemp_c'))
        mintemperature = str(wjson.get('forecast').get('forecastday')[0].get('day').get('mintemp_c'))
        condition = wjson.get('forecast').get('forecastday')[0].get('day').get('condition').get('text').lower()
        if "-" in str(mintemperature):
            mintemperature = "mínus " + mintemperature[1:]
        weather = condition + " s minimální teplotou " + mintemperature + " stupňů a maximální teplotou " + maxtemperature + " stupňů."
    return(weather)

def wiki(body):
    wikipedia.set_lang("cs")
    response = ""
    search_term = ""
    try:
        search_term = body.lower().split("wikipedia ", 1)[1]
    except Exception as e:
        return("")
    try:
        response = wikipedia.summary(search_term, sentences=3)
    except Exception as e:
        try:
            suggest = wikipedia.suggest(search_term)
            response = wikipedia.summary(suggest, sentences=3)
        except Exception as e:
            print("")
    return response

def callback(recognizer, audio):
    try:
        words = r.recognize_google(audio, language='cs-CZ')
        if "hej jakube" in words.lower():
            wit(words)
    except sr.UnknownValueError:
        print("Google nerozpoznal audio.")
    except sr.RequestError as e:
        print("Nemohla být zaslána žádost na Google. {0}".format(e))

def wit(recognition):
    API_ENDPOINT = 'https://api.wit.ai/speech'
    ACCESS_TOKEN = 'BGGZW42I23GWLR27K442PVGDRQ3DDW6O'
    headers = {'authorization': 'Bearer ' + ACCESS_TOKEN}
    resp = requests.get('https://api.wit.ai/message?&q=(%s)' % recognition, headers = headers)
    data = json.loads(resp.content)
    test = resp.json()
    result = json.dumps(test)
    if "time:time" in result:
        now = datetime.datetime.now()
        response = "Teď je " + str(now.hour) + "hodin a " + str(now.minute) + "minut."
        print(response)
        tts(response)
    elif "date:date" in result:
        now = datetime.datetime.now()
        response = "Dnes je " + str(now.day) + "." + str(now.month) + "." + str(now.year)
        print(response)
        tts(response)
    elif "weather:current" in result:
        additional = ""
        call = "http://api.weatherapi.com/v1/current.json?key="
        response = weather(call,additional)
        text = "Aktuálně je " + response
        print(text)
        tts(text)
    elif "weather:tomorrow" in result:
        additional = "&days=1"
        call = "http://api.weatherapi.com/v1/forecast.json?key="
        response = weather(call,additional)
        text = "Zítra bude " + response
        print(text)
        tts(text)
    elif "wit$wikipedia_search_query:wikipedia_search_query" in result:
        body = data['entities']['wit$wikipedia_search_query:wikipedia_search_query'][0]['body']
        response = wiki(body)
        print(response)
        tts(response)

while True:
    os.system('cls')
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        callback(r,audio)
