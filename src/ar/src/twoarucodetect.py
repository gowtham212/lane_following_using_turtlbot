#!/usr/bin/python3  
import rospy
import math
import tf2_ros
from turtlesim.msg import Pose
from tf.transformations import euler_from_quaternion
import tf.transformations as tft
from geometry_msgs.msg import Twist


if __name__ == '__main__':
    rospy.init_node('flipbot_tf_listener_2')

    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    rate = rospy.Rate(1.0)
    while not rospy.is_shutdown():
        try:
            # trans = tfBuffer.lookup_transform(
            #     'marker_id0', 'marker_id1', rospy.Time())
            trans1 = tfBuffer.lookup_transform(
                "camera_link","marker_id1",rospy.Time()
            )
            trans2 = tfBuffer.lookup_transform(
                "camera_link","marker_id2",rospy.Time()
            )
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rate.sleep()
            continue
        # a=(trans.transform.translation.x)
        c=(trans1.transform.translation.x)
        e1=(trans1.transform.rotation.z)
        d=(trans2.transform.translation.x)
        e=(trans2.transform.rotation.z)
        # print (type(a))
        # rospy.loginfo("marker length %2f",a)
        # rospy.loginfo("marker length center %2f",b)
        
        # rospy.loginfo("marker_id0 to marker_id1 %.2f",a)
        # rospy.loginfo("usb length_maeker0  x %.2f",c)
        rospy.loginfo("usb length marker1  x %.2f",c)
        rospy.loginfo("usb length marker1  orientation %.2f",e1)
        rospy.loginfo("usb length marker1  x %.2f",d)
        rospy.loginfo("usb length marker1  orientation %.2f",e)
        
        
        quaternion1 = [trans1.transform.rotation.x, trans1.transform.rotation.y,
                      trans1.transform.rotation.z, trans1.transform.rotation.w]

        # Convert the quaternion to Euler angles
        euler1 = tft.euler_from_quaternion(quaternion1)
        yaw1=euler1[2]

        # Print the Euler angles in radians
        print("Roll1: ", euler1[0])
        print("Pitch1: ", euler1[1])
        print("Yaw1: ", euler1[2])
        
        quaternion2 = [trans2.transform.rotation.x, trans2.transform.rotation.y,
                      trans2.transform.rotation.z, trans2.transform.rotation.w]

        # Convert the quaternion to Euler angles
        euler2 = tft.euler_from_quaternion(quaternion2)
        yaw2=euler2[2]

        # Print the Euler angles in radians
        print("Roll2: ", euler2[0])
        print("Pitch2: ", euler2[1])
        print("Yaw2: ", euler2[2])
        
        
        
        if yaw1>=-1.5:
            twist = Twist()
            # twist.linear.x = 0.2
            twist.angular.z = 0.1
            pub.publish(twist)
        elif yaw2<=-1.3:
            twist = Twist()
            # twist.linear.x = 0.2
            twist.angular.z = -0.1
            pub.publish(twist)
       
           
        else:
            twist = Twist()
            # twist.linear.x = 0.0
            twist.angular.z = 0.0
            pub.publish(twist)
            # if d >=0.84:
            #     twist = Twist()
            #     twist.linear.x = 0.15
            #     # twist.angular.z = 0.0
            #     pub.publish(twist)
            # else:
            #     twist = Twist()
            #     twist.linear.x = 0.0
            #     # twist.angular.z = 0.0
            #     pub.publish(twist)
            
        rate.sleep()