import sys
import struct

FILE = sys.argv[1]
f = open(FILE, 'r')
fileData = f.read().split()

readydata = struct.pack('!4s', fileData.pop(0).encode())
a = struct.pack('!h', int(fileData.pop(0)))
print(readydata, a)