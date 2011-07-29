'''
transmut-poc.py

For Transmutation Study, I simply want to collect a set of data points from
image analysis. cv.GoodFeaturesToTrack does corner detection and returns a 
list of said corners. This is based on the opencv cookbook example, and so 
it needlessly saves the snapshot to a file before reading it back. For this
project, this method will suffice. Besides, storing the snapshot images will
allow me to retrieve them later, perhaps with different parameters. If I need 
to do anyting more elaborate, then I can learn how to convert the webcam 
input to grayscale within memory.

Created on Jul 23, 2011

@author: davk
'''

import cv
import sys

INTERNAL_CAM = 0
EXTERNAL_CAM = 1

capture = cv.CaptureFromCAM(INTERNAL_CAM)

if not capture:
    print "No camera captured. Exiting..."
    sys.exit(1)
    
cv.NamedWindow("test", cv.CV_WINDOW_AUTOSIZE)
    

def get_cam():
    frame = cv.QueryFrame(capture) 
    filepath = "/Users/davk/Desktop/test.jpg"
    cv.SaveImage(filepath, frame)
    
    img = cv.LoadImageM(filepath, cv.CV_LOAD_IMAGE_GRAYSCALE)
    eig_image = cv.CreateMat(img.rows, img.cols, cv.CV_32FC1)
    temp_image = cv.CreateMat(img.rows, img.cols, cv.CV_32FC1)
    for (x,y) in cv.GoodFeaturesToTrack(img, 
                                        eig_image, 
                                        temp_image, 
                                        10, # number of features to track 
                                        0.04, 
                                        1.0, 
                                        useHarris = True):
        print "good feature at", x,y

        
    

if __name__ == "__main__":
    print "testing camera input"
    get_cam()
    
