# About
This project implements a P-controller on a SITL simulation of an ardurover to follow a set of waypoints using ROS. <br/>

The simulation can be setup using this link: http://ardupilot.org/dev/docs/rover-sitlmavproxy-tutorial.html <br/>

The proportional gain was tuned to prevent rapid changes in the bot's orientation. Below is the video showing the p-controller running on the simulated rover: <br/>

[![Simulation Video](https://github.com/adityajain07/SITL_Simulation-Ardurover-P_Controller/blob/master/thumbnail.png)](https://www.youtube.com/watch?v=ezrckOLDqDA "Simulation Video")


# Methodology
The below steps needs to be implemented (in order):

1. Set up the SITL simulation of ardurover: http://ardupilot.org/dev/docs/rover-sitlmavproxy-tutorial.html
1. Install ROS, create a ROS workspace and a ROS package
1. Install mavros
1. Run roscore and connect your master ROS to the SITL simulation (via mavros) with this command: roslaunch mavros apm2.launch fcu_url:=udp://localhost:14550@
1. In MAVProxy (command-line based GCS which pops up when you start SITL simulation), enter two commands: 'arm throttle' and 'mode guided' ('arm throttle' turns the motors on and 'mode guided' enables us to control the simulated rover using our code)
1. Run the 'controller.py' file as a ros node



