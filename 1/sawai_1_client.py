# /////////////////////////////////////////////////////////////////// 
# // Student name: Cor Handika Sawai
# // Course: COSC 4653 - Advanced Networks
# // Assignment: #1 - Min-Max-StdDev Distributed Processing
# // File name: sawai_1_client.py
# // Program's Purpose: The client program shall create a list of randomly-generated positive integers,
# //                    pass a third of the list to each of three servers, read the minimum, maximum,
# //                    and stddev values returned by each server, and print the combined minimum, maximum,
# //                    and average of the stddev values.
# // 
# // Program's Limitations: There has to be exactly 3 servers and assuming inputs are valid
# // Development Computer: Xidax pc
# // Operating System: Windows 10
# // Integrated Development Environment (IDE): Notepad++ & Command Prompt
# // Compiler: Python3 
# // Program's Operational Status: Work as expected
# ///////////////////////////////////////////////////////////////////
import sys
import random
import socket
import statistics
import time
import struct

def main():
    
    numbers = []
    clientTest = []
    address = []
    ports = []
    sockList = []
    dataRecv = []
    sentinel = -1
    structSend = struct.Struct("!i")
    structRecv = struct.Struct("!iif")
    
    if  len(sys.argv) != 8 or int(sys.argv[1]) < 3:
        sys.exit("Usage: py sawai_1_client <#integers> <First IP address>"
            + " <First port number> <Second IP address> <Second port number>"
            + " <Third IP address> <Third port number>"
            + "\nNote: The #integers should be greater than or equal to 3")
    
    #Create random numbers   
    for x in range(int(sys.argv[1])):
        temp = random.randint(1, 1000000)
        numbers.append(temp)
        clientTest.append(temp)
    
    #Get a list of address, ports, and create sockets for each servers
    for x in range(2, len(sys.argv), 2):
        address.append(sys.argv[x])
        ports.append(int(sys.argv[x+1]))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockList.append(sock)
    
    print(numbers)
    #Connect to each server
    for x in range(len(ports)):
        sockList[x].connect((address[x], ports[x]))    
    
    #send data to each server one number at a time
    i = 0
    while len(numbers) > 0:
        if i >= 3:
            i = 0
        sockList[i].send(structSend.pack(numbers.pop()))
        i+=1
            
    for x in range (3):
        sockList[x].send(structSend.pack(sentinel))
                    
    for x in range(len(sockList)):
        temp = structRecv.unpack(sockList[x].recv(struct.calcsize("!iif")))
        dataRecv.append(temp)
    
    #compute the combined minimum and maximum values
    print()
    print("Results computed by the servers:")
    print("Minimum value:", min(int(dataRecv[0][0]), int(dataRecv[1][0]), int(dataRecv[2][0])))
    print("Maximum value:", max(int(dataRecv[0][1]), int(dataRecv[1][1]), int(dataRecv[2][1])))
    print("Standard deviation value: {:.1f}".format((float(dataRecv[0][2]) + float(dataRecv[1][2]) + float(dataRecv[2][2]))/3.0))
    
    #client shall independently find the minimum, maximum and stddev values
    print()
    print("Results computed by the client from data sent by the servers:")
    print("Minimum value:", min(clientTest))
    print("Maximum value:", max(clientTest))
    print("Standard deviation value: {:.1f}".format(statistics.stdev(clientTest)))
    
    #Close all sockets
    for x in range(len(sockList)):
        sockList[x].close()
        
if __name__ == "__main__":
    main()
    