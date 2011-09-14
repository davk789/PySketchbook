"""
face.py

draw a main image by detecting facial features and running a sigil creation
algorithm from the detected features.

"""

import sys, platform, math, random

import cv
import pygame

class Faces(object):
    """
    Analyze an image using face recognition and points of interest, coming from
    an opencv image, and then draw a figure on a pygame Surface based on the
    manipulated data.
    """
    def __init__(self):
        super(Faces, self).__init__()
        if platform.system() == 'Windows':
            self.cascade = cv.Load("G:\\Developer\\OpenCV2.3\\opencv\\data\\haarcascades\\haarcascade_frontalface_default.xml")
        else:
            self.cascade = cv.Load("/opt/local/var/macports/build/_opt_local_var_macports_sources_rsync.macports.org_release_ports_graphics_opencv/opencv/work/OpenCV-2.2.0/data/haarcascades/haarcascade_frontalface_default.xml")
        self.pen = DrawManager()
    def analyze(self, frame):
        return [self.get_points_of_interest(frame, (x,y,w,h)) 
                for (x,y,w,h),n 
                in self.detect_faces(frame)]
    
    def get_points_of_interest(self, img, roi, numpoints=15):
        """
        Use cv.GoodFeaturesToTrack() to get points over a region of interest,
        then order and quantize the resulting list.
        
        ** All data processing should happen from this function.
        """
        cropped = self.crop(img, roi)
        
        g_img = self.get_grayscale(cropped)
        eig_image = cv.CreateMat(g_img.rows, g_img.cols, cv.CV_32FC1)
        temp_image = cv.CreateMat(g_img.rows, g_img.cols, cv.CV_32FC1)
        
        features = cv.GoodFeaturesToTrack(g_img,
                                          eig_image, 
                                          temp_image, 
                                          numpoints,
                                          0.001, # quality level -- lower is better
                                          0.01, 
                                          useHarris = True)

        return [self.quantize((x, y), roi[2:], 3.0) for x, y in features]
        
    
    def quantize(self, pt, size, grain=5.0):
        """
        There has got to be a more elegant way to quantize a point
        """
        stepx = size[0] / grain
        stepy = size[1] / grain
        quantx = 0
        quanty = 0
    
        while abs(quantx - pt[0]) > (stepx / 2.0):
            quantx += stepx
        while abs(quanty - pt[1]) > (stepy / 2.0):
            quanty += stepy
    
        return (quantx / size[0], quanty / size[1])
    
    def crop(self, img, roi):
        cv.SetImageROI(img, roi)
        cropped = cv.CreateImage(roi[2:], img.depth, img.nChannels)
        cv.Copy(img, cropped)
        cv.ResetImageROI(img)
        return cropped
        
    def detect_faces(self, frame):
        g_img = self.get_grayscale(frame)
        storage = cv.CreateMemStorage(0)
        cv.EqualizeHist(g_img, g_img)
        return cv.HaarDetectObjects(g_img, self.cascade, storage)
    
    def get_grayscale(self, frame):
        gray = cv.CreateMat(frame.height, frame.width, cv.CV_8U)
        cv.CvtColor(frame, gray, cv.CV_RGB2GRAY)
        return gray

    def draw(self, image, data):
        self.pen.draw(image, data)


class DrawManager(object):
    """
    Calls to pygame.pen go here, along with the corresponding configuration 
    data.
    """
    def __init__(self):
        self.drawfuncs = [self.draw_circle,
                          self.draw_line,
                          self.draw_arc]
        self.pen_width = 5
        self.pen_color = pygame.Color(random.randrange(0, 255),
                                      random.randrange(0, 255),
                                      random.randrange(0, 255))
    def draw(self, image, data):
        for face in data:
            scaled = [(x*image.get_width(), y*image.get_height()) for x, y in face]
            numpoints = len(scaled)
            for i in range(numpoints):
                random.choice(self.drawfuncs)(image, scaled, i)


    def draw_line(self, image, data, i):        
        print data[i-1]
        
        pygame.draw.line(image, 
                         self.pen_color, 
                         data[i-1], 
                         data[i],
                         self.pen_width)
    
    def draw_circle(self, image, data, i):
        
        pygame.draw.circle(image,
                           self.pen_color,
                           [int(n) for n in data[i]],
                           25, # radius
                           self.pen_width   # width
                           )

    def draw_arc(self, image, data, i):
        # (Surface, color, Rect, start_angle, stop_angle, width=1)
        n = self.nearest_index(data[i], data)
        size = (abs(data[i][0] - data[n][0]), 
                abs(data[i][1] - data[n][1]))
        size = max(size[0], size[1]), max(size[0], size[1])
        if size == 0.0:
            return
        rect = (data[i], size)
        pygame.draw.arc(image,
                        self.pen_color,
                        rect, # rect
                        random.choice([math.pi * 0.5, 0]),
                        random.choice([math.pi * 0.5 + math.pi, math.pi]),
                        self.pen_width # width
                        )
    
    def nearest_index(self, loc, pts):
        min = get_distance((0, 0), (2**16, 2**16))
        lind = 0
        for ind in range(len(pts)):
            distance = get_distance(loc, pts[ind])
            if (distance < min) and (distance > 0):
                min = distance
                lind = ind
    
        return lind
    


def get_distance(start, end):
    a = abs(end[0] - start[0])
    b = abs(end[1] - start[1])
    return math.sqrt(pow(a,2) + pow(b, 2))

def testz():
    capture = cv.CaptureFromCAM(0)
    if not capture:
        print "Could not get the cam. Crashing now..."
        sys.exit(1)
        
    faec = Faces(capture)
    print faec.get_image()
    sys.exit(0)

def test():
    import trans
    trans.test()

if __name__ == "__main__":
    test()

