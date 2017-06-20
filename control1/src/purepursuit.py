#!/usr/bin/env python



import rospy
import numpy as np
#from trajectory_planner import Path
from communication.msg import input_model
from communication.msg import mocap_data
from std_msg.msg import PoseArray,Pose

pub=rospy.publish('drive_parameters_topic', input_pid, queue_size=1)
velocity=20
def callback2(waypt)
    # min_dist = 100.0
    # min_point = ref_point = None
    # Ax=0.0
    # Ay=0.0
    # rows=len(traj)
    # for i in rows
    #  Ax=traj[0][i+1]-traj[0][i]
    #  Ay=traj[1][i+1]-traj[1][i]
    #  Bx=state.x-traj[0][i]
    #  By=state.y-traj[1][i]
    #  waylength=np.sqrt(Ax*Ax+Ay*Ay)
    #  Lproj=(Ax*Bx+Ay*By)/waylength
    #  Rx=(Lproj+lookahead)*Ax/waylength+traj[0][i]
    #  Ry=(Lproj+lookahead)*Ay/waylength+traj[1][i]
    #  dist = np.sqrt((state.x - Rx)**2 + (state.y - Ry)**2)
    #  Rad=dist/(2*np.sin(state.yaw))

 rospy.loginfo(waypt)
   msg= inp 
     

#input reference trajectory



if __name__ == '__main__':
    rospy.init_node('purepursuit_node',anonymous=True)
    print('pure-pursuit node is started')
    #rospy.Subscriber("car_state_topic", mocap_data, callback1)
    rospy.Subscriber("way_points",PoseArray,callback2)
 #   rospy.Subscriber("trajectory_topic", mocap_data, callback_traj)
    rospy.spin()


