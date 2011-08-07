"""
trans.py

Top-level transmutation study (second pass) script.

"""

import sys

import pygame
import cv

from face import Faces

if __name__ != "__main__":
    # i guess this makes sense?
    print "This script is not to be imported. Run it directly dummy!"
    sys.exit(2)

CAMWIDTH  = 640
CAMHEIGHT = 480
CAMERA    = 0

capture = cv.CaptureFromCAM(CAMERA)
if not capture:
    print "Could not get the cam. Crashing now..."
    sys.exit(1)

faces = Faces(capture)

def get_draw_image():
    return faces.get_image()

def main():
    pygame.init()
    screen = pygame.display.set_mode((CAMWIDTH, CAMHEIGHT))
    pygame.display.set_caption("Transmutation Study")

        
    while True:
        for ev in pygame.event.get():
            if ev.type == QUIT:
                return
        
        img = get_draw_image()
        screen.blit((0, 0))
        display.flip()

    #face = FaceTransmuter()



main()



