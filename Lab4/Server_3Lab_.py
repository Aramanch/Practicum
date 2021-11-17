import socket
import threading
import logging


logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', filename="log.txt", level=logging.DEBUG)

try:
    file = open("users.txt", "r")
    users = [line[:-1].split(";") for line in file.readlines()]
    file.close()
except FileNotFoundError:
    file = open("users.txt", "w")
    file.close()



sock = socket.socket()
sock.bind(('127.0.0.1', 9700))
sock.listen(1)


Users = []

def ThreadFunc():
    global Users
    conn, addr = sock.accept()
    Users.append(conn)
    print(addr)
    global NewThread
    NewThread = True
    Ident = False

    
    try:
        for user in users:
            if user[0] == str(addr):
                name = user[1]
                conn.send((f"Здравствуйте, {name}\n").encode())
                Ident = True
                break
    except:
        pass

    if not(Ident):
        conn.send(("Здравствуйте!\n").encode())
        while True:
            conn.send(("Ваше имя: \n").encode())
            message = conn.recv(1024).decode()
            if message != "":
                name = message
                Users.append([str(addr), name])
                with open("spisok.txt", "w") as file:
                    for line in users:
                        file.write(";".join(line))
                        file.write("\n")
                conn.send((f"Ок,{name}\n").encode())
                break
            else:
                conn.send(("Ошибка\n").encode())

   
    for user in Users:
        print(user)
        if user[0] == str(addr):
            while True:
                try:
                    if user[2] != "":
                        conn.send(("Введите пароль: ").encode())
                        message = conn.recv(1024).decode()
                        if message == user[2]:
                            conn.send(("Вход выполнен\n Введите новое сообщение: ").encode())
                            break
                        else:
                            conn.send(("Неверный пароль\n").encode())
                except:
                    conn.send(
                        ("Установка пароля\n Введите пароль: ").encode())
                    message = conn.recv(1024).decode()
                    while True:
                        if message != "":
                            user.append(message)
                            with open("spisok.txt", "w") as file:
                                for line in users:
                                    file.write(";".join(line))
                                    file.write("\n")
                            break
                        else:
                            conn.send(("Введите пароль: ").encode())
                    break

    while True:
        message = conn.recv(1024).decode()
        print(f"{name}: {message}")
        print(Users)
        for conn_from_list in Users:
            if conn_from_list != conn:
                try:
                    conn_from_list.send((f"{name}: {message}").encode())
                except:
                    pass
        logging.info(f"{name}: {message}")
       conn.send(message.encode())
        if message == "exit":
            break




NewThread = True


while True:
    if NewThread:
        threading.Thread(target=ThreadFunc).start()
        NewThread = False
