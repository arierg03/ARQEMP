from cgitb import text
import speech_recognition as sr
import pyttsx3
import pyaudio
import rospy
from robotnik_msgs.msg import BatteryStatus

recognizer = sr.Recognizer()
engine = pyttsx3.init(driverName='espeak',debug=True)
engine.setProperty('voice', 'es')
engine.setProperty('volume', 1.0)

def leeNivelBateria():
    def callback(data):
        mensaje = f"El nivel de la bateria es: {str(int(data.level))}"
        rospy.loginfo(mensaje) 
        rospy.signal_shutdown('Nivel de bateria recibido')
        return mensaje
    rospy.init_node('listenerBateria', anonymous=True)
    rospy.Subscriber("/robot/battery_estimator/data", BatteryStatus, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

keywords = {
    'hola': 'buenos dias',
    'nivel de batería': leeNivelBateria,
    'batería': leeNivelBateria,
}

#with sr.Microphone() as source:
    #print("Habla algo...")
    #audio = recognizer.listen(source)

try:
    #text = recognizer.recognize_google(audio, language="es-ES")
    text = 'batería'
    print("Has dicho: " + text)

    for key, response in keywords.items():
        if key in text:
            if callable(response):
                result = response()
                print(result)
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
