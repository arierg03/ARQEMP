#!/usr/bin/env python
import rospy
from robotnik_msgs.msg import String, BatteryStatus

def callback(data):
  rospy.loginfo("El nivel de la bateria es: " + data.level)
def listener():
  rospy.init_node('listenerBateria', anonymous=True)
  rospy.Subscriber("/robot/battery_estimator/data", BatteryStatus, callback)
  # spin() simply keeps python from exiting until this node is stopped
  rospy.spin()
if __name__ == ’__main__’:
  listener()
