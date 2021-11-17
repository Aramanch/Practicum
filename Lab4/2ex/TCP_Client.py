import socket
import threading


import time

sock = socket.socket()
sock.setblocking(1)
sock.connect(('127.0.0.1', 9605))
message = ""
Fl = True


def Recieving():
    while True:
        server_message = sock.recv(1024).decode()
        print(server_message)


def Sending():
    while True:
        message = input()
        sock.send(message.encode())

        if message == "exit":
            global Fl
            Fl = False
            sock.close()
            break


t1 = threading.Thread(target=Recieving).start()
t2 = threading.Thread(target=Sending).start()

