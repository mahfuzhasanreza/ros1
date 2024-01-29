#!/usr/bin/env python3
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math

def pose_callback(msg: Pose):
    dest_point = [dest_x, dest_y]
    rospy.loginfo("X==" + str(msg.x) + ", Y==" + str(msg.y))
    
    cmd = Twist()

    pres_dist = math.dist([msg.x, msg.y], dest_point)
    global min_dist
    global count

    if pres_dist <= 0.1:
        rospy.loginfo("----------HURRAH! REACH THE POINT SUCCESSFULLY----------")
    elif pres_dist <= 0.7:
        if min_dist >= pres_dist: # for x axis
            cmd.linear.x = 0.1
            min_dist = pres_dist
        elif msg.theta >= 0.0 and count == 1:
            cmd.angular.z = 0.1
        elif count == 1:
            count = 2
            min_dist = pres_dist

        if msg.theta <= -1.57 and count == 2:
            cmd.angular.z = 0.1
        elif count == 2:
            count = 3
            min_dist = pres_dist
    
        if msg.theta <= 1.57 and count == 3:
            cmd.angular.z = 0.1
        elif count == 3:
            count = 1
            min_dist = pres_dist
    else:
        if min_dist >= pres_dist:
            cmd.linear.x = 0.3
            min_dist = pres_dist
        elif msg.theta >= 0.0 and count == 1:
            cmd.angular.z = 0.1
        elif count == 1:
            count = 2
            min_dist = pres_dist

        if msg.theta <= -1.57 and count == 2:
            cmd.angular.z = 0.1
        elif count == 2:
            count = 3
            min_dist = pres_dist

        if msg.theta <= 1.57 and count == 3:
            cmd.angular.z = 0.1
        elif count == 3:
            count = 1
            min_dist = pres_dist

    rospy.loginfo("Destination: (" + str(dest_x) + ", " + str(dest_y) + ")")
    rospy.loginfo("Location: (" + str(msg.x) + ", " + str(msg.y) + ")")
    rospy.loginfo("Distance: " + str(pres_dist))

    pub.publish(cmd)

if __name__ == '__main__':
    rospy.init_node('move_turtle')

    print("\n----------THE DESTINATION COORDINATES----------")
    dest_x = float(input("Enter the X-axis value: "))
    dest_y = float(input("Enter the Y-axis value: "))
    while dest_x > 11.088889122009277 or dest_y > 11.088889122009277:
        rospy.logerr("This coordinates (" + str(dest_x) + ", " + str(dest_y) + ") is not determine at the turtlesim universe")
        rospy.logwarn("Try again! (Values should less than 11.088889122009277)")
        dest_x = float(input("Enter the X-axis value again: "))
        dest_y = float(input("Enter the Y-axis value again: "))
    count = 1
    min_dist = 100.0

    rospy.Subscriber('/turtle1/pose', Pose, pose_callback)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

    rospy.spin()
