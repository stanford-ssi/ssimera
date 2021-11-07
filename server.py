#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import datetime
import random

from line_parser import LineParser
from serial_manager import SerialManager

import json
import time

class TelemHandler(object):

    def __init__(self):
        self.man = SerialManager()
        self.par = LineParser()

    def get_data(self):
        self.man.update()
        lines = self.man.getLines()
        if len(lines) > 0:
            data = [self.par.parseLine(l) for l in lines]
            return data
        return []


t = TelemHandler()

USERS = set()

async def register(websocket):
    USERS.add(websocket)

async def unregister(websocket):
    USERS.remove(websocket)

async def serve(websocket, path):
    await register(websocket)
    try:
        pass #might need to be while true
        print("hi")
    finally:
        await unregister(websocket)
        print("fuk")

start_server = websockets.serve(serve, "127.0.0.1", 5678)

asyncio.get_event_loop().run_until_complete(start_server)

while True:
    data = t.get_data()
    message = json.dumps(data)
    for user in USERS:
        user.send(message)
    time.sleep(0.1)

asyncio.get_event_loop().run_forever()


