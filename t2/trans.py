"""
trans.py

Transmutation Study

Analyze faces in a webcam capture. Based on the data, draw a sigil and start a
synth.

TODO:
1 - audio programming
2 - analysis timing and behavior:
     - draw a sigil when detecting the face and preserve that image - no 
       re-analysis/redraw
     - if no face is detected, remove the image and wait for new image
3 - window resize behavior - test on dual-screen monitor

"""

import sys

import pygame
from pygame.locals import *
import cv

from face import Faces


WIDTH  = 800
HEIGHT = 800
CAMERA = 0

def get_capture_image(frame):
    "convert cv image to pygame image"
    frame_rgb = cv.CreateMat(frame.height, frame.width, cv.CV_8UC3)
    cv.CvtColor(frame, frame_rgb, cv.CV_BGR2RGB)
    return pygame.image.frombuffer(frame_rgb.tostring(), 
                                   cv.GetSize(frame_rgb), 
                                   "RGB")

def get_solid_image(dimensions):
    "generate a blank pygame drawing surface"
    canvas = pygame.Surface(dimensions)
    canvas.fill(pygame.Color("black"))
    return canvas

def toggle_fullscreen(screen):
    if toggle_fullscreen.full:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
    toggle_fullscreen.full = not toggle_fullscreen.full
    return screen
toggle_fullscreen.full = False

def update(screen, capture, faces):
    """prepare images and data, and then update the pygame display"""
    cv_frame = cv.QueryFrame(capture)
    data = faces.analyze(cv_frame)
    
    has_data = len(data) > 0
    if has_data == update.last_data:
        return

    update.last_data = has_data
    
    #pg_frame = get_capture_image(cv_frame)
    pg_frame = get_solid_image((WIDTH, HEIGHT))

    faces.draw(pg_frame, data)
    screen.blit(pg_frame, (0, 0))
    pygame.display.flip()
update.last_data = False

def main():
    
    pygame.init()
    
    capture = cv.CaptureFromCAM(CAMERA)
    if not capture:
        print "Could not get the cam. Crashing now..."
        sys.exit(1)
    
    pygame.display.set_caption("Transmutation Study")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    faces = Faces()
    img = update(screen, capture, faces)

    while True:
        for ev in pygame.event.get():
            if ev.type == QUIT:
                return
            elif ev.type == KEYDOWN:
                if ev.key == K_f:
                    screen = toggle_fullscreen(screen)
                elif ev.key == K_ESCAPE:
                    return

        update(screen, capture, faces)
        pygame.time.wait(50)

if __name__ == "__main__":
    main()
else:
    print "This script is not to be imported. Run it directly dummy!"
    raise Exception("import_error")





