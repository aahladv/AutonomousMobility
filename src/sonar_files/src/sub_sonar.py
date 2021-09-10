#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32MultiArray

def callback(lis):

#Implementing the turning logic

	

	if lis.data[0] < 10:
		print('Stop')
	elif lis.data[1] < 10:
		print('Turn Right')
	elif lis.data[2] < 10:
		print('Turn Left')
	else:
		print('Here we go')  

def listener():
	
	rospy.init_node('listener')
	rospy.Subscriber("Sonar_Values", Float32MultiArray, callback) #Here we are linking the rostopics

if __name__ == '__main__':
	listener()
	rospy.spin()

	   

