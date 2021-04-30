from socket import *
import struct
import ipaddress
import statistics
import math


def main():
    PORT = 8001
    ADDR = ''
    
    #Create socket, bind, and listen on the address and port
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((ADDR, PORT))
    sock.listen(1)
    
    #Accept connection and print out client info
    cSock, addr = sock.accept()
    print('Connection received from', str(addr[0]) + ":" + str(addr[1]))
    
    #Send respond asking for 'COURSEID'
    cSock.send('COURSEID'.encode())
    
    #Receive information about the course
    data = cSock.recv(struct.calcsize('!4s2h'))
    course, number , section = struct.unpack('!4s2h', data)
    print('Received', course.decode(), number, section)
    
    #Send respond asking for 'MAX SCORE'
    cSock.send(struct.pack('!9s','MAX SCORE'.encode()))
    
    #Receive information about the max score
    data = cSock.recv(struct.calcsize('!h'))
    maxScore = struct.unpack('!h', data)
    print('Received maxscore of', maxScore[0])
    
    #Send respond 'BEGIN'
    cSock.send(struct.pack('!5s','BEGIN'.encode()))
    
    #Receive student scores one packet at a time and process them
    validList = []
    invalidList = []
    while True:
        data = cSock.recv(struct.calcsize('!ih'))
        studentId, score = struct.unpack('!ih', data)
        print('Score recieved', studentId, score)
        
        if studentId == score == -1:
            print('Sentinel received')
            break
        elif score > maxScore[0]:
            invalidList.append([studentId, score])
        else:
            validList.append(score)
    
    ip = int(ipaddress.IPv4Address(addr[0]))
    port = int(addr[1])
    course = course.decode() + str(number) + "-0" + str(section)
    scoresRecv = len(validList) + len(invalidList)
    valid = len(validList)
    low = min(validList)
    high = max(validList)
    avg = statistics.mean(validList)
    stdev = statistics.stdev(validList)
    
    #Build a packet containing all computations 
    a = struct.pack('!iH11shhhh', ip, port, course.encode(), scoresRecv, valid, low, high)
    b = struct.pack('ff', avg, stdev)
    packet = a + b
    cSock.send(packet)
    
    #Receive respond 'ERRORS' and sending all invalid scores to client
    data = cSock.recv(4096).decode()
    if data == 'ERRORS':
        #Send respond 'ERRORS' and sending all invalid scores to client
        cSock.send(struct.pack('!6s','ERRORS'.encode()))
        for x in invalidList:
            packet = struct.pack('!ih', int(x[0]), int(x[1]))
            cSock.send(packet)
        #Send sentinal value to tell the client it is done sending packets
        packet = struct.pack('!ih', -1, -1)
        cSock.send(packet)
            
    cSock.close()
    
    #TODO: Have the server to continue listening
    sock.close()
    
if __name__ == "__main__":
    main()