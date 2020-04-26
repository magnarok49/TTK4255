#!/bin/bash

~/Libraries/ORB_SLAM2/Examples/Monocular/mono_tum ~/Libraries/ORB_SLAM2/Vocabulary/ORBvoc.txt ./images/video1/config.yaml ./images/video1

mv ./KeyFrameTrajectory.txt ./data/video1/KeyFrameTrajectory.txt