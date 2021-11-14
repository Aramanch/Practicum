import socket
import logging

sock = socket.socket()

try:
    try:
        portt = int(input('Введите порт для сервера: '))

        sock.bind(('', portt))

        sock.listen(2)
        
        logging.basicConfig(filename='/Users/Aram/Desktop/procc.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        logging.info(f'{portt} has been connected')
        
        
    except OSError:
        portt = portt + 15
        sock.bind(('', portt))

        sock.listen(2)
        
        logging.basicConfig(filename='/Users/Aram/Desktop/procc.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        logging.info(f'{portt} has been connected')

    addrs = []

    message = ''
    while message != 'exit':
        conn, addr = sock.accept()
        
        if addr[0] in addrs:
            conn.send('Твоё лицо мне знакомо, братан!'.encode())
        else:
            conn.send('Введите ваше имя и пароль'.encode())
            
            addrs.append(addr[0])
        
            f = open('addrs.txt', 'w')
            
            f.write(addr[0])
            
            f.close()
        
        

        message = ''

        while True:

            data = conn.recv(1024)
            if not data:
                break
            message = data.decode()
            conn.send(data.upper())
            print(message)
        
        logging.basicConfig(filename='/Users/Aram/Desktop/procc.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        logging.info(f'{addr} has wroten')
        
        
        
    conn.close()


except OSError:

    logging.basicConfig(filename='/Users/Aram/Desktop/procc.log',level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

    logging.error('Address already in use')
