# gowing01selc.py
# The assignment 01 client, but using select to handle the three servers

import struct
import socket
import sys
import math
import random
import select

MAXLINE = 4096
HOST = ''
MAXVAL = 1000000
MINVAL = -MAXVAL
MAXNRVALS = 1000000
MINNRVALS = 3
SENTINAL = -1

def stddev(vals):
   avg = 0.0;
   dev = 0.0;
   tmp = 0.0;
   l = len(vals)
   
   for x in vals:
      avg += x
      
   avg /= l
   
   for x in vals:
      tmp = x - avg
      tmp *= tmp
      dev += tmp
   
   dev /= (l - 1)
   dev = math.sqrt(dev)
   return dev
   
def main():
   
   if (len(sys.argv) != 8):
      print(f"Usage {sys.argv[0]} <nrvals> <ip1> <port1> <ip2> <port2> <ip3> <port3>")
      print("<ip> and <port> pairs describe servers")
      sys.exit(1)
      
   vals = []
   mymin = MAXVAL
   mymax = MINVAL
   smin = mymin
   smax = mymax
   tmin = mymin
   tmax = mymax
   sdev = 0.0
   tdev = 0.0
   
   nrdone = 0;
   
   nrvals = int(sys.argv[1])
   
   for i in range(nrvals):
      vals.append(random.randint(1,MAXVAL+1))
      
      if vals[i] < mymin:
         mymin = vals[i]
         
      if vals[i] > mymax:
         mymax = vals[i]
   
   mydev = stddev(vals)
   
   
   s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
   h1 = sys.argv[2]
   h2 = sys.argv[4]
   h3 = sys.argv[6]
   
   p1 = int(sys.argv[3])
   p2 = int(sys.argv[5])
   p3 = int(sys.argv[7])
   
   s1.connect((h1, p1))
   s2.connect((h2, p2))
   s3.connect((h3, p3))
   
   conns = [s1, s2, s3]
   rconns = [s1, s2, s3]
   
   intstr = "!i"
   resstr = "!ii"
   resdstr = "=d"
   
   # send the values
   for i in vals:
      bytes = bytearray(struct.pack(intstr, i))
      conns[i % 3].send(bytes)
   
   bytes = bytearray(struct.pack(intstr, SENTINAL))
   
   for i in range(3):
      conns[i % 3].send(bytes)
      
      
      
   #
   # This is where it changes
   #
   
   while nrdone < 3:
      res = select.select(rconns, [], [])
      
      for sock in res[0]:
         bytes = sock.recv(struct.calcsize(resstr))
         (tmin, tmax) = struct.unpack(resstr, bytes)
         bytes = sock.recv(8)
         (tdev,) = struct.unpack(resdstr, bytes)
         sdev += tdev
      
         if tmin < smin:
            smin = tmin
         if tmax > smax:
            smax = tmax
      
         nrdone += 1
         rconns.remove(sock)
         
         print("result ", conns.index(sock)+1)
         print(f"min: {tmin}")
         print(f"max: {tmax}")
         print(f"dev: {tdev}")
         print("")
   
   sdev /= 3.0
   
   print("Local results:")
   print(f"local min: {mymin}")
   print(f"local max: {mymax}")
   print("local dev: {0:.4f}".format(mydev))
   print("")
   
   print("Server results:")
   print(f"local min: {smin}")
   print(f"local max: {smax}")
   print("local dev: {0:.4f}".format(sdev))
   
   for x in conns:
      x.close()
      
if __name__ == "__main__":
   main()