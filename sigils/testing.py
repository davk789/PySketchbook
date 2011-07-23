'''
Created on Jul 23, 2011

@author: davk
'''

import cv
import time, sys

cv.NamedWindow("test", cv.CV_WINDOW_AUTOSIZE)

for i in range(5):
    capture = cv.CaptureFromCAM(i)
    if capture:
        print "i got index ", i  
        break

def get_cam():
    frame = cv.QueryFrame(capture)
    cv.ShowImage("test", frame)
    #time.sleep(1)
    c = cv.WaitKey(10)
    if c == "q":
        sys.exit(0)
    

if __name__ == "__main__":
    while True:
        get_cam()

