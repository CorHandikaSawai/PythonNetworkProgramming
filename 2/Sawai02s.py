import socket
import struct
import ipaddress
import statistics
import select
import signal
import sys

 
def main():
    PORT = 8001
    ADDR = ''
    readSock = []
    data = []
    maxScore = []
    
    #Create socket, bind, and listen on the address and port
    ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssock.bind((ADDR, PORT))
    ssock.setblocking(False)
    ssock.listen(5)
    readSock.append(ssock)

    while True:
        try:
            #This will stuck, but still accept new connections
            reads, writes, excepts = select.select(readSock, [], [])
            
            for sock in reads:
                #If this is a server socket, then accept new connections
                if sock == ssock:
                    #Accept connection and print out client info
                    cSock, addr = sock.accept()
                    cSock.setblocking(False)
                    print('Connection received from', str(addr[0]) + ":" + str(addr[1]))
                    cSock.send('COURSEID'.encode())
                    readSock.append(cSock)
                    # dataQueues[cSock] = queue.Queue()
                else:
                    sock.setblocking(1)
                    #Receive information about the course
                    data = sock.recv(struct.calcsize('!4s2h'))
                    course, number , section = struct.unpack('!4s2h', data)
                    print('Received', course.decode(), number, section)
                    
                    #Send respond asking for 'MAX SCORE'
                    sock.send(struct.pack('!9s','MAX SCORE'.encode()))
                    
                    #Receive information about the max score
                    data = sock.recv(struct.calcsize('!h'))
                    maxScore = struct.unpack('!h', data)
                    print('Received maxscore of', maxScore[0])
                    
                    #Send respond 'BEGIN'
                    sock.send(struct.pack('!5s','BEGIN'.encode()))
                    
                    #Receive student scores one packet at a time and process them
                    validList = []
                    invalidList = []
                    while True:
                        data = sock.recv(struct.calcsize('!ih'))
                        studentId, score = struct.unpack('!ih', data)
                        if studentId == score == -1:
                            print('Sentinel received')
                            break
                        elif score > maxScore[0]:
                            invalidList.append([studentId, score])
                        else:
                            print('Score recieved', studentId, score)
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
                    sock.send(packet)
                    
                    #Receive respond 'ERRORS' and sending all invalid scores to client
                    data = sock.recv(4096).decode()
                    if data == 'ERRORS':
                        #Send respond 'ERRORS' and sending all invalid scores to client
                        sock.send(struct.pack('!6s','ERRORS'.encode()))
                        for x in invalidList:
                            packet = struct.pack('!ih', int(x[0]), int(x[1]))
                            sock.send(packet)
                        #Send sentinal value to tell the client it is done sending packets
                        packet = struct.pack('!ih', -1, -1)
                        sock.send(packet)
                    print('Source:', str(ip) + ':' + str(port))
                    print('Course:', course)
                    print('Total:', scoresRecv)
                    print('Min:', low)
                    print('Max:', high)
                    print('Average:',round(avg, 2))
                    print('Dev:',round(stdev, 2))
                    print('Closing connection with', str(addr[0]) + ":" + str(addr[1]))
                    print()
                    
                    readSock.remove(sock)
                    sock.close()
                    
        except Exception:
            sys.exit(0)
            
if __name__ == "__main__":
    main()