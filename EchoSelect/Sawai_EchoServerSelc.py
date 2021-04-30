import select
import socket
import sys

def main():
    ADDR = '127.0.0.1'
    PORT = 7
    MAXLINE = 4096
    sockets = [] #Holds all sockets including the server
    reply = []#Hold all messages to be send


    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((ADDR, PORT))
    serverSocket.setblocking(False)

    serverSocket.listen(5)
    sockets.append(serverSocket)

    sfd = serverSocket.fileno() 
    
    print('Server is listening...')
    while True: 
        try:
            rlist, wlist, _ = select.select(sockets, sockets, [])
            for sock in rlist:
                #If this is a server socket, accept incoming connection
                if sock.fileno() == sfd:
                    clientSocket, clientAddress = sock.accept()
                    sockets.append(clientSocket)
                #If this is a client socket, receive the message
                else:
                    message = sock.recv(MAXLINE)
                    if message:
                        print(message.decode())
                        reply.append((sock, message))
            for sock in wlist:
                for s in reply:
                    if sock.fileno() == s[0].fileno():
                        sock.send(s[1])
                        reply.pop(reply.index(s))
        except KeyboardInterrupt:
            serverSocket.close()
            break
    sys.exit('Closing server...')
        
    
if __name__ == '__main__':
    main()
