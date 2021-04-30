import select
import socket
import time

def main():
    ADDR = '127.0.0.1'
    PORT = 7
    MAXLINE = 4096
    clientSockList = []

    #Server setups
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setblocking(False)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    serverSocket.bind((ADDR, PORT))
    serverSocket.listen(5)

    #Poll setups
    poll = select.poll()
    poll.register(serverSocket)

    while True:
        try:
            socks = poll.poll()
            
            for sock in socks:
                #Receiving connections
                if sock[0] == serverSocket.fileno():
                    clientSocket, cAddr = serverSocket.accept()
                    clientSockList.append(clientSocket)
                    poll.register(clientSocket, select.POLLIN | select.POLLOUT)
                #Receiving messages and sending them back
                else:
                    for c in clientSockList:
                        if sock[0] == c.fileno() and sock[1] == (select.POLLIN | select.POLLOUT):
                            msg = c.recv(MAXLINE)
                            c.send(msg)
        except KeyboardInterrupt:
            print('Closing server....')
            break
    serverSocket.close()

if __name__ == '__main__':
    main()