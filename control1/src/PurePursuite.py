#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseArray, Pose
from slip_control_communications.msg import out_pursuit
from slip_control_communications.msg import mocap_data


pub = rospy.Publisher('trajectory_request', out_pursuit, queue_size=10)

x_d=0
y_d=0
flag=0
def callback1(data):
    global x_d
    global y_d
    global flag	
    rospy.loginfo(data.poses[0].position.x)
    rospy.loginfo(type(data.poses[0].position.x))
    flag=1

def callback2(state):
    yaw_rate=2.0
    velocity=3.0
    msg=out_pursuit()
    msg.yaw_rate_req=yaw_rate
    msg.velocity_req=velocity
    rospy.loginfo(msg)
    pub.publish(msg)

def WaypointsListener():

    rospy.init_node('WaypointsListener', anonymous=True)
    print("listening to way-points")

    rospy.Subscriber('waypoints', PoseArray, callback1)
    rospy.Subscriber("car_state_topic", mocap_data, callback2)


    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    WaypointsListener()
