from collections import deque

class PlotCache():
    
    def __init__(self):
        self.data = {}

    def process_data(self,new_data):
        for entry in new_data:
            for key in self.data.keys():
                if (key in entry) and ('tick' in entry):
                    pair = (entry['tick'], entry[key])
                    self.data[key].append(pair)

    def get(self):
        streams = {}
        for key in self.data.keys():
            streams[key] = tuple(zip(*self.data[key]))
        return streams

    def set_streams(self,streams):
        #clean out old keys
        for key in self.data:
            if key not in streams:
                self.data.pop(key)
        for key in streams:
            if key not in self.data:
                self.data[key] = deque(maxlen=1000)