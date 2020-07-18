'''
SerialManager manages all connected serial devices.
It is greedy, and tries to connect to as many serial devices as possible.
For each connected port, it will spin off a SerialReader to read the port, and 
produce lines of data, annotated with a port name and timestamp.
'''

from serial.tools import list_ports
from serial_reader import SerialReader


class SerialManager():

    def __init__(self):
        self.readers = {}

    def update(self):
        for p in list(self.readers.keys()):
            if not self.readers[p].reader_alive:
                print(f"Port {p} Disconnected!")
                self.readers.pop(p)

        for port in list_ports.comports():
            if port.device not in self.readers:
                try:
                    reader = SerialReader(port.device)
                except Exception:
                    print(f"Failed to Connect to {port.device}!")
                else:
                    self.readers[port.device] = reader
                    print(f"Port {port.device} Connected!")

    def getLines(self):
        lines = []
        for reader in self.readers.values():
            lines += reader.getLines()
        return lines


'''This is a basic self-test script that tests auto-connect and line-reading'''
if __name__ == "__main__":
    man = SerialManager()
    while True:
        man.update()
        print(man.getLines())
        import time
        time.sleep(0.5)
