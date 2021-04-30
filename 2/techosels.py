# techosels.py
# single-threaded echo server using tcp and select
# python 3

import socket
import select
import time
import struct


def main():
    PORT = 7
    MAXLINE = 4096
    readSocks = []
    writeSocks = []

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", PORT))
    server.listen(5)
    server.setblocking(0)
    readSocks.append(server)
    sfd = server.fileno()
    
    while True:
        reads, writes, excepts = select.select(readSocks, writeSocks, [])
        
        for sock in reads:
            if sock.fileno() == sfd:    
                client, addr = server.accept()
                readSocks.append(client)
                writeSocks.append(client)
            else:
                data = sock.recv(4096).decode()
                if data:
                    print(data)
                    for sock in writes:
                        sock.send(data.encode())
            
           
                    
           

if __name__ == "__main__":
    main()
