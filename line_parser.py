import json
from json import JSONDecodeError
import msgpack
import base64

def flatten(data, prefix=""):
	'''
	Converts a heiarchical dict data structure into flat dict, with an "a.b.c" key namespace
	'''
	flat = dict()
	if isinstance(data, dict):
		if prefix:
			prefix += "."
		for k, v in data.items():
			flat.update(flatten(v, prefix + str(k)))
		return flat
	if isinstance(data, list):
		if prefix:
			prefix += "."
		i = 0
		for v in data:
			flat.update(flatten(v, prefix + str(i)))
			i += 1
		return flat
	return {prefix: data}


'''
LineParser converts a string (from the serial port) into a python data structure. It accepts JSON and Base64 MsgPack formats.
'''
class LineParser():

	def __init__(self):
		self.json_count = 0
		self.base64_count = 0
		self.fail_count = 0

	def parseLine(self, line):
		''' Takes a 3-tuple: the string of recived data, the originating serial port, and the timestamp in ns'''
		# First, try
		try:
			data = json.loads(line[0])
			self.json_count += 1
		except JSONDecodeError:
			try:
				byte_msg = base64.b64decode(line[0])
				data = msgpack.unpackb(byte_msg)
				self.base64_count += 1
			except Exception as e:
				self.fail_count += 1
				print(f"Failed to parse line: {line[0]}")
				data = []
				# Needs to be implemented!
		flat = flatten(data)
		flat["serial_port"] = line[1]
		flat["telem_time"] = line[2]
		return flat
