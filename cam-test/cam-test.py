'''

Get a face, and then draw points of interest

Created on Aug 1, 2011

@author: davk
'''

import sys, math
import cv
import pygame
from pygame import image, display, event, draw
from pygame.locals import *

CAMWIDTH = 640
CAMHEIGHT = 480

def get_pygame_image(img_cv):
    img_cv_rgb = cv.CreateMat(img_cv.height, img_cv.width, cv.CV_8UC3)
    cv.CvtColor(img_cv, img_cv_rgb, cv.CV_BGR2RGB)
    img_pg = image.frombuffer(img_cv_rgb.tostring(), 
                              cv.GetSize(img_cv_rgb), 
                              "RGB")
    
    return img_pg

def crop(image, roi):
    cv.SetImageROI(image, roi)
    cropped = cv.CreateImage(roi[2:], 
                             image.depth, 
                             image.nChannels)
    cv.Copy(image, cropped)
    cv.ResetImageROI(image)
    return cropped

def get_points_of_interest(cv_image, numpoints=10, roi=None):
    
    cropped = crop(cv_image, roi)
    
    g_img = get_grayscale(cropped)
    eig_image = cv.CreateMat(g_img.rows, g_img.cols, cv.CV_32FC1)
    temp_image = cv.CreateMat(g_img.rows, g_img.cols, cv.CV_32FC1)
    
    ret = cv.GoodFeaturesToTrack(g_img,
                                 eig_image, 
                                 temp_image, 
                                 numpoints,
                                 0.001, # quality level -- lower is better
                                 0.01, 
                                 useHarris = True)
    offset = [(x + roi[0], y + roi[1]) for x, y in ret]
    return offset

def get_grayscale(rgb_image):
    g_img = cv.CreateMat(rgb_image.height, rgb_image.width, cv.CV_8U)
    cv.CvtColor(rgb_image, g_img, cv.CV_RGB2GRAY)
    return g_img
    
def draw_points_of_interest(img, dest, roi=None):
    points = get_points_of_interest(img, 25, roi)
    indexes = nearest_indexes(points, roi)
    
    ordered_points = []
    ind = 0
    for i in indexes:
        ordered_points.append(points[ind])
        ind = indexes[ind]
    
    draw.lines(dest, 
               pygame.Color("red"), 
               0, # filled
               ordered_points, 
               1)
        
def nearest_indexes(points, roi):
    indexes = []
    for pt in points:
        indexes.append(nearest_index(pt, points, indexes, roi))
    return indexes

# taken from display.py, adapted from its use in a class there
def nearest_index(loc, pts, exclude=[], roi=None):
    min = get_distance((0, 0), roi[2:])
    lind = 0
    for ind in range(len(pts)):
        distance = get_distance(loc, pts[ind])
        if (distance < min) and (distance > 0) and (not ind in exclude):
            min = distance
            lind = ind

    return lind
        
def get_distance(start, end):
    a = abs(end[0] - start[0])
    b = abs(end[1] - start[1])
    return math.sqrt(pow(a,2) + pow(b, 2))
# taken from display.py ^^^

def detect_faces(img, cascade):
    g_img = get_grayscale(img)
    
    storage = cv.CreateMemStorage(0)
    cv.EqualizeHist(g_img, g_img)
    faces = cv.HaarDetectObjects(g_img, cascade, storage)
    return faces

def draw_faces(src_img, dest_img, cascade):
    faces = detect_faces(src_img, cascade)
    for (x,y,w,h),n in faces:
        draw_points_of_interest(src_img, dest_img, (x,y,w,h))

def get_frame(capture, cascade):
    """
    MAIN DRAW LOOP FUNCTION
    Return the captured and manipulated pygame image to draw on the main
    window."""
        
    cam_capture = cv.QueryFrame(capture)
    pygame_image = get_pygame_image(cam_capture)
    draw_faces(cam_capture, pygame_image, cascade)
       
    return pygame_image


def main():
    pygame.init()
    screen = display.set_mode((CAMWIDTH, CAMHEIGHT))
    display.set_caption("monkey fever")
    capture = cv.CaptureFromCAM(0);
    haar_cascade = cv.Load("G:\\Developer\\OpenCV2.3\\opencv\\data\\haarcascades\\haarcascade_frontalface_default.xml")
    
    if not capture:
        print "could not get cam. exiting..."
        sys.exit(1)
    
    while 1:
        for ev in event.get():
            if ev.type == QUIT:
                return
        
        img = get_frame(capture, haar_cascade)
        screen.blit(img, (0, 0))
        display.flip()
    
    
if __name__ == "__main__":
    main()
    