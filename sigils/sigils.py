"""
Template for sigil generation. This template file will provide a 500x500 
window with the proper event loop. Redefine the draw function.
"""

import random
import os
import glob

from PyQt4 import QtGui, QtCore#, uic
# use pre-compiled version of the ui file
import SigilWindow_ui

class SigilWindow(QtGui.QWidget):
    """
    Contains the SigilView and its controls.
    """
    def __init__(self):
        super(SigilWindow, self).__init__()
        #self.ui = uic.loadUi("ui/SigilWindow.ui", self)
        self.ui = SigilWindow_ui.Ui_Form()
        self.ui.setupUi(self)
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
            view.refresh()

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
        for view in self.sigilViews:
            view.refresh()
            view.update()
        
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
        
        self.figureData = []
        
        self.setGeometry(0, 0, self.width, self.height)        
        
    def setNumStrokes(self, num):
        self.numStrokes = num
        self.refresh()
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
        print "this function must be implemented by the subclass!"
        return None
    
    def refresh(self):
        """Virtual Function
        Update the data points describing the figure.
        """
        print "this function must be implemented by the subclass!"
        return None


class SigilSquare(SigilView):
    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)
        self.numStrokes = 15
        
    def doDrawImage(self, painter):
        for data in self.figureData:
            painter.drawLine(
                QtCore.QPoint(data[0], data[1]),
                QtCore.QPoint(data[0] + data[2], data[1] + data[3]))
    
    def refresh(self):
        self.figureData = []
        for i in range(self.numStrokes):
            size = random.choice([2, 4, 8, 16])
            x = random.randrange(33, self.width, self.width / size)
            y = random.randrange(33, self.width, self.width / size)
            directions = [self.width / size, -(self.width / size), 0]
            ox = random.choice(directions)
            oy = random.choice(directions)
            self.figureData.append((x, y, ox, oy))


class SigilCircle(SigilView):
    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)
        self.numStrokes = 15

    def doDrawImage(self, painter):
        for data in self.figureData:
            painter.drawArc(
                            QtCore.QRectF(data[0], data[1], data[2], data[3]), 
                            data[4], 
                            data[5])
    
    def refresh(self):
        self.figureData = []
        for i in range(self.numStrokes):
            size = random.choice([2, 4, 8, 16])
            x = random.randrange(33, self.width, self.width / size)
            y = random.randrange(33, self.width, self.width / size)
            w = self.width / size
            h = self.width / size
            sa = random.randrange(-180, 180, 90) * 16
            ea = random.randrange(-180, 180, 90) * 16
            self.figureData.append((x, y, h, w, sa, ea))
            
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
        self.numStrokes = 1
        self.numSegments = 50
        
        step = self.width / 5
        self.grid = range(step, self.width, step)
            
    def doDrawImage(self, painter):
        """
        iterate over self.figureData to draw the line
        """
        path = QtGui.QPainterPath()
        
        for data in self.figureData:
            path.moveTo(QtCore.QPointF(data[0][0], data[0][1]))
            for ind in range(1, len(data)):
                loc = QtCore.QPointF(data[ind][0], data[ind][1])
                old = QtCore.QPointF(data[ind - 1][0], data[ind - 1][1])
                vertex = self.getVertex(loc, old)
                path.quadTo(vertex, loc)
        
        painter.drawPath(path)
            
    def getVertex(self, start, end):
        "randomly choose between upper and lower curve point"
        vx = random.choice([start.x(), end.x()])
        vy = random.choice([start.y(), end.y()])
        return QtCore.QPointF(vx, vy)
    
    def refresh(self):
        """ 
        collect the data from the random walks. start with 
        """
        self.starts = []
        for i in range(self.numStrokes):
            self.starts.append((random.choice(self.grid), random.choice(self.grid)))
        
        self.figureData = []
        for start in self.starts:
            directionX = random.randrange(-1,2)
            directionY = random.randrange(-1,2)

            path = self.walk(start, directionX, directionY)
            self.figureData.append(path)

    def walk(self, start, directionX, directionY):
        "do a random walk and add the steps to a return array"
        ret = []
        loc = start # removing the copy calls since there is no drawing yet
        ret.append(loc)
        for i in range(self.numSegments):
            loc = (loc[0] + self.getDirection(directionX) * self.segLength,
                   loc[1] + self.getDirection(directionY) * self.segLength)
            ret.append(loc)
        
        return ret
    
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
    print "testing SigilView subclasses"
    app = QtGui.QApplication(sys.argv)
    #sw = SigilDiagonals()
    sw = SigilWindow()
    sw.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    
