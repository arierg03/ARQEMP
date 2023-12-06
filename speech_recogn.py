from cgitb import text
import speech_recognition as sr
import pyttsx3
import rospy
from robotnik_msgs.msg import BatteryStatus
from std_msgs.msg import String
from datetime import datetime  


#Variables globales necesarias
logs_path = 'speech_recogn.txt'
...

#Declaramos el recognizer y el altavoz
log_publisher = rospy.Publisher('audio/speech_recogn_logs', String, queue_size=10)
recognizer = sr.Recognizer()
engine = pyttsx3.init(driverName='espeak',debug=True)
engine.setProperty('voice', 'es')
engine.setProperty('volume', 1.0)

#Funciones de lectura de tópicos
#Función que lee el nivel de la bateria
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
#Función que lee cuanto queda de batería
def leeTiempoRestanteBateria():
    def callback(data):
        mensaje = f"El tiempo restante de la bateria es: {str(int(data.level))}"
        rospy.loginfo(mensaje) 
        rospy.signal_shutdown('Nivel de bateria recibido')
        return mensaje
    rospy.init_node('listenerBateria', anonymous=True)
    rospy.Subscriber("/robot/battery_estimator/data", BatteryStatus, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

#Diccionario de palabras clave para detectar en el audio escuchado
keywords = {
    'hola': 'buenos dias',
    'nivel de batería': leeNivelBateria,
    'nivel de la batería': leeNivelBateria,
    'queda de batería': leeTiempoRestanteBateria,
    'tiempo restante de batería': leeTiempoRestanteBateria,
    'tiempo restante de la batería': leeTiempoRestanteBateria,
}

while not rospy.is_shutdown():  # Bucle principal hasta que se reciba una señal de parada
    with sr.Microphone() as source:
        print("Habla algo...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="es-ES")

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
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{now}] {text}"
        with open(logs_path, "a") as file:
            file.write(log_line + "\n")

        # Publicar el contenido del archivo en el tópico
        with open(logs_path, "r") as f:
            content = f.read()
            log_publisher.publish(content)
        
    except sr.UnknownValueError:
        print("No se pudo entender el audio")
        engine.say("No se pudo entender el audio")
    except sr.RequestError as e:
        print("Error en la solicitud: {0}".format(e))
