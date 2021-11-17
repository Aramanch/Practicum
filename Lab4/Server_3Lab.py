import socket

with open("spisok.txt", "r") as file:
    users = [line.split() for line in file.readlines()]



sock = socket.socket()
sock.bind(('127.0.0.1', 9700))
sock.listen(1)
conn, addr = sock.accept()
Fl = False


try:
    for user in users:
        if user[0] == str(addr[0]):
            conn.send((f"Здравствуйте, {user[1]}\n").encode())
            Fl = True
            break
except:
    pass

if not(Fl):
    conn.send(("Здравствуйте!\n").encode())
    while True:
        conn.send(("Ваше имя: \n").encode())
        message = conn.recv(1024).decode()
        if message != "":
            users.append([addr[0], message])
            with open("spisok.txt", "w") as file:
                for line in users:
                    file.write(" ".join(line))
            conn.send((f"Ок, {message}\n").encode())
            break
        else:
            conn.send(("Ошибка\n").encode())


for user in users:
    if user[0] == str(addr[0]):
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
                conn.send(("Установка пароля.\n Введите пароль: ").encode())
                message = conn.recv(1024).decode()
                while True:
                    if message != "":
                        user.append(message)
                        with open("spisok.txt", "w") as file:
                            for line in users:
                                file.write(" ".join(line))
                        break
                    else:
                        conn.send(("Введите пароль: ").encode())






while True:
    message = conn.recv(1024).decode()
    print(message)
    conn.send(message.encode())
    conn.send(("\nВведите новое сообщение: ").encode())
    if message == "exit" or message == "":
        break
