#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseArray, Pose

def goalPublisher():
    pub = rospy.Publisher('waypoints', PoseArray, queue_size=10)
    rospy.init_node('goalPublisher', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    
    while not rospy.is_shutdown(): #quand on clique sur le bouton
        point1=Pose()
        point2=Pose()
        Array=PoseArray()
        point1.position.x=666
        point1.position.y=789

        point2.position.x=1042
        point2.position.y=870
        

        Array.poses.append(point1)
        Array.poses.append(point2)
        rospy.loginfo(Array)
        pub.publish(Array)
        rate.sleep()

if __name__ == '__main__':
    try:
        goalPublisher()
    except rospy.ROSInterruptException:
        pass

#[666,789],[1042,870],[501,999],[697,802],
#[1244,728],[1403,200],[865,127],[914,186],[945,217],[995,42]