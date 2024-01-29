#include <ros.h>
#include <std_msgs/String.h>

ros::NodeHandle  nh;

std_msgs::String str_msg;
ros::Publisher chatter("chatter", &str_msg);

void setup() {
  nh.initNode();
  nh.advertise(chatter);
}

int i = 0;
void loop() {
  i++;
  if(i == 100) i = 0;
  char int_str[100];
  sprintf(int_str, "%d", i);
  
  char str[100] = "Hello ROS - ";
  strcat(str, int_str);

  str_msg.data = str;
  chatter.publish( &str_msg );
  nh.spinOnce();
}