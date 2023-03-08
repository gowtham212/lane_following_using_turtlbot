#!/usr/bin/env python3

import cv2
import numpy as np
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

# Define the lower and upper bounds for yellow color in HSV color space
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([40, 255, 255])

# Initialize the ROS node
rospy.init_node('yellow_tape_detection')

# Initialize the CV bridge
bridge = CvBridge()

# Define the callback function for processing the image messages
def image_callback(msg):
    # Convert ROS image message to OpenCV image
    img = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

    # Convert image to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Apply color thresholding to extract yellow pixels
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Apply morphological operations to remove noise and fill in gaps
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)

    # Find contours in the binary image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on size and shape
    for contour in contours:
        area = cv2.contourArea(contour)
        x,y,w,h = cv2.boundingRect(contour)
        aspect_ratio = float(w)/h
        if area > 100 and aspect_ratio > 1.5:
            # Draw bounding box around the yellow tape region
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

    # Display the resulting image
    cv2.imshow('Yellow Tape Detection', img)
    cv2.waitKey(1)

# Subscribe to the camera image topic
rospy.Subscriber('/camera/color/image_raw', Image, image_callback)

# Start the main loop
rospy.spin()
