"""
face.py

draw a main image by detecting facial features and running a sigil creation
algorithm from the detected features.

"""

# this would be one way to forbid running scripts as main
import sys

import cv
import pygame
from pygame.locals import *



class Faces(object):
    def __init__(self, capture):
        super(Faces, self).__init__()
        self.capture = capture
        print self.__class__.__string__, "initialized"
        
    def get_image(self):
        print "I should return a pygame image to draw the main window."
        return self


if __name__ == "__main__":
    print "run this from trans.py!"
    sys.exit(1)

