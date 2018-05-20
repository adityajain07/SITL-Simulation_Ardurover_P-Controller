#!/usr/bin/env python
import rospy 
from std_msgs.msg import String, Float64
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import TwistStamped
from geometry_msgs.msg import Vector3Stamped
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Quaternion
import csv
from math import sin, cos, sqrt, atan2, radians, degrees, pi
import utm
from mavros_msgs.msg import AttitudeTarget
import geopy.distance
from numpy.linalg import norm 
import geopy 
from geopy.distance import VincentyDistance
import numpy as np

######## Author(s): Aditya Jain, Anubhav Jain, Aravinda Kumaran, Rajan Girisa ###########
######## Topic: SITL with ROS, P-Controller #####
######## Date: 17th March, 2018 ########

## Global Variables
inc = 1     # incrementer for the VTP
kp = 0.01     # P gain
curHead = 0  # heading 


# Returns the current heading
def hdgCallback(data):
	global curHead
	curHead = data.data


# This function returns the lat,long of the bot
def posCallback(data):	
	wayList = readWaypoints()
	r = rospy.Rate(1)
	p = [data.latitude, data.longitude] # current locaiton of the bot
 	print "Current Location of Bot", p

	# Getting the current heading
	rospy.Subscriber("/mavros/global_position/compass_hdg", Float64, hdgCallback)
	global curHead		

	# To check distance from the final position
	finalWP = [float(i) for i in wayList[number]]

	finalWP = utm.from_latlon(finalWP[0], finalWP[1] )
	p = utm.from_latlon(p[0], p[1] )

	# thetau = atan2(p[1] - finalWP[1], p[0] - finalWP[0])
	thetau = atan2(finalWP[1] - p[1], finalWP[0] - p[0])
	print "Desired Heading:", degrees(thetau)
	global des
	des = degrees(thetau)
  

def velCallback(data):
	print(data.twist.linear.x)

def location():
	# Subscribing to the (lat, long) of the robot	
	rospy.Subscriber("/mavros/global_position/global", NavSatFix, posCallback)



# Reads the waypoints of the path to be followed and returns it
def readWaypoints():
	wlist = []
	with open('waypoints.txt', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			# print row[0], row[1]
			wlist.append(row)

		return wlist


# Returns the euclidean distance
def euclideanDis(v, w):
	return sqrt((w[1] - v[1])**2 + (w[0] - v[0])**2)


# Returns the euclidean distance between lat/long coordinates
def euclideanDisGPS(v, w):
	v = utm.from_latlon(v[0], v[1] )
	w = utm.from_latlon(w[0], w[1] )
	return sqrt((w[1] - v[1])**2 + (w[0] - v[0])**2)


currAng=0

def heading(msg):
	global currAng
	x = 1
	currAng = msg.data


# Calculates the error in heading
def calculateError(des, curr):		
	theta_cnew = 90 - curr 
	error = des - theta_cnew
	
	error = error%360
	if(error>180):
		error = error -360

	return error 


currLat = 0.0
currLong = 0.0
finalLat = 0.0
finalLong = 0.0

number = 0

def getLoc(data):	

	p = [data.latitude, data.longitude] # current locaiton of the bot

	global currLat
	global currLong
	currLat = data.latitude
	currLong = data.longitude
	
des = 0
def algo():
	
	velocityPub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size = 10)
	headingSub = rospy.Subscriber('/mavros/global_position/compass_hdg',Float64, heading)
	rospy.Subscriber("/mavros/global_position/global", NavSatFix, getLoc)
	rate = rospy.Rate(1) #1 H
	wayList = readWaypoints()
	global finalLong
	global finalLat
	global number
	number =0

	r = rospy.Rate(1)
	location()	

	while not rospy.is_shutdown():
		
		
		finalLat = float(wayList[number][0])
		finalLong = float(wayList[number][1])
	

		pointA = (float(currLat), float(currLong))
		pointD = (float(finalLat), float(finalLong))
		
		Wi1 = utm.from_latlon(currLat, currLat)
		Wi2 = utm.from_latlon(finalLat, finalLong)		

		print 'Des', des
		print 'heading angle', currAng

		error = calculateError(des, currAng)
		print 'error', error

		move = TwistStamped()

		check = euclideanDisGPS(pointD, pointA)

		print "distance from waypoint:", check


		if(check < 7):  # if in the vicinity, then stop giving the control
			move.twist.linear.x = 0
			move.twist.linear.y = 0
			move.twist.angular.z = 0
			velocityPub.publish(move)

			
      # shift to the next waypoint when the current waypoint is reached
			if(number<(len(wayList)-1)):
				number +=1
				print 'len', len(wayList)
				print 'number', number

			
		else:
			move.twist.linear.x = 300
			move.twist.linear.y = 300
			move.twist.angular.z = error*kp
			velocityPub.publish(move)
		
		r.sleep()

	rospy.spin()



###################################################################################



def mainFunc():
	rospy.init_node('carrotpath', anonymous=True)
	algo()


# Main function
if __name__ == '__main__':
	try:
		mainFunc()
	except rospy.ROSInterruptException:
		pass
