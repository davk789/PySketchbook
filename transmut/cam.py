"""
cam.py

Manage the camera input. For now, this section draws on an example from the 
opencv cookbook. Eventually, I will want to take another look here and come
up with something the might work better. But for now this will suffice.
"""

import cv
import os, sys

save_path = None
capture = None
img_num = 0

def init(cam=1):
    global save_path
    global capture

    save_path = "/Users/davk/Pictures/transmutation-study/"
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    capture = cv.CaptureFromCAM(cam) # 1 = external webcam
    if not capture:
        print "ERROR: camera not captured!! Exiting now."
        sys.exit(1)

def get_cam(numpoints=10):
    global img_num
    global save_path
    global capture

    frame = cv.QueryFrame(capture)
    filename = save_path + "capture" + str(img_num) + ".jpg"
    cv.SaveImage(filename, frame)
    img_num += 1
    
    img = cv.LoadImageM(filename, cv.CV_LOAD_IMAGE_GRAYSCALE)
    eig_image = cv.CreateMat(img.rows, img.cols, cv.CV_32FC1)
    temp_image = cv.CreateMat(img.rows, img.cols, cv.CV_32FC1)
    ret = []
    for (x,y) in cv.GoodFeaturesToTrack(img, 
                                        eig_image, 
                                        temp_image, 
                                        numpoints,
                                        0.04, 
                                        1.0, 
                                        useHarris = True):
        ret.append((x,y))
    return ret

### testing

if __name__ == "__main__":
    print "testing cam.py..."
    init(0)
    print get_cam(1)
    print get_cam(2)
    print get_cam(5)
    print get_cam(25)
    del capture
    sys.exit(0)

