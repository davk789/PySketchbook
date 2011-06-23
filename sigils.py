"""
Template for sigil generation. This template file will provide a 500x500 
window with the proper event loop. Redefine the draw function.
"""


import math
import random
import copy

from PyQt4 import QtGui, QtCore

class SigilWindow(QtGui.QWidget):
    """
    Container for sigil diagrams. To draw sigils, subclass SigilWindow and 
    redefine self.doDrawImage(painter).
    """
    def __init__(self):
        QtGui.QWidget.__init__(self)
        
        self.foregroundColor = QtGui.QColor("white")
        self.backgroundColor = QtGui.QColor("black")

        self.penWidth = 7
        self.width = 500
        self.height = 500
        
        self.initUI()
        
    def initUI(self):
        self.setGeometry(300, 300, self.width + 70, self.height + 70)
        self.setWindowTitle('Sigil Test')
        # set the background color
        self.setPalette(QtGui.QPalette(self.backgroundColor))

    def paintEvent(self, event):
        """
        manage the setup for each draw event and pass the actual
        drawing routine to another function in this class.
        """
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawImage(event, qp)
        qp.end()        

    def mousePressEvent(self, event):
        self.update()

    def drawImage(self, event, qp):
        """
        do the draw routine that will be run in the main event loop.
        """
        pen = QtGui.QPen()
        pen.setColor(self.foregroundColor)
        pen.setWidth(self.penWidth)

        qp.setPen(pen)

        self.doDrawImage(qp)

    def doDrawImage(self, painter):
        """
        Virtual Function
        """
        print "this function is not implemented in this parent class!"
        return None


class SigilSquareCircle(SigilWindow):
    def __init__(self):
        super(SigilSquareCircle, self).__init__()

        
    def doDrawImage(self, painter):
        
        for i in range(50):
            self.makeCurve(painter, random.choice([2, 4, 8, 16]))

        for i in range(15):
            self.makeLine(painter, random.choice([2, 4, 8, 16]))

            
    def makeCurve(self, painter, size=4):
        """
        curve based on 90 degree angles, placed randomly on a grid of 
        different resolutions.
        """
        painter.drawArc(
            QtCore.QRectF(
                random.randrange(33, self.width, self.width / size),
                random.randrange(33, self.width, self.width / size),
                self.width / size,
                self.width / size
                ),
            random.randrange(-180, 180, 90) * 16,
            random.randrange(-180, 180, 90) * 16
            )

    def makeLine(self, painter, size=4):
        x = random.randrange(33, self.width, self.width / size)
        y = random.randrange(33, self.width, self.width / size)
        offset = [self.width / size, -(self.width / size), 0]
        painter.drawLine(
            QtCore.QPoint(x, y),
            QtCore.QPoint(x + random.choice(offset), y + random.choice(offset))
            )

class SigilDiagonals(SigilWindow):
    def __init__(self):
        super(self.__class__, self).__init__()

        self.penWidth = 1
        self.segLength = 20
        self.spread = 0.5
        
        numNodes = 5
        step = self.width / numNodes
        self.grid = range(step, self.width, step)
        self.starts = []
        for i in range(5):
            self.starts.append(QtCore.QPoint(random.choice(self.grid), random.choice(self.grid)))

    def doDrawImage(self, painter):
        for start in self.starts:
            path = QtGui.QPainterPath()
            direction = QtCore.QPoint(
                random.randrange(-1, 2), 
                random.randrange(-1, 2))
            self.walk(path, start, direction)
            painter.drawPath(path)

    def drawStroke(self, path, end):
        "change which stroke in subclasses"
        # convert QPoint to QPointF specifically for this function
        fend = QtCore.QPointF(end)
        path.lineTo(fend)#fstart, fend)

    def walk(self, path, qstart, direction):
        qloc = copy.copy(qstart)

        path.moveTo(QtCore.QPointF(qloc))

        for i in range(500):
            qloc += QtCore.QPoint(
                self.getDirection(direction.x()) * self.segLength, 
                self.getDirection(direction.y()) * self.segLength)
            self.drawStroke(path, qloc)

    def getDirection(self, weight):
        """
        given -1, 0, 1 return random number weighted towards the given value
        stolen from http://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python/"""
        remainder = (1 - self.spread) / 2
        if weight > 0:
            weights = [remainder, remainder, self.spread]
        elif weight < 0:
            weights = [self.spread, remainder, remainder]
        else: 
            weights = [remainder, self.spread, remainder]

        # stolen section
        rnd = random.random() * sum(weights)
        for i, w in enumerate(weights):
            rnd -= w
            if rnd < 0:
                return i - 1

def main():
    import sys
    print "testing SigilWindow subclasses"
    app = QtGui.QApplication(sys.argv)
    #sw = SigilSquareCircle()
    sw = SigilDiagonals()
    sw.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    
