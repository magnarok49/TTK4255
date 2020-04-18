#!/usr/bin/env python3

import argparse
import cv2
import os
import time
import yaml_utils as yaml

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('src', type=str, help='Specify path to video source.')
    parser.add_argument('--create_yaml', default=None, type=str, \
                        help='Create yaml file with given name')
    parser.add_argument('--fps', type=str, default=None, \
                        help='Specify the frame rate for the images to be captured.')
    parser.add_argument("-v", "--verbose", action="store_true", \
                        help='Increase output verbosity')
    args = parser.parse_args()

    # Create directories
    super_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')
    if not os.path.exists(super_dir):
        os.makedirs(super_dir)

    # TODO: what happens when you run this twice on the same video name? 
    img_dir = os.path.join(super_dir, os.path.basename(args.src).split('.')[0])
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    rgb_dir = os.path.join(img_dir, 'rgb')
    if not os.path.exists(rgb_dir):
        os.makedirs(rgb_dir)

    gray_dir = os.path.join(img_dir, 'gray')
    if not os.path.exists(gray_dir):
        os.makedirs(gray_dir)

    # Create files
    rgb = open(os.path.join(img_dir, 'rgb.txt'), 'w')
    gray = open(os.path.join(img_dir, 'gray.txt'), 'w')

    # Specify parameters
    try:
        fps = float(args.fps)
        tpf = 1/float(args.fps)
    except TypeError:
        print('Using default fps: 30')
        fps = 30            # Specify frame rate
        tpf = 1/fps         # Time per fram: Adjust to capture a frame every ... second        
    
    # Create yaml file
    if args.create_yaml:
        yaml_path = os.path.join(img_dir,args.create_yaml)
        yaml.createDefaultYamlFile(yaml_path)
        d = {
            "Camera": {
                "fps": fps,
                "RGB": 1
            }
        }
        yaml.updateExistingFile(d,yaml_path)
    
    # Capture video
    sec = 0
    src = cv2.VideoCapture(os.path.realpath(args.src))
    src.set(cv2.CAP_PROP_POS_MSEC,sec*1000)

    success,image = src.read()
    image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # Gray scale images
    
    while success:
        # Save frame as JPG file based on frame timestamp
        img_name = int(src.get(cv2.CAP_PROP_POS_MSEC))
        cv2.imwrite(rgb_dir + '/' + "%d.jpg" %img_name, image)
        cv2.imwrite(gray_dir + '/' + "%d.jpg" %img_name, image_gray)
        if args.verbose: print("Read a new frame: ", "%d.jpg" %img_name)
        
        # Write to file
        rgb.write('%f rgb/%d.jpg\n' %(sec, img_name))
        gray.write('%f gray/%d.jpg\n' %(sec, img_name))
        
        # Set frame rate
        sec += tpf
        sec = round(sec, 2)
        src.set(cv2.CAP_PROP_POS_MSEC,sec*1000)

        # Extract frame
        success,image = src.read()
        if success:
            image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # Gray scale images

