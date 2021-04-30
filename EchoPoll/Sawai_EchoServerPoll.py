import socket
from select import poll

def main():
    ADDR = '127.0.0.1'
    PORT = 7
    MAXLINE = 4096

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((ADDR, PORT))
    serverSocket.setblocking(False)
    serverSocket.listen(5)

    # pollObj = poll
    # pollObj.poll()
    # # pollObj.register(serverSocket.fileno())

    # # while True:
    # #     sock = pollObj.poll()
    # #     print(sock)


if __name__ == '__main__':
    main()