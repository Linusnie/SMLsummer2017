#!/usr/bin/env python
'''
Node to determine deviation from trajectory.

'''

import rospy
import numpy as np
from slip_control_communications.msg import out_pursuit
from slip_control_communications.msg import input_pid
from slip_control_communications.msg import mocap_data

pub = rospy.Publisher('error_topic', input_pid, queue_size=10)
#-------------------------------------------------------------------------------
# callback
#
# INPUT:
#   state: measurements derived from mocap
#------------------------------------------------------------------------------
global flag
v_desired=0
yaw_rate_desired=0
flag=0

def callback1(traj):
    global v_desired 
    global yaw_rate_desired
    global flag
    v_desired=traj.velocity_req
    yaw_rate_desired=traj.yaw_rate_req
    flag=1


def callback2(state):
    global v_desired 
    global yaw_rate_desired
    global flag
    if flag ==1:
      vel_error=3.0
      angle_error=6.0
      msg = input_pid()
      msg.error_velocity = vel_error
      msg.error_yaw_rate = angle_error
      rospy.loginfo(msg)
      pub.publish(msg)
 #     x=state.x
 #     y=state.y
 #     t=state.ts
 #     if prev_x == None:
 #        delta_x = 0
 #     else:
 #        delta_x = x - prev_x
 #    prev_x=x

 #    if prev_y == None:
 #        delta_y = 0
 #     else:
 #        delta_y = y - prev_y
 #    prev_y=y

 #    if prev_t == None:
 #        delta_t = 0
 #     else:
 #        delta_t = t - prev_t
 #    prev_t=t


 # velocity= np.sqrt(delta_x*delta_x+delta_y*delta_y)/delta_t
    


#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    rospy.init_node('error_calculation_node', anonymous=True)
    print("error is calculated")
    rospy.Subscriber("trajectory_request",out_pursuit,callback1)
    rospy.Subscriber("car_state_topic", mocap_data, callback2)
    rospy.spin()
