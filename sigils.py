"""
sigils.py

create sigils randomly, using predetermined layout points and shapes.

hacked from an example at http://zetcode.com/tutorials/pyqt4/drawing/
"""

import math
import random

from PyQt4 import QtGui, QtCore

class SigilWindow(QtGui.QWidget):
  
    def __init__(self):
        QtGui.QWidget.__init__(self)
        
        self.foregroundColor = QtGui.QColor("white")
        self.backgroundColor = QtGui.QColor(50, 0, 0)

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
        pen.setWidth(7)

        qp.setPen(pen)

        for i in range(50):
            self.makeCurve(qp, random.choice([2, 4, 8, 16]))

        for i in range(15):
            self.makeLine(qp, random.choice([2, 4, 8, 16]))
            
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

def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    sw = SigilWindow()
    sw.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    
