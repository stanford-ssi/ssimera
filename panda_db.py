from line_parser import LineParser
from serial_manager import SerialManager
import time
import pandas as pd

class PandaDB(object):

    def __init__(self):
        self.man = SerialManager()
        self.par = LineParser()
        self.bigframe = pd.DataFrame()

    def get_data(self):
        self.man.update()
        lines = self.man.getLines()
        if len(lines) > 0:
            data = [self.par.parseLine(l) for l in lines]
            frame = pd.DataFrame.from_records(data,index="tick")
            self.bigframe = self.bigframe.append(frame)
        x = self.bigframe["bmi1.a.1"]
        return x