#!/usr/bin/env python3

import rospy
import cv_bridge  
import cv2 as cv
import numpy as np
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import time
from std_msgs.msg import Int32



class ROSExample:
    def __init__(self):
        self.bridge = cv_bridge.CvBridge()
        cv.namedWindow('BGR Image', 1)
        cv.namedWindow('MASK', 1)
        cv.namedWindow('MASKED', 1)
        self.image_sub = rospy.Subscriber(
            'camera/color/image_raw', Image, self.image_callback)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.rfid_sub = rospy.Subscriber('rfid', Int32, self.rfid_call)
        self.ultra_sub = rospy.Subscriber('ultra', Int32, self.ultra_call)
        self.rfid_status = 0
        self.ultra_status = 0
        self.twist = Twist()

    def rfid_call(self, msg):
        self.rfid_status = msg.data
        rospy.loginfo("Updating {}".format(self.rfid_status))
    def ultra_call(self, msg):
        self.ultra_status = msg.data
        rospy.loginfo("Updating111 {}".format(self.ultra_status))


    def image_callback(self, msg):
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        # lower_yellow = np.array([10, 10, 10])
        # upper_yellow = np.array([255, 255, 250])
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([40, 255, 255])
        mask = cv.inRange(hsv, lower_yellow, upper_yellow)
        masked = cv.bitwise_and(image, image, mask=mask)
        h, w = image.shape[:2]
        RESIZE = (w//3, h//3)
        search_top = (h//4)*3
        search_bot = search_top + 20
        mask[0:search_top, 0:w] = 0
        mask[search_bot:h, 0:w] = 0
        M = cv.moments(mask)
        if M['m00'] > 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv.circle(image, (cx, cy), 20, (0, 0, 255), -1)
            err = cx - w//2
            self.twist.linear.x = 0.2
            self.twist.angular.z = -float(err)/1000
            
        display_mask = cv.resize(mask, RESIZE)
        display_masked = cv.resize(masked, RESIZE)
        display_image = cv.resize(image, RESIZE)
        cv.imshow('BGR Image', display_image)
        cv.imshow('MASK', display_mask)
        cv.imshow('MASKED', display_masked)
        cv.waitKey(3)

    def run(self):
        rate = rospy.Rate(10)  # 10 Hz
        while not rospy.is_shutdown():
            if ((self.rfid_status == 1)):
                self.twist.linear.x = 0.0
                self.twist.angular.z = 0.0
                self.cmd_vel_pub.publish(self.twist)
                
                rospy.loginfo("Robot stopeed")
                print(" Before RFID status ",self.rfid_status)
                go = input("Move")
                print("RFID status",self.rfid_status)
                self.rfid_status= 0
                print("after RFID status",self.rfid_status)
            
            elif ((self.rfid_status == 0)and (self.ultra_status == 0)):
                self.cmd_vel_pub.publish(self.twist)
              
            elif ((self.ultra_status == 0)):
                self.twist.linear.x = 0.0
                self.twist.angular.z = 0.0
                self.cmd_vel_pub.publish(self.twist)
                
                rospy.loginfo("Robot due to ultra stopeed")
                
            else: 
                self.twist.linear.x = 0.0
                self.twist.angular.z = 0.0
                self.cmd_vel_pub.publish(self.twist)
                # self.ultra_status = 1
                rospy.loginfo("Robot ultra stopeed")
            # else:
            
                
                
            rospy.loginfo('Published message: %s')
            rate.sleep()
    
    def stops(self):
        self.twist.linear.x = 0.0
        self.twist.angular.z = 0.0
        self.cmd_vel_pub.publish(self.twist)
        rospy.loginfo("stop") 

if __name__ == '__main__':
    try:
        rospy.init_node('ros_example')
        ros_example = ROSExample()
        # time.sleep(0.2)
        
        ros_example.run()
        rospy.spin()
        # time.sleep(0.2)
        # ros_example.stops()
        
        
        
    except KeyboardInterrupt:
        pass