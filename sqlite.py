from influxdb import DataFrameClient
import pandas as pd
from serial_manager import SerialManager
from line_parser import LineParser
import time

class RealDB(object):

    def __init__(self):
        self.client = DataFrameClient(host='172.30.111.210', port=8086, database="pyexample")
        self.man = SerialManager()
        self.par = LineParser()
        self.bigframe = pd.DataFrame()

    def process_data(self):
        self.man.update()
        lines = self.man.getLines()
        if len(lines) > 0:
            try:
                data = [self.par.parseLine(l) for l in lines]
                frame = pd.DataFrame.from_records(data)
                frame['time_tick'] = pd.to_datetime(frame['tick'], unit='ms')
                frame = frame.set_index('time_tick')
                frame = frame.astype({"bmp1.t": float,"bmp2.t": float, "bmp1.p": float, "bmp2.p": float, "tick": int })
                self.client.write_points(frame,"demo")
            except Exception:
                pass
            #print("Sent!")


test = RealDB()
while True:
    time.sleep(0.05)
    test.process_data()