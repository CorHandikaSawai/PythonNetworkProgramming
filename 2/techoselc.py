# techosels.py
# single-threaded echo server using tcp and select
# python 3

import socket
import select
import sys
import time
import struct
import tkinter as tk


def main():
    root = tk.Tk()
    # root.geometry("500x500")
    
    display = tk.Frame(root)
    display.grid()
    
    OutputText = tk.Text(display, bg="white")
    OutputText.grid(row=0, columnspan=2)
    
    inputText = tk.Text(display, bg="Blue")
    inputText.grid(row=1, column=0)
    
    sendBtn = tk.Button(display, text="Send", bg="red")
    sendBtn.grid(row=1, column=1)
    
    root.mainloop()
    # PORT = 7
    # MAXLINE = 4096


    # csocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # csocket.connect(("127.0.0.1", PORT))
    
    # while True:
        # send = input('Data: ')
        # csocket.send(send.encode())
        # data = csocket.recv(MAXLINE)
        # print(data)
        
        
        
        
    # csocket.close()
    
if __name__ == "__main__":
    main()
