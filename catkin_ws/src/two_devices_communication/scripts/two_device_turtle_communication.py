#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

def pose_callback(pose: Pose):
    cmd = Twist()
    
    cmd.linear.x = 8.0
    cmd.angular.z = 8.0
    
    pub.publish(cmd)


if __name__ == '__main__':
    rospy.init_node("turtle_controller")
    
    pub  = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
    sub = rospy.Subscriber("/turtle1/pose", Pose, callback=pose_callback)

    rospy.spin()