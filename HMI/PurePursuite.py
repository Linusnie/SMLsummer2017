#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseArray, Pose

def callback(data):

	
    rospy.loginfo(data.poses[0].position.x)
    rospy.loginfo(type(data.poses[0].position.x))

def WaypointsListener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('WaypointsListener', anonymous=True)

    rospy.Subscriber('waypoints', PoseArray, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    WaypointsListener()
