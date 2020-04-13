# Robotic vision project, TTK4255, Magne Sirnes, Aleksander Elvebakk, Gustav Often

## Tasks:

 + Problem 1: Get a slam library running, run this on a pre-recorded video, visualize results
 + Problem 2: Record video on running lego-robot, collect encoder odometry from robot, compare slam and odometry results.

## TODO:

 + Build lego robot
 + Program cruise control + odometry for lego robot
 + Test slam libraries
 + Fetch camera from Anette
 + Figure out data storage/streaming from lego robot
 + Figure out video streaming from camera
 + Write some visualization for problem 1
 + Write some visualization/comparison for problem 2 

## Useful links:

 + [MonoSLAM paper, 2007](https://www.robots.ox.ac.uk/ActiveVision/Publications/davison_etal_pami2007/davison_etal_pami2007.pdf)
 + [Paper categorizing different types of SLAM](https://arxiv.org/ftp/arxiv/papers/1610/1610.03660.pdf)
 + [ORBSLAM2, library that we use](https://github.com/raulmur/ORB_SLAM2)

## Guide for installing
 + Follow guide on the ORBSLAM github page
 + When installing opencv, make sure to check out so you use 3.2 and not latest release
 + if orbslam can install, one trick may be to add the line #include <unistd.h> in ORB_SLAM2/include/System.h
