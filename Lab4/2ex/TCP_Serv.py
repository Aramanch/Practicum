import socket
import threading

sock = socket.socket()
sock.bind(('127.0.0.1', 9605))
sock.listen(1)


def Thread_Function():
	client_socket, addr = sock.accept()
	global Thread_new
	Thread_new = True

	while True:
		message = client_socket.recv(1024).decode()
		print(message)
		client_socket.send(message.encode().upper())
		if message == "exit":
			sock.close()
			break

Thread_new = True


while True:
	if Thread_new:
		threading.Thread(target=Thread_Function).start()
		Thread_new = False



