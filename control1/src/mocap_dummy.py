#!/usr/bin/env python

import rospy
from slip_control_communications.msg import mocap_data

def talker():
     rospy.init_node('mocap_publisher_node', anonymous=True)
     pub = rospy.Publisher('car_state_topic', mocap_data, queue_size=10)
     rate = rospy.Rate(10) # 10hz
     data = mocap_data()

     while not rospy.is_shutdown():
        data.ts = 1
        data.id = 2
        data.x =  3
        data.y = 4
        data.z = 5
        data.roll = 6
        data.pitch = 7
        data.yaw = 8
        rospy.loginfo(data)
        pub.publish(data)
        rate.sleep()
      

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass