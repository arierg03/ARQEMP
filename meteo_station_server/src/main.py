#!/usr/bin/python3

import string
import rospy
from meteo_station_server.msg import MeteoData
import socket

rospy.init_node('meteo_station', anonymous=True)
pub = rospy.Publisher('meteo_data', MeteoData)
rate = rospy.Rate(10)

def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_address = ('0.0.0.0', 7500)
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Server is listening on {server_address}")

    while True:
        try:
            # Wait for a connection
            print("Waiting for a connection...")
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")

            # Handle the connection
            handle_connection(client_socket)
        finally:
            client_socket.close()
            print(f"Connection with {client_address} closed")

def handle_connection(client_socket):
    # You can customize this function to handle the data received from the client
    while True:
        data = client_socket.recv(8192)
        if not data:
            break
        if data.strip() == "end":
            os._exit(0)
        
        dataArray = str(data).split(';')
        
        if (len(dataArray) < 10):
            rospy.logerr("The meteo data received is invalid")
            rospy.logerr("The data is: " + str(data))
            break
        
        msg = MeteoData()
        msg.temperature = data[0]
        msg.humidity = data[1]
        msg.gasses = data[2]
        msg.light = data[3]
        msg.rain = data[4]
        msg.pressure = data[5]
        msg.internalTemperature = data[6]
        msg.airParticlesDataAtmosferic1 = data[7]
        msg.airParticlesDataAtmosferic2_5 = data[8]
        msg.airParticlesDataAtmosferic10 = data[9]
        pub.publish(msg)

        rospy.loginfo("Published: %s", msg)
        rate.sleep()


if __name__ == '__main__':
    try:
        start_server()
    except rospy.ROSInterruptException:
        pass
