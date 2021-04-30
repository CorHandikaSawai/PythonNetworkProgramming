# Client
import socket
import struct
import sys
import select
import threading
import tkinter as tk

def joinServer():
    username = input('Username: ')
    while True:
        #Send username to the server, 0 is the join command
        packType = '!Bh' + str(len(username)) + 's'
        sock.send(struct.pack(packType, 0, len(username), username.encode('ASCII')))
        
        #Receive respond from server whether the name is taken or not
        data = struct.unpack('!B', sock.recv(struct.calcsize('!B')))
        if data[0] == 0:
            
            break
        
        username = input('Username rejected, enter a new username: ')

def sendMessage():
    #Get message from user and send it to server
    messageToSend = userInput.get('1.0', 'end - 1c')
    packType = '!Bh' + str(len(messageToSend)) + 's'
    sock.send(struct.pack(packType, 2, len(messageToSend), messageToSend.encode('ASCII')))

def updateChatScreen():
    while True:
        #Get message from server and print it out
        data = struct.unpack('!Bh', sock.recv(3))
        messageLen = data[1]
        messageType = '!' + str(messageLen) + 's'
        message = struct.unpack(messageType, sock.recv(struct.calcsize(messageType)))
        message = message[0].decode('ASCII')
        print(message)
        chatScreen.insert('1.0', message)


root = tk.Tk()
root.title("Chat App")
IP = '127.0.0.1'
PORT = 9000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP, PORT)) 

joinServer()

mainFrame = tk.Frame(root)
mainFrame.pack(expand=True, fill=tk.BOTH)

chatScreen = tk.Text(mainFrame, wrap="word")
chatScreen.pack(expand=True, fill=tk.BOTH)

userInput = tk.Text(mainFrame, height=5, wrap="word")
userInput.pack(side=tk.LEFT, expand=True, fill=tk.X)

sendBtn = tk.Button(mainFrame, text="Send", width=10, command=sendMessage)
sendBtn.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)


outputThread = threading.Thread(target=updateChatScreen)
inputThread = threading.Thread(target=root.mainloop())

inputThread.daemon = True
outputThread.daemon = True

inputThread.start()
outputThread.start()

inputThread.join()
outputThread.join()



