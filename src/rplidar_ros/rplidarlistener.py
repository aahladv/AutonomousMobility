#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.export PYTHONPATH=$PYTHONPATH:/usr/lib/python2.7/dist-packages
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id$

## Simple talker demo that listens to std_msgs/Strings published 
## to the 'chatter' topic

import rospy
import math
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import LaserScan
from adafruit_servokit import ServoKit 
import time
kit = ServoKit(channels=16)
global ti
ti =time.time()
def callback(data):
	global ti 
	angar = ["not"]
	a=data.ranges
	a=list(a)
	cnt=0
	gavg=0
	average=0
	summ=0
	s= time.time()
	for i in range(-85,86):
		v = a[i]
		if math.isinf(a[i]):
			v = 12
		if a[i]>0.6:
			cnt=cnt+1
		#print type(a[i])
			summ +=v
			if cnt==33:
				average=summ/cnt
				if(average>gavg):
					gavg=average
					cent=round((i-16.5)*(-0.47058823529411764)) + 96
					print('data',cent,gavg)
					angar.pop(0)
					angar.append(cent)		    
				cnt=0
				summ= 0
		    
		    #print('After 17 cnt',i)
		    #print(i)
		else:
			cnt=0
		    
		#print('Less than 2',i)
		#print(i)
    #rospy.loginfo(a)
	print("total time " ,time.time() -ti)    
	ti = time.time()
	print(angar)

	if angar[0]=="not":
		#some angle at wheel \
		kit.continuous_servo.throttle = 0
	else:
			
		kit.servo[0].angle= angar[0]
		kit.continuous_servo[1].throttle = 0.20
	   
	

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
	rospy.init_node('rplisten', anonymous=True)
	global ti

	while not rospy.is_shutdown():
		rospy.Subscriber('scan', LaserScan, callback,queue_size =1)

    # spin() simply keeps python from exiting until this node is stopped
		rospy.spin()

if __name__ == '__main__':
	listener()
