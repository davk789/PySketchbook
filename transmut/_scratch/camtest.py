'''
camtest

get the camera working on windows.
'''

import cv
import sys


    

def get_cam():
    
    INTERNAL_CAM = 0
    
    cv.NamedWindow("test", cv.CV_WINDOW_AUTOSIZE)
    capture = cv.CaptureFromCAM(INTERNAL_CAM)
    
    if not capture:
        print "No camera captured. Exiting..."
        sys.exit(1)

    run = True
    
    while run:

        frame = cv.QueryFrame(capture)
        cv.ShowImage("test", frame)
        run = cv.waitKey(10) != 113

        
    

if __name__ == "__main__":
    print "testing camera input"
    get_cam()
    
