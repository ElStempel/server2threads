import random
import socket
import string
import queue
from threading import Thread
import array
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response


lista = []
wyliczona = 0
uzyto = 0
L1 = 0
L2 = 0


def wylicz():
    global uzyto
    global wyliczona
    global lista
    global L1
    global L2
    while True:
        if (uzyto == 1):
            uzyto = 1
            break
        uzyto = 1
        while True:
            if (len(lista) == 2):
                break
        L2 = lista.pop()
        L1 = lista.pop()
        liczba = random.randrange(L1 - L2, L1 + L2)
        print("Wylosowana liczba: ")
        print(liczba)
        uzyto = 1
        wyliczona = liczba


licz = Thread(target=wylicz, args=())


def sessionID():
    id = str(random.randrange(0, 7))
    print("ID sesji to: ")
    print(id)
    return id


def wyslijID(id):
    s.send(bytes(id, "utf-8"))


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))


def klient1(ip, port):
    global wyliczona
    global lista
    global L1
    global L2
    print('Starting thread1\n')
    id = sessionID()
    odebrana = conn.recv(BUFFER_SIZE)
    print("Otrzymano: ", odebrana.decode())
    lista.append(int(odebrana.decode()))
    licz.start()
    licz.join()


def klient2(ip, port):
    global wyliczona
    global lista
    global L1
    global L2
    print('Starting thread2\n')
    id = sessionID()
    odebrana2 = conn.recv(BUFFER_SIZE)
    print("Otrzymano: ", odebrana2.decode())
    lista.append(int(odebrana2.decode()))
    licz.start()
    licz.join()


while True:
    s.listen(1)
    (conn, (ip, port)) = s.accept()
    t1 = Thread(target=klient1, args=(ip, port))
    t1.start()

    s.listen(1)
    (conn, (ip2, port2)) = s.accept()
    t2 = Thread(target=klient2, args=(ip2, port2))
    t2.start()

    break

while True:
    time.wait(1)

s.close()
