'''
display.py

Manage the display.

Created on Jul 29, 2011

@author: davk
'''

import sys
from PyQt4 import QtGui
import Transmutation_ui
import cam

class TSDrawArea(QtGui.QWidget):
    def __init__(self, parent=None):
        super(TSDrawArea, self).__init__(parent)

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.draw_image(qp)
        qp.end()
    
    def draw_image(self, painter):
        points = cam.get_cam(10)
        for ix, iy in points:
            x = ix * self.width()
            y = iy * self.height()
            painter.drawArc(x, y, 100.0, 100.0, 0, 360.0 * 18)
    
def make_window():
    win = QtGui.QWidget()
    ui = Transmutation_ui.Ui_Form()
    ui.setupUi(win)
    draw_area = TSDrawArea(ui.drawArea)
    draw_area.resize(ui.drawArea.width(),
                     ui.drawArea.height())
    return win

def run():
    app = QtGui.QApplication(sys.argv)
    win = make_window()
    win.showFullScreen()
    sys.exit(app.exec_())
     
if __name__ == "__main__":
    run()
