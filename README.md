# lane_following_using_turtlbot
lane_following_using_turtlbot

open Terminal 1:
catkin_ws$ roslaunch ar court.launch 
For line Following with rfid input from external sensor and ultra sonic input external sensor the robot will stop otherwise robot move ,FOr giving rfi input pub data through rfid topic and also for ultra sonic 
open Terminal 2:
catkin_ws$ roslaunch ar line_follower_with ultra_rfid.py
open Terminal 3:
catkin_ws$ rostopic pub /ultra std_msgs/Int32 "data: 0" 
or 
catkin_ws$ rostopic pub /ultra std_msgs/Int32 "data: 1" 
open Terminal 4:
catkin_ws$ rostopic pub /rfid std_msgs/Int32 "data: 1" 
or 
catkin_ws$ rostopic pub /ultra std_msgs/Int32 "data: 0" 
