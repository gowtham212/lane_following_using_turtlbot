#!/usr/bin/env python3

import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

# Initialize the node
rospy.init_node('hsv_color_node', anonymous=True)

# Create a bridge to convert ROS image messages to OpenCV images
bridge = CvBridge()

# Define the image topic to subscribe to
image_topic = "/camera/color/image_raw"

# Define the HSV color you want to detect
hsv_color = (255, 0, 0) # Green color

# Set the threshold range for the color
hsv_range = 10

# Define the callback function for the image subscriber
def image_callback(msg):
    try:
        # Convert the ROS image message to OpenCV image
        img = bridge.imgmsg_to_cv2(msg, "bgr8")
    except CvBridgeError as e:
        print(e)
        return

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define the upper and lower limits of the threshold range
    lower = (hsv_color[0] - hsv_range, hsv_color[1] - hsv_range, hsv_color[2] - hsv_range)
    upper = (hsv_color[0] + hsv_range, hsv_color[1] + hsv_range, hsv_color[2] + hsv_range)

    # Print the upper and lower limits of the threshold range
    rospy.loginfo("Lower: {}".format(lower))
    rospy.loginfo("Upper: {}".format(upper))

    # Apply the threshold to the image to extract the color
    mask = cv2.inRange(hsv, lower, upper)

    # Display the extracted color image
    cv2.imshow("Extracted Color", mask)
    cv2.waitKey(1)

# Subscribe to the image topic
rospy.Subscriber(image_topic, Image, image_callback)

# Spin the node to prevent it from exiting
rospy.spin()
