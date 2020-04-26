#!/usr/bin/env python3
# Code found on https://www.learnopencv.com/camera-calibration-using-opencv/

import argparse
import cv2
import numpy as np
import os
import glob

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('imagepath', type=str, help='Specify path to video source.')
    parser.add_argument('size', type = int, help = "size of checker square in mm")
    parser.add_argument('checker_width', type = int, help = "amount of squares horizontally-1")
    parser.add_argument('checker_height', type = int, help = "amount of squares vertically-1")
    args = parser.parse_args()

    # Defining the dimensions of checkerboard
    CHECKERBOARD = (args.checker_height,args.checker_width)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Creating vector to store vectors of 3D points for each checkerboard image
    objpoints = []
    # Creating vector to store vectors of 2D points for each checkerboard image
    imgpoints = [] 

    #Creating files for storing intrinsics
    dist_file = open("dist.txt", "w+")
    K_file = open("K.txt", "w+")


    # Defining the world coordinates for 3D points
    objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
    objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
    objp = objp*args.size
    prev_img_shape = None

    # Extracting path of individual image stored in a given directory
    images = glob.glob(os.path.realpath(args.imagepath)+'/*')
    for fname in images:
        print('Analysing image: ', fname)

        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # Find the chess board corners
        # If desired number of corners are found in the image then ret = true
        ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
        print(ret)
        """
        If desired number of corner are detected,
        we refine the pixel coordinates and display 
        them on the images of checker board
        """
        if ret == True:
            objpoints.append(objp)
            # refining pixel coordinates for given 2d points.
            corners2 = cv2.cornerSubPix(gray, corners, (11,11),(-1,-1), criteria)
            
            imgpoints.append(corners2)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)

        # cv2.imshow('img',img)
        # cv2.waitKey(0)



    cv2.destroyAllWindows()

    h,w = img.shape[:2]

    """
    Performing camera calibration by 
    passing the value of known 3D points (objpoints)
    and corresponding pixel coordinates of the 
    detected corners (imgpoints)
    """
    #print('imgpoints: ', imgpoints)
    #print('gray.shape[::-1]: ', gray.shape[::-1])

    

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    
    
    print("rvecs : \n")
    print(rvecs)
    print("tvecs : \n")
    print(tvecs)
    print("dist : \n")
    print(dist)
    dist_file.write("k1: ")   
    dist_file.write(str(dist[0, 0])) 
    dist_file.write("\nk2: ")
    dist_file.write(str(dist[0, 1]))
    dist_file.write("\np1: ")
    dist_file.write(str(dist[0, 2]))
    dist_file.write("\np2: ")
    dist_file.write(str(dist[0, 3]))
    dist_file.write("\nk3: ")
    dist_file.write(str(dist[0, 4]))
    dist_file.close()
    print("Camera matrix : \n")
    print(mtx)
    K_file.write(str(mtx))
    K_file.close()

