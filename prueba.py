import speech_recognition as sr
import pyttsx3
import pyaudio

recognizer = sr.Recognizer()
engine = pyttsx3.init(driverName='espeak',debug=True)
engine.setProperty('voice', 'es')
engine.setProperty('volume', 1.0)

def leeTemp():
    return 'eooooo'

keywords = {
    'hola': 'buenos dias',
    'temperatura': leeTemp,
}

with sr.Microphone() as source:
    print("Habla algo...")
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio, language="es-ES")
    print("Has dicho: " + text)

    for key, response in keywords.items():
        if key in text:
            if callable(response):
                result = response()
                engine.say(result)
                engine.runAndWait()
            else:
                engine.say(response)
                engine.runAndWait()
            
    

    # Guarda las palabras transcritas en un archivo de texto
    with open("transcripcion.txt", "a") as file:
        file.write(text + "\n")

except sr.UnknownValueError:
    print("No se pudo entender el audio")
    engine.say("No se pudo entender el audio")
except sr.RequestError as e:
    print("Error en la solicitud: {0}".format(e))
