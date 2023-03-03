#!/usr/bin/env python3

import rospy, cv_bridge	#ROSとOpenCV間でデータを受け渡すためのパッケージ
import cv2 as cv
import numpy as np
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist

class ROSExample:
    def __init__(self):
        self.bridge = cv_bridge.CvBridge()
        cv.namedWindow('BGR Image', 1)	
        cv.namedWindow('MASK', 1)	
        cv.namedWindow('MASKED', 1)	
        self.image_sub = rospy.Subscriber('camera/rgb/image_raw', Image, self.image_callback)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
        self.twist = Twist()	

    def image_callback(self, msg):
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding = 'bgr8')
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)	
        lower_yellow = np.array([10, 10, 10])	
        upper_yellow = np.array([255, 255, 250])	
        mask = cv.inRange(hsv, lower_yellow, upper_yellow)	
        masked = cv.bitwise_and(image, image, mask = mask)	
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
    
            self.cmd_vel_pub.publish(self.twist)
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
        ros_example.run()
        
    except KeyboardInterrupt:
        ros_example.stops()
