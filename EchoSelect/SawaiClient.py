import socket
import time

def main():
    ADDR = '127.0.0.1'
    PORT = 7
    MAXLINE = 4096

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((ADDR, PORT))

    for i in range(20):
        clientSocket.send((str(clientSocket.fileno()) + ' ' + str(i)).encode())
        msg = clientSocket.recv(MAXLINE).decode()
        print(msg)
        time.sleep(1)

if __name__ == '__main__':
    main()