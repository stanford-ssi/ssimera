# -*- coding: utf-8 -*-
"""
Various methods of drawing scrolling plots.
"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from telem_handler import TelemHandler
import sys
import time

win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle('test Plot')

test = TelemHandler()
'''
Status report:
-BMP1 is shot (but jumps down if you touch it!)
-BMP2 is negative? but seems right. (its shifted)
'''
#test.cache.set_streams(["bmi1.a.0","bmi1.a.1","bmi1.a.2","bmi2.a.0","bmi2.a.1","bmi2.a.2"])
#test.cache.set_streams(["bmi1.g.0","bmi1.g.1","bmi1.g.2","bmi2.g.0","bmi2.g.1","bmi2.g.2"])
test.cache.set_streams(["adxl1.a.0","adxl1.a.1","adxl1.a.2","adxl2.a.0","adxl2.a.1","adxl2.a.2"])
#test.cache.set_streams(["bmp1.p"])
#test.cache.set_streams(["bmp2.p"])

win.nextRow()
p3 = win.addPlot()
# Use automatic downsampling and clipping to reduce the drawing load
p3.setDownsampling(mode='peak')
p3.setClipToView(True)

curves = {}

def update():
    streams = test.get_data()
    for key,stream in streams.items():
        if key not in curves:
            curves[key] = p3.plot()
        if len(stream) > 0 :
            idx,data = stream
            curves[key].setData(idx,data)

timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)

# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
