"""
trans.py

Transmutation Study

Analyze faces in a webcam capture. Based on the data, draw a sigil and start a
synth.

TODO:
1 - test window resize on dual-screen monitor
2 - finish sound portion (mostly done)
3 - drawing algorithm -- make it look nice

"""

import sys
import random

import pygame
from pygame import surfarray
from pygame.locals import *
import cv
from scosc import controller
from scipy import ndimage

from face import Faces
import synth

# controls audio computer - the target ip and the port from the synth listener
controller = controller.Controller(("192.168.2.5", 57199)) 

WIDTH  = 800
HEIGHT = 800
CAMERA = 0
LOOKBACK = 10
REFRESH_TIME = 50 # ms

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
    if not allow_update(has_data):
        return
    
    synth.run(data)

    update_display(screen, data, faces)

def fake_update(screen, faces):
    """prepare images, faking the facial data with random data"""
    numfaces = 1
    quant = 4.0
    data = []
    for i in range(numfaces):
        face = [(random.randrange(0, quant) / float(quant-1),
                 random.randrange(0, quant) / float(quant-1))
                 for i in range(random.randrange(3, 15))]
        data.append(face)

    update_display(screen, data, faces)
    
def update_display(screen, data, faces):
    "actually draw the display"
    #pg_frame = get_capture_image(cv_frame)
    pg_frame = get_solid_image((WIDTH, HEIGHT))

    faces.draw(pg_frame, data)

    # add a blur - very glitchy but kind of interesting
    #arr_frame = surfarray.array2d(pg_frame)
    #arr_frame = ndimage.filters.gaussian_filter(arr_frame, 3.0)
    #pg_frame = surfarray.make_surface(arr_frame)
    
    screen.blit(pg_frame, (0, 0))
    pygame.display.flip()

def allow_update(has_data):
    """BBD signal delay comparison. Stabilize drawing."""
    allow_update.buffer.append(has_data)
    if len(allow_update.buffer) >= LOOKBACK:
        allow_update.buffer.pop(0)
    else:
        allow_update.active = has_data
        return False
    
    if has_data == allow_update.buffer[0] and has_data != allow_update.active:
        allow_update.active = has_data
        return True
    else:
        return False
allow_update.buffer = []

def main():
    pygame.init()
    capture = cv.CaptureFromCAM(CAMERA)
    if not capture:
        print "Could not get the cam. Crashing now..."
        sys.exit(1)
    
    pygame.display.set_caption("Transmutation Study")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    faces = Faces()

    update(screen, capture, faces)

    while True:
        for ev in pygame.event.get():
            if ev.type == QUIT:
                controller.sendMsg('run', 0)
                return
            elif ev.type == KEYDOWN:
                if ev.key == K_f:
                    screen = toggle_fullscreen(screen)
                elif ev.key == K_ESCAPE:
                    controller.sendMsg('run', 0)
                    return
        update(screen, capture, faces)
            
        pygame.time.wait(REFRESH_TIME)

def test():
    "hacked version of run(). the testing should be better integrated."
    pygame.init()
    pygame.display.set_caption("Transmutation Study Test")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    faces = Faces()

    fake_update(screen, faces)
    while True:
        for ev in pygame.event.get():
            if ev.type == QUIT:
                return
            elif ev.type == KEYDOWN:
                if ev.key == K_f:
                    screen = toggle_fullscreen(screen)
                elif ev.key == K_ESCAPE:
                    return
            
        pygame.time.wait(REFRESH_TIME)

if __name__ == "__main__":
    test()
    #main()





