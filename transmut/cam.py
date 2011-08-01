"""
cam.py

Manage the camera input. For now, this section draws on an example from the 
opencv cookbook. Eventually, I will want to take another look here and come
up with something the might work better. But for now this will suffice.
"""

import cv
import os, sys

save_path = os.path.join(os.path.expanduser("~"), 
                         "Pictures", 
                         "transmutation-study")
if not os.path.exists(save_path):
    print "save path does not exist. creating one now"
    os.mkdir(save_path)

capture = cv.CaptureFromCAM(1) # 1 = external webcam
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
        ret.append((x / 640.0,y / 480.0))
    return ret

img_num = 0 # used by win bug workaround. remove this asap.
def get_cam(numpoints, name="capture.jpg", usecam=True):
    """
    Generate the filename, and then use it to capture and analyze input from
    the webcam. I should not have to write to file, fix this later.
    """
    global img_num
    print str(img_num)
    if usecam:
        filename = os.path.join(save_path, "capture.jpg")
        capture_image(filename)
    else:
        # hack for windows testing. do not use.
        filename = os.path.join(save_path, "capture" + str(img_num) + ".jpg")
        img_num = (img_num + 1) % 4
    
    ret = analyze_image(filename, numpoints)
    
    return ret


### testing

if __name__ == "__main__":
    print "testing cam.py..."
    print get_cam(1)
    print get_cam(2)
    print get_cam(5)
    print get_cam(25)
    del capture
    sys.exit(0)

