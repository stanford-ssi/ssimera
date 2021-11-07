from influxdb import DataFrameClient
import pandas as pd
import time


# -*- coding: utf-8 -*-
"""
Various methods of drawing scrolling plots.
"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from panda_db import PandaDB
import sys
import time

win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle('pyqtgraph example: Scrolling Plots')

client = DataFrameClient(host='172.30.111.210', port=8086, database="pyexample")

win.nextRow()
p3 = win.addPlot()
# Use automatic downsampling and clipping to reduce the drawing load
p3.setDownsampling(mode='peak')
p3.setClipToView(True)
curve3 = p3.plot()


def update2():
    global data3, ptr3
    a = time.process_time()
    series = client.query("SELECT \"bmi1.a.0\" from demo")
    series = series["demo"]
    b = time.process_time()
    data = series["bmi1.a.0"].to_numpy()
    idx = series.index.astype(np.int64) / int(1e6)
    c = time.process_time()
    curve3.setData(idx,data)
    #curve3.setPos(-idx[-1:], 0)
    d = time.process_time()
    print(f"get_data: {1000*(b-a)}")

# update all plots
def update():
    update2()


timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(10)


# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
