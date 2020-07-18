'''
SerialReader creates a thread to read charecters from a serial port, and packages them into timestamped lines of UTF8 text.
'''

from serial import *
from collections import deque
import threading


class SerialReader():
    def __init__(self, serialPort, baud=115200):
        self.port_name = serialPort
        self.q = deque()
        self.serial = Serial(serialPort, baud)

        self.reader_alive = True
        self.receiver_thread = threading.Thread(target=self.readSerial)
        self.receiver_thread.daemon = True
        self.receiver_thread.start()
        self.decode_err_counter = 0

    def stop(self):
        self.reader_alive = False
        if hasattr(self.serial, 'cancel_read'):
            self.serial.cancel_read()
        self.receiver_thread.join()

    def getLines(self):
        lines = []
        while self.q:
            lines += self.q.pop()
        return lines

    def readSerial(self):
        serBuffer = ""
        try:
            while self.reader_alive & self.serial.is_open:
                c = self.serial.read()  # attempt to read a character from Serial

                # check if character is a delimeter
                if c == b'\r':
                    c = b''  # don't want returns. chuck it

                if c == b'\n':
                    self.q.appendleft(
                        (serBuffer, self.port_name, time.time_ns()))
                    serBuffer = ""  # empty the buffer

                else:
                    try:
                        serBuffer += c.decode("utf-8")  # add to the buffer
                    except UnicodeDecodeError as a:
                        self.decode_err_counter += 1
        except SerialException:
            self.reader_alive = False
            self.serial.close()
