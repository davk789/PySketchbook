'''
display.py

Manage the display.

Created on Jul 29, 2011

@author: davk
'''

import sys, time, math, random
from PyQt4 import QtGui, QtCore
import Transmutation_ui
import cam

class TSWindow(QtGui.QWidget):
    def __init__(self):
        super(TSWindow, self).__init__()
        self.ui = Transmutation_ui.Ui_Form()
        self.ui.setupUi(self)
        self.draw_area = TSDrawArea(self.ui.drawArea)
        self.draw_area.resize(self.ui.drawArea.width(),
                              self.ui.drawArea.height())
        self.resize(1920, 1080)

    
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.draw_area.update_points()

class TSDrawArea(QtGui.QWidget):
    def __init__(self, parent=None):
        super(TSDrawArea, self).__init__(parent)
        self.num_points = 100
        self.points = self.get_points()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        for p in self.points:
            self.draw_image(qp, p)
        qp.end()

    def get_points(self):
        points = []
        for i in range(7):
            points.append([(x * self.width(), y * self.height()) 
                           for x, y 
                           in cam.get_cam(self.num_points, "capture" + str(i) + ".jpg")])
        return points

    def update_points(self):
        self.points = self.get_points()
        self.update()

    def draw_image(self, painter, points):
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor(155, 255, random.random()*255))
        pen.setWidth(2)
        painter.setPen(pen)
        path = QtGui.QPainterPath()
        path.moveTo(QtCore.QPointF(points[0][0],
                                   points[0][1]))
        ind = 0
        used = []
        for i in range(len(points)):
            ni = self.nearest_point(points[ind], 
                                    points,
                                    used)

            ind = ni
            used.append(ind)
            nearest = points[ind]
            path.lineTo(QtCore.QPointF(nearest[0], nearest[1]))

        painter.drawPath(path)

    def nearest_point(self, loc, pts, exclude=[]):
        min = self.get_distance((0, 0), (self.width(), self.height()))
        lind = 0
        for ind in range(len(pts)):
            distance = self.get_distance(loc, pts[ind])
            if (distance < min) and (distance > 0) and (not ind in exclude):
                min = distance
                lind = ind

        return lind
            
    def get_distance(self, start, end):
        a = abs(end[0] - start[0])
        b = abs(end[1] - start[1])
        return math.sqrt(pow(a,2) + pow(b, 2))

def run():
    app = QtGui.QApplication(sys.argv)
    win = TSWindow()
    #win.showFullScreen()
    win.show()
    sys.exit(app.exec_())
     
if __name__ == "__main__":
    run()
