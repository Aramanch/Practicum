#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

hostt = input('Введите нужный хост: ')

portt = int(input('Введите нужный порт: '))

password = 'user111'

sock = socket.socket()
sock.connect((hostt, portt))
mes = '-'


password = 'user111'


sock.send(mes.encode())

data = sock.recv(1024)

print(data.decode())

if data.decode() == 'Введите ваше имя и пароль':
    namee = input('Имя: ')
    passw = input('Пароль: ')
    f = open('addrs.txt', 'w')
    
    f.write(namee)
    f.write(str(sock))
    
    f.close()
    if passw == password:
        print('Пароль верный')
    else:
        print('Пароль неверный')
        message = 'exit'
        sock.send(message.encode())
        
        
while True:
        
    message = input("Введите сообщение:  ")


    sock.send(message.encode())

    data = sock.recv(1024)

    print(data.decode())

sock.close()








