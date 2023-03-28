#!/usr/bin/python3  
import rospy
import math
import tf2_ros
from turtlesim.msg import Pose
from tf.transformations import euler_from_quaternion
import tf.transformations as tft
from geometry_msgs.msg import Twist


if __name__ == '__main__':
    rospy.init_node('flipbot_tf_listener_1')

    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    rate = rospy.Rate(1.0)
    while not rospy.is_shutdown():
        try:
            # trans = tfBuffer.lookup_transform(
            #     'marker_id0', 'marker_id1', rospy.Time())
            # trans2 = tfBuffer.lookup_transform(
            #     "camera_link","marker_id0",rospy.Time()
            # )
            trans3 = tfBuffer.lookup_transform(
                "camera_link","marker_id1",rospy.Time()
            )
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rate.sleep()
            continue
        # a=(trans.transform.translation.x)
        # c=(trans2.transform.translation.x)
        d=(trans3.transform.translation.x)
        e=(trans3.transform.rotation.z)
        # print (type(a))
        # rospy.loginfo("marker length %2f",a)
        # rospy.loginfo("marker length center %2f",b)
        
        # rospy.loginfo("marker_id0 to marker_id1 %.2f",a)
        # rospy.loginfo("usb length_maeker0  x %.2f",c)
        rospy.loginfo("usb length marker1  x %.2f",d)
        rospy.loginfo("usb length marker1  orientation %.2f",e)
        
        
        quaternion = [trans3.transform.rotation.x, trans3.transform.rotation.y,
                      trans3.transform.rotation.z, trans3.transform.rotation.w]

        # Convert the quaternion to Euler angles
        euler = tft.euler_from_quaternion(quaternion)
        yaw=euler[2]

        # Print the Euler angles in radians
        print("Roll: ", euler[0])
        print("Pitch: ", euler[1])
        print("Yaw: ", euler[2])
        
        if yaw >=-1.54:
            twist = Twist()
            # twist.linear.x = 0.2
            twist.angular.z = 0.2
            pub.publish(twist)
       
           
        else:
            twist = Twist()
            # twist.linear.x = 0.0
            twist.angular.z = 0.0
            pub.publish(twist)
            if d >=0.84:
                twist = Twist()
                twist.linear.x = 0.15
                # twist.angular.z = 0.0
                pub.publish(twist)
            else:
                twist = Twist()
                twist.linear.x = 0.0
                # twist.angular.z = 0.0
                pub.publish(twist)
            
        rate.sleep()