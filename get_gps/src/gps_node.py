#! /usr/bin/env python

import rospy
import numpy as np
import serial
from get_gps.msg import gps_reach
from sensor_msgs.msg import NavSatFix

def receiver():
	port = rospy.get_param('~port', '/dev/ttyACM0')
	
	try:
		ser = serial.Serial(port=port, baudrate=115200, timeout=1)
	except serial.serialutil.SerialException:
		ser = serial.Serial("dummy_gps.txt", baudrate=115200, timeout=1)


	rospy.init_node('gps_receiver', anonymous=True)
	pub_reach = rospy.Publisher('gps_reach', gps_reach, queue_size=10)
	pub_navSat = rospy.Publisher('gps_navsat', NavSatFix, queue_size=10)

	solution_types = ['fixed', 'float', 'reserved', 'DGPS', 'single']
	
	gps = gps_reach()
	navsat = NavSatFix()
	while not rospy.is_shutdown():
		line = ser.readline()
		words = line.split()

		if len(words) == 15:
			gps.date = words[0]
			gps.time = words[1]
			
			gps.latitude = float(words[2])
			gps.longitude = float(words[3])
			gps.height = float(words[4])

			navsat.latitude = float(words[2])
			navsat.longitude = float(words[3])
			navsat.height = float(words[4])
			
			gps.solution = solution_types[int(words[5])-1] 
			gps.num_satelites = int(words[6])
			
			gps.stn = float(words[7])
			gps.ste = float(words[8])
			gps.stu = float(words[9])
			gps.stne = float(words[9])
			gps.steu = float(words[10])
			gps.stun = float(words[11])

			navsat.position_covariance = [gps.stn,  gps.stne, gps.stun,
				 gps.stne, gps.ste,  gps.steu,
				 gps.stun, gps.steu, gps.stu]
			
			gps.age = float(words[12])
			gps.ratio = float(words[13])

		pub_reach.publish(gps)
		pub_navsat.publish(navsat)

receiver()
