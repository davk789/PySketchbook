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

usecam = False # workaround for an OpenCV bug on windows

def init(cam=1):
    global save_path
    global capture

    save_path = os.path.join(os.path.expanduser("~"), 
                             "Pictures", 
                             "transmutation-study")
    if not os.path.exists(save_path):
        print "save path does not exist. creating one now"
        os.mkdir(save_path)

    capture = cv.CaptureFromCAM(cam) # 1 = external webcam
    if not capture:
        print "ERROR: camera not captured!! Exiting now."
        sys.exit(1)
        
def capture_image(path):
    frame = cv.QueryFrame(capture)
    cv.SaveImage(path, frame)
    
def analyze_image(path, numpoints=10):
    img = cv.LoadImageM(path, cv.CV_LOAD_IMAGE_GRAYSCALE)
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

def get_cam(numpoints):
    """
    Generate the filename, and then use it to capture and analyze input from
    the webcam
    """
    global img_num
    
    filename = os.path.join(save_path, "capture" + str(img_num) + ".jpg")
    if usecam:
        capture_image(filename)
    
    ret = analyze_image(filename, numpoints)
    
    img_num += 1
    
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

