from socket import *
import struct
import sys
import time
import random
import ipaddress

def main():
    PORT = 8001
    fileData = ''
    packet = []
    
    if len(sys.argv) != 3:
        sys.exit('Usage: py Sawai02c.py <ip address> <filename>')
    
    ADDR = sys.argv[1]
    FILE = sys.argv[2]
    f = open(FILE, 'r')
    fileData = f.read().split()
    
    #Create socket and connect to the server
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((ADDR, PORT))

    #Receive respond 'COURSEID' 
    data = sock.recv(4096).decode()
    
    if data == 'COURSEID':
        #Send the course id
        packet = struct.pack('!4s2h',fileData.pop(0).encode(), int(fileData.pop(0)), int(fileData.pop(0)))
        sock.send(packet)
    else:
        sys.exit('Invalid respond:', data)
    
    #Receive respond 'MAX SCORE' from the server
    data = sock.recv(4096).decode()
    
    if data == 'MAX SCORE':
        #Send the max score
        maxScore = int(fileData.pop(0))
        sock.send(struct.pack('!h', maxScore))
    else:
        sys.exit('Invalid respond:', data)
    
    #Receive respond 'BEGIN' from the server
    data = sock.recv(4096).decode()
    
    if data == 'BEGIN':
        #Send student id and score
        for x in range(0,len(fileData),2):
            packet = struct.pack('!ih', int(fileData[x]), int(fileData[x+1]))
            sock.send(packet)
            time.sleep(random.randint(1, 3))
 
        #Send sentinal value to tell the server it is done sending packets
        packet = struct.pack('!ih', -1, -1)
        sock.send(packet)
    
        #Receive result from server
        data = sock.recv(struct.calcsize('!iH11shhhh'))
        dataFloats = sock.recv(struct.calcsize('ff'))
        ip, port, course, scoresRecv, valid, low, high = struct.unpack('!iH11shhhh', data)
        avg, stdev = struct.unpack('ff', dataFloats)
        
        print('Data from server:')
        print('IP:', ipaddress.IPv4Address(ip), "Port:", port)
        print('Course:', course.decode())
        print('Total:', scoresRecv)
        print('Valid:', valid)
        print('Min:', low)
        print('Max:', high)
        print('Average:',round(avg, 2))
        print('Dev:',round(stdev, 2))
    
        #Send an 'ERRORS'
        sock.send('ERRORS'.encode())
        
        #Receive respond 'ERRORS' from the server
        data = sock.recv(struct.calcsize('!6s')).decode()
 
        if data == 'ERRORS':
            print('Errors reported:')
            for x in range(scoresRecv - valid):
                studentId, score = struct.unpack('!ih', sock.recv(struct.calcsize('!ih')))
                print(str(studentId) + " " + str(score))
            #Receive sentinel value and close connection
            #studentId, score = struct.unpack('!ih', sock.recv(struct.calcsize('!ih')))
            if studentId == score == -1:
                sock.close()
        else:
            sys.exit('Errors when processing students scores')
           
        
    
if __name__ == '__main__':
    main()