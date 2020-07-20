from line_parser import LineParser
from serial_manager import SerialManager
from plot_cache import PlotCache

class TelemHandler(object):

    def __init__(self):
        self.man = SerialManager()
        self.par = LineParser()
        self.cache = PlotCache()

    def get_data(self):
        self.man.update()
        lines = self.man.getLines()
        if len(lines) > 0:
            data = [self.par.parseLine(l) for l in lines]
            self.cache.process_data(data)
        return self.cache.get()