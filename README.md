# Robotic vision project, TTK4255, Magne Sirnes, Aleksander Elvebakk, Gustav Often, Thomas Hellum

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
 + if orbslam fails to compile, one trick may be to add the line `#include <unistd.h>` in ORB_SLAM2/include/System.h


## Usage


### Generate sequence

Requirements: 
 + openCV (tested with 3.2.0)
 + opencv-python (tested with 4.2.0)
 + pyyaml
 
Generates a sequence of images from a specified video. Two parameters should/can be specified when runnning it. PATH_TO_VIDEO needs to be specified and can be both absolute and relative, while DESIRED_FPS for images to be captured is optional. If fps is not specified the default will be 30 frames per second.   
The script first generates directories for images to be saved, located in the same folder as the generate_sequenec.py script. The images will be named based on the millisecond they were captured and saved to the image folder. The images will be saved both in rgb and gray scale, and saved in their respective folders. Additionally two .txt files (for rgb and gray scale) are created containing the time instant the frame was captured and the name of the respective image. 
If the `--create_yaml YAML_NAME` option is passed, a yaml file with default options and correct fps will be created along with the txt files.

```bash
$ python3 generate_sequence.py PATH_TO_VIDEO
$ python3 generate_sequence.py PATH_TO_VIDEO --fps DESIRED_FPS
$ python3 generate_sequence.py PATH_TO_VIDEO --create_yaml YAML_NAME
```

### Yaml utils

Requirements: 
 + pyyaml

Utility functions for dealing with YAML files in python.
The only functions you need to deal with are `createDefaultYamlFile(filePath)` and `updateExistingFile(dict, filePath [,newFilePath])`
The first of which generates a yaml file at the specified path with default values.
The second accepts a dict and a path to an existing yaml file, it will apply the changes found in dict to this yaml file,
or optionally save the updated yaml file to a new path.

The dictionary should be formatted as:
```python3
dict = {
    "Camera": {
        "fps": NEW_FPS_VALUE,
        "fx": NEW_FX_VALUE,
        etc..
    },
    etc..
}
```
 
See TUM1.yaml in ORB_SLAM2/Examples/Monocular or `make***SubDict()` etc. in yaml_utils.py for an overview of all values that can be set.. 

### Camera calibration

Computes the calibration matrix for camera. The following needs to be specified as input arguments for the script when running it.
 + Path to folder containing pictures of checkerboard
 + size of side of each square on board
 + Amounts of inner corners vertically (amount of squares -1)
 + Amount of inner corners horizontally (amount of squares -1)

```bash
$ python3 camera_calibration.py PATH_TO_FOLDER SIZE_OF_CHECKER_SQUARES_IN_MM AMOUNT_OF_INNER_CORNERS_VERTICALLY AMOUNT_OF_INNER_CORNERS_HORIZONTALLY
```
