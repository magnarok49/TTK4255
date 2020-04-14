# Inspired by https://medium.com/@iKhushPatel/convert-video-to-images-images-to-video-using-opencv-python-db27a128a481

import argparse
import cv2
import os


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('src', type=str, help='Specify path to video source.')
    args = parser.parse_args()

    # Create directories
    img_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)  

    sec = 0
    fps = 1             # Adjust to capture a frame every ... second
    count = 1

    # Capture video
    src = cv2.VideoCapture(os.path.realpath(args.src))
    # src.set(cv2.CAP_PROP_FPS, fps)
    src.set(cv2.CAP_PROP_POS_MSEC,sec*1000)

    success,image = src.read()
    while success:
        # image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # Uncomment for gray scale images
        cv2.imwrite(img_dir + '/' + "image%d.jpg" %count, image)     # save frame as JPEG file      
        print('Read a new frame: ', "image%d.jpg" %count)

        count += 1
        sec += fps
        sec = round(sec, 2)        

        src.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
        success,image = src.read()

