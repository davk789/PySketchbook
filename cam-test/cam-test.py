'''

Get a face, and then draw points of interest

Created on Aug 1, 2011

@author: davk
'''

import sys
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

def get_points_of_interest(cv_image, numpoints=10):
    g_img = get_grayscale(cv_image)
    eig_image = cv.CreateMat(g_img.rows, g_img.cols, cv.CV_32FC1)
    temp_image = cv.CreateMat(g_img.rows, g_img.cols, cv.CV_32FC1)
    
    ret = cv.GoodFeaturesToTrack(g_img,
                                 eig_image, 
                                 temp_image, 
                                 numpoints,
                                 0.001, # quality level -- lower is better
                                 0.01, 
                                 useHarris = True)
    return ret

def get_grayscale(rgb_image):
    g_img = cv.CreateMat(rgb_image.height, rgb_image.width, cv.CV_8U)
    cv.CvtColor(rgb_image, g_img, cv.CV_RGB2GRAY)
    return g_img
    
def draw_points_of_interest(img, dest):
    points = get_points_of_interest(img, 100)
    for x, y in points:
        draw.circle(dest, pygame.Color("red"), (int(x), int(y)), 3)

def get_frame(capture):
    cam_capture = cv.QueryFrame(capture)
    
    pygame_image = get_pygame_image(cam_capture)
    
    draw_points_of_interest(cam_capture, pygame_image)
    
    return pygame_image

def detect_faces():
    g_img = get_grayscale()
    
    storage = cv.CreateMemStorage(0)
    cv.clearMemStorage()

def main():
    pygame.init()
    screen = display.set_mode((CAMWIDTH, CAMHEIGHT))
    display.set_caption("monkey fever")
    capture = cv.CaptureFromCAM(0);
    if not capture:
        print "could not get cam. exiting..."
        sys.exit(1)
    
    while 1:
        for ev in event.get():
            if ev.type == QUIT:
                return
        
        img = get_frame(capture)
        screen.blit(img, (0, 0))
        display.flip()
    
    
        
    

if __name__ == "__main__":
    main()
    