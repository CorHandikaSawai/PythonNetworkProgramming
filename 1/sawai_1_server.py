# /////////////////////////////////////////////////////////////////// 
# // Student name: Cor Handika Sawai
# // Course: COSC 4653 - Advanced Networks
# // Assignment: #1 - Min-Max-StdDev Distributed Processing
# // File name: sawai_1_server.py
# // Program's Purpose: The server will calculate the standard deviation, minimum, and maximum value from data sent by the client.
# //                    The server shall send the current value of the minimum integer, the maximum integer, and the
# //                    double stddev (in that order) in a single packet to the client.
# // 
# // Program's Limitations: There has to be 3 servers and assuming inputs are valid
# // Development Computer: Xidax pc
# // Operating System: Windows 10
# // Integrated Development Environment (IDE): Notepad++ & Command Prompt
# // Compiler: Python3 
# // Program's Operational Status: Work as expected
# ///////////////////////////////////////////////////////////////////

import socket
import sys
import statistics
import time
import struct

def main():
    #Print out usage message
    if len(sys.argv) != 2:
        print("Usage: python sawai_1_server.py <port number>")
    
    #Declaring empty list to store data sent from client and struct format
    numbers = []
    structRecv = struct.Struct("!i")
    structSend = struct.Struct("!iif")
    
    #Creating the socket, bind ports to the local address, and listen for the incoming request
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", int(sys.argv[1])))
    s.listen()
    conn, addr = s.accept()
    print("Accepted connection from", addr)
    
    
    # if the first integer is -1 then terminate the program    
    temp = conn.recv(struct.calcsize("!i"))
    data = structRecv.unpack(temp)
    
    print(data[0])
    if data[0] == -1:
        numbers = [0, 0]
    else:
        numbers.append(data[0])
        while True: 
            data = structRecv.unpack(conn.recv(struct.calcsize("!i")))
            print(data[0])
            if data[0] == -1:
                break
            numbers.append(data[0])
    
    maxValue = max(numbers)
    minValue = min(numbers)
    stdevValue = statistics.stdev(numbers)
    
    conn.send(structSend.pack(minValue, maxValue, stdevValue))
    
    conn.close()
    s.close()
               
if __name__ == "__main__":
    main()