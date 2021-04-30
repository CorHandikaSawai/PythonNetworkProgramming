import socket
import time

def main():
    MAXLINE = 4096
    ADDR = '127.0.0.1'
    PORT = 7
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((ADDR, PORT))

    while True:
        for i in range(100):
            message = str(clientSocket.fileno()) + ' ' + str(i)
            clientSocket.send(message.encode())
            mRecv = clientSocket.recv(MAXLINE).decode()
            print(mRecv)
            time.sleep(1)

if __name__ == '__main__':
    main()