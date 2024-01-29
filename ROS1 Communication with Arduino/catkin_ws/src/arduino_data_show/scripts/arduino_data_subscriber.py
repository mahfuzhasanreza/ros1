#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

def chatter_callback(msg: String):
    rospy.loginfo("Arduino says: " + str(msg.data))

if __name__ == '__main__':
    rospy.init_node("my_arduino_pub_node")
    sub = rospy.Subscriber("/chatter", String, callback=chatter_callback)

    rospy.loginfo("Subscriber node has been started")

    rospy.spin()