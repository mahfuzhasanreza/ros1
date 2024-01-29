#!/usr/bin/env python3
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math
from turtlesim.srv import SetPen

count = 1
min_dist = 100.0

def call_set_pen_service(r, g, b, width, off):
    try:
        set_pen = rospy.ServiceProxy("/turtle1/set_pen", SetPen)
        set_pen(r, g, b, width, off)
    except rospy.ServiceException as e:
        rospy.logwarn(e)

def pose_callback(msg: Pose):
    cmd = Twist()

    pres_dist = math.dist([msg.x, msg.y], [dest_x, dest_y])
    
    if pres_dist >= 2.5:
        call_set_pen_service(0, 255, 0, 3, 0)
    else:
        call_set_pen_service(255, 0, 0, 3, 0)

    global min_dist
    global count

    if pres_dist <= 0.099999999999999:
        rospy.loginfo("-----HURRAH! REACH THE POINT SUCCESSFULLY-----\n\n")
    elif pres_dist <= 1.0:
        if min_dist >= pres_dist:
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
            cmd.linear.x = 10
            min_dist = pres_dist
        elif msg.theta >= 0.0 and count == 1:
            cmd.angular.z = 5
        elif count == 1:
            count = 2
            min_dist = pres_dist

        if msg.theta <= -1.57 and count == 2:
            cmd.angular.z = 5
        elif count == 2:
            count = 3
            min_dist = pres_dist

        if msg.theta <= 1.57 and count == 3:
            cmd.angular.z = 5
        elif count == 3:
            count = 1
            min_dist = pres_dist

    rospy.loginfo("Destination: (" + str(dest_x) + ", " + str(dest_y) + ")")
    rospy.loginfo("Location: (" + str(msg.x) + ", " + str(msg.y) + ")")
    rospy.loginfo("Distance: " + str(pres_dist))

    pub.publish(cmd)

if __name__ == '__main__':
    rospy.init_node('move_turtle')
    rospy.wait_for_service("/turtle1/set_pen")

    print("\n----------THE DESTINATION COORDINATES----------")
    dest_x = float(input("Enter the X-axis value: "))
    dest_y = float(input("Enter the Y-axis value: "))
    while dest_x > 11.088889122009277 or dest_y > 11.088889122009277:
        rospy.logerr("This coordinates (" + str(dest_x) + ", " + str(dest_y) + ") is not determine at the turtlesim universe")
        rospy.logwarn("Try again! (Values should less than 11.088889122009277)")
        dest_x = float(input("Enter the X-axis value again: "))
        dest_y = float(input("Enter the Y-axis value again: "))

    rospy.Subscriber('/turtle1/pose', Pose, pose_callback)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

    rospy.spin()