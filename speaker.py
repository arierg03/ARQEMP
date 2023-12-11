import pyttsx3
import rospy
from std_msgs.msg import String
from datetime import datetime  

logs_path = 'say_logs.txt'

#Declaraciones del altavoz
engine = pyttsx3.init(driverName='espeak',debug=True)
engine.setProperty('voice', 'es')
engine.setProperty('volume', 1.0)

#Funcionamiento
def callback(data):
    rospy.loginfo("Recibido: %s", data.data)
    result = data.data
    
    #Inicia la nueva reproduccion
    engine.say(result)
    engine.runAndWait()

    # Construir la línea de log con [fecha - hora] mensaje leído
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{now}] {result}"
    with open(logs_path, "a") as f:
        f.write(log_line + "\n")

    # Publicar el contenido del archivo en el tópico
    with open(logs_path, "r") as f:
        content = f.read()
        log_publisher.publish(content)
    

def listener():
    rospy.init_node('audio', anonymous=True)
    #Inicializamos el publicador para el tópico de logs
    log_publisher = rospy.Publisher('/audio_say_logs', String, queue_size=10)
    rospy.Subscriber('/audio_say', String, callback)
    rospy.spin()

    #Variante de .spin()
    # rate = rospy.Rate(10)  # Frecuencia de bucle (puedes ajustar según sea necesario)
    
    # while not rospy.is_shutdown():
    #     rate.sleep()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
