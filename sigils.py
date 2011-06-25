"""
Template for sigil generation. This template file will provide a 500x500 
window with the proper event loop. Redefine the draw function.
"""

import random
import copy
import os
import glob

from PyQt4 import QtGui, QtCore, uic

class SigilWindow(QtGui.QWidget):
    """
    Contains the SigilView and its controls.
    """
    def __init__(self):
        super(SigilWindow, self).__init__()
        self.ui = uic.loadUi("ui/SigilWindow.ui", self)
        self.sigilViews = [
                           SigilDiagonals(self.ui.drawArea),
                           SigilSquare(self.ui.drawArea),
                           SigilCircle(self.ui.drawArea)
                           ]
        self.setStyleSheet("""
                           QWidget {
                               color : white;
                               background-color : black;
                           }
                           QPushButton {
                               color : black;
                               background-color : none;
                           }"""
                           )
        
        self.initWidgets()
        
    def initWidgets(self):
        "set the widget attributes"
        
        # top-level attributes
        self.setPalette(QtGui.QPalette(QtGui.QColor("black")))
        self.setWindowTitle("sigil generator")
        
        # refresh button
        self.ui.refreshButton.pressed.connect(self.updateAlgorithm)
    
        # save button
        self.ui.saveButton.pressed.connect(self.save)
        
        # create the draw controls    
        self.drawControls = []
        for view in self.sigilViews:
            self.createSpinBox(view)

    def save(self):
        image = QtGui.QPixmap.grabWidget(self.ui.drawArea, 0, 0, 500, 500)
        saveFolder = os.path.expanduser("~")
        saveFolder += os.path.sep + "Pictures" + os.path.sep + "pysigils" + os.path.sep

        if not os.path.exists(saveFolder):
            os.makedirs(saveFolder)
            counter = 0
        else:
            counter = len(glob.glob1(saveFolder, "*.jpg"))
        
        fileName = saveFolder + "pysigil" + str(counter) + ".jpg"

        if image.save(fileName):
            print "image saved successfully"
        else:
            print "there was a problem saving the image!!"


    def updateAlgorithm(self):
        self.update()
        
    def createSpinBox(self, view):
        "create a spinbox and label and set their attributes"
        
        # spinbox
        self.drawControls.append(QtGui.QSpinBox())
        #self.drawControls[-1].setPalette(QtGui.QPalette(QtGui.QColor("black")))
        self.drawControls[-1].setValue(view.numStrokes)
        self.drawControls[-1].valueChanged.connect(view.setNumStrokes)
        
        # label
        label = QtGui.QLabel()
        #label.setStyleSheet("QLabel { color : white; }");
        label.setText(view.__class__.__name__)
        
        # add them to the layout
        self.ui.controlBox.addWidget(label)
        self.ui.controlBox.addWidget(self.drawControls[-1])
    
    

class SigilView(QtGui.QWidget):
    """
    Container for sigil diagrams. To draw sigils, subclass SigilWindow and 
    redefine self.doDrawImage(painter).
    """
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        
        self.penColor = QtGui.QColor("white")

        self.penWidth = 4
        self.width = 500
        self.height = 500
        self.numStrokes = 50
        
        self.setGeometry(0, 0, self.width, self.height)        
        
    def setNumStrokes(self, num):
        self.numStrokes = num
        self.update()

    def paintEvent(self, event):
        """
        manage the setup for each draw event and pass the actual
        drawing routine to another function in this class.
        """
        
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawImage(qp)
        qp.end()

    def drawImage(self, qp):
        """
        do the draw routine that will be run in the main event loop.
        """
        # initialize the routine
        pen = QtGui.QPen()
        pen.setColor(self.penColor)
        pen.setWidth(self.penWidth)

        qp.setPen(pen)

        # do the routine
        self.doDrawImage(qp)

    def doDrawImage(self, painter):
        """
        Virtual Function
        """
        print "this function is not implemented in this parent class!"
        return None


class SigilSquare(SigilView):
    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)
        self.numStrokes = 15
        
    def doDrawImage(self, painter):
        for i in range(self.numStrokes):
            self.makeLine(painter, random.choice([2, 4, 8, 16]))

    def makeLine(self, painter, size=4):
        x = random.randrange(33, self.width, self.width / size)
        y = random.randrange(33, self.width, self.width / size)
        offset = [self.width / size, -(self.width / size), 0]
        painter.drawLine(
            QtCore.QPoint(x, y),
            QtCore.QPoint(x + random.choice(offset), y + random.choice(offset)))
        

class SigilCircle(SigilView):
    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)
        self.numStrokes = 50

    def doDrawImage(self, painter):
        for i in range(self.numStrokes):
            self.makeCurve(painter, random.choice([2, 4, 8, 16]))
            
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
                self.width / size),
            random.randrange(-180, 180, 90) * 16,
            random.randrange(-180, 180, 90) * 16)


class SigilDiagonals(SigilView):
    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)

        self.segLength = 45
        self.spread = 0.5
        self.numStrokes = 5
        
        step = self.width / 5
        self.grid = range(step, self.width, step)

    def doDrawImage(self, painter):
        # i wish i knew what to do here without .collect(...)
        self.starts = []
        for i in range(self.numStrokes):
            self.starts.append(QtCore.QPoint(random.choice(self.grid), random.choice(self.grid)))
        
        for start in self.starts:
            path = QtGui.QPainterPath()
            direction = QtCore.QPoint(
                random.randrange(-1, 2), 
                random.randrange(-1, 2))
            self.walk(path, start, direction)

            painter.drawPath(path)

    def drawStroke(self, path, start, end):
        "Add a segment to the drawing path."
        # convert QPoint to QPointF specifically for this function
        if start.x() < end.x():
            vx = start.x()
        else:
            vx = end.x()
        if start.y() < end.y():
            vy = start.y()
        else:
            vy = end.y()

        vertex = QtCore.QPointF(vx, vy)
        fend = QtCore.QPointF(end)
        path.quadTo(vertex, fend)

    def walk(self, path, qstart, direction):
        """
        Walk a random path at multiples of 45 degree angles.
        """
        qloc = copy.copy(qstart)

        path.moveTo(QtCore.QPointF(qloc))

        for i in range(500):
            old = copy.copy(qloc)
            qloc += QtCore.QPoint(
                self.getDirection(direction.x()) * self.segLength, 
                self.getDirection(direction.y()) * self.segLength)
            self.drawStroke(path, qloc, old)

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
    #sw = SigilDiagonals()
    sw = SigilWindow()
    sw.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    
