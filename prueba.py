import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer()
engine = pyttsx3.init(driverName='espeak')
engine.setProperty('voice', 'es')

with sr.Microphone() as source:
    print("Habla algo...")
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio, language="es-ES")
    print("Has dicho: " + text)

    if 'hola' in text:
        engine.say("Buenas noches")
        engine.runAndWait()

    # Guarda las palabras transcritas en un archivo de texto
    with open("transcripcion.txt", "a") as file:
        file.write(text + "\n")

except sr.UnknownValueError:
    print("No se pudo entender el audio")
except sr.RequestError as e:
    print("Error en la solicitud: {0}".format(e))
