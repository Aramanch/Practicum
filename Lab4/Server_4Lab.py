import socket
import sys
import threading
import logging


logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', filename="procss.log", level=logging.DEBUG)

try:
    file = open("spisok.txt", "r")
    users = [line[:-1].split(";") for line in file.readlines()]
    file.close()
except FileNotFoundError:
    file = open("spisok.txt", "w")
    file.close()



sock = socket.socket()
sock.bind(('127.0.0.1', 9800))
sock.listen(1)


Users = []
Pause = False

def ThreadFunc():
    global Users
    global Pause
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
            conn.send(("Ваше имя:\n").encode())
            message = conn.recv(1024).decode()
            if message != "":
                name = message
                users.append([str(addr), name])
                with open("spisok.txt", "w") as file:
                    for line in users:
                        file.write(";".join(line))
                        file.write("\n")
                conn.send((f"Ок, {name}\n").encode())
                break
            else:
                conn.send(("Ошибка\n").encode())

    
    for user in users:
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
                        ("Установка пароля.\n Введите пароль: ").encode())
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
        if not Pause:
            message = conn.recv(1024).decode()
            print(f"{name}: {message}")
            for conn_from_list in Users:
                if conn_from_list != conn:
                    try:
                        conn_from_list.send((f"{name}: {message}").encode())
                    except:
                        pass
            logging.info(f"{name}: {message}")
            if message == "exit":
                break

def ThreadServ():
    global Pause
    while True:
        comm = input()
        if comm == "shutdown":
            sys.exit()
        elif comm == "pause":
            Pause = not Pause
        elif comm == "log":
            with open("procss.log", "r") as file:
                print("Содержимое лог-файла:")
                for line in file.readlines():
                    print(line, end="")
        elif comm == "logclear":
            with open("procss.log", "w") as file:
                print("Содержимое лог-файла очищено")
        elif comm == "clearident":
            with open("spisok.txt", "w") as file:
                print("Содержимое файла-идентификации очищено")
        else:
            print("Неизвестная команда")





NewThread = True
server_thread = threading.Thread(target=ThreadServ, name="serv")
server_thread.start()

while True:
    if NewThread:
        threading.Thread(target=ThreadFunc).start()
        NewThread = False
