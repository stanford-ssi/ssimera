# -*- coding: utf-8 -*-
"""
Various methods of drawing scrolling plots.
"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from panda_db import PandaDB
import sys

win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle('pyqtgraph example: Scrolling Plots')

test = PandaDB()

win.nextRow()
p3 = win.addPlot()
# Use automatic downsampling and clipping to reduce the drawing load
p3.setDownsampling(mode='peak')
p3.setClipToView(True)
p3.setRange(xRange=[-100, 0])
p3.setLimits(xMax=0)
curve3 = p3.plot()


def update2():
    global data3, ptr3
    tmp = np.empty(0)
    series = test.get_data().dropna()
    data = series.to_numpy()
    idx = series.index.to_numpy()
    curve3.setData(idx,data)
    curve3.setPos(-idx[-1:], 0)

# update all plots
def update():
    update2()


timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)


# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
