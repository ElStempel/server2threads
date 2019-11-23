import random
import socket
import string
import queue
from threading import Thread
import array
import time
import Header

TCP_IP = '192.168.0.107'
TCP_PORT = 5005
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

lista = []
wyliczona = 0
uzyto = 0
L1 = 0
L2 = 0
dol = 0
gora = 0
bezwzg = 0


def wylicz():
    global uzyto
    global wyliczona
    global lista
    global L1
    global L2
    global dol
    global gora
    global bezwzg
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
        dol = L1 - L2
        if dol < 0:
            dol = abs(dol)
            bezwzg = 1
        gora = L1 + L2
        liczba = random.randrange(L1 - L2, L1 + L2)
        print("Wylosowana liczba: ")
        print(liczba)
        uzyto = 1
        wyliczona = liczba


licz = Thread(target=wylicz, args=())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))


def klient1(ip, port):
    global wyliczona
    global lista
    global L1
    global L2
    global dol
    global gora
    global bezwzg
    print('Klient 1 polaczony \n')
    id = 1
    req = conn.recv(BUFFER_SIZE)
    gib = Header.Header(0,0,0,0)
    gib.setHeader(req)
    conn.send(Header.Header(0, 9, id, 0).getHeader())
    #wysylanie id = 9

    while True:
        odebrana = conn.recv(BUFFER_SIZE)
        gib.setHeader(odebrana)
        op = gib.getOp()
        num = gib.getNumber()

        if(int(op) == 1):
            lista.append(int(num))
            licz.join()
            if bezwzg == 1:
                print("Wysylam: -" + str(dol))
                conn.send(Header.Header(0, 3, id, int(dol)).getHeader())
                # 3 = dol ujemny
            else:
                print("Wysylam: " + str(dol))
                conn.send(Header.Header(0, 1, id, int(dol)).getHeader())
                # wyslanie dolu = 1
            print("Wysylam: " + str(gora))
            conn.send(Header.Header(0, 2, id, int(gora)).getHeader())
            # wyslanie gory = 2
        if(int(op) == 5):
            print("Klient 1 zgaduje: ", num)
            if (int(wyliczona) == int(num)):
                print("Klient 1 zgadl")
                conn.send(Header.Header(0, 5, id, 0).getHeader())
                # 5 = zgadl
            else:
                print("Nie zgadnieto")
                conn.send(Header.Header(0, 6, id, 0).getHeader())
                # 6 = nie zgadl

        if (int(op) == 6):
            print("Klient 1 zgaduje: ", -num)
            if (int(wyliczona) == int(-num)):
                print("Klient 1 zgadl")
                conn.send(Header.Header(0, 5, id, 0).getHeader())
                # 5 = zgadl
            else:
                print("Nie zgadnieto")
                conn.send(Header.Header(0, 6, id, 0).getHeader())
                # 6 = nie zgadl


def klient2(ip, port):
    global wyliczona
    global lista
    global L1
    global L2
    global dol
    global gora
    global bezwzg
    print('Klient 2 polaczony\n')
    id = 2
    req = conn2.recv(BUFFER_SIZE)
    gib = Header.Header(0,0,0,0)
    gib.setHeader(req)
    conn2.send(Header.Header(0, 9, id, 0).getHeader())
    # wysylanie id = 9

    while True:
        odebrana = conn2.recv(BUFFER_SIZE)
        gib.setHeader(odebrana)
        op = gib.getOp()
        num = gib.getNumber()

        if (int(op) == 1):
            lista.append(int(num))
            licz.join()
            print("Wysylam: " + str(dol))
            conn2.send(Header.Header(0, 1, id, int(dol)).getHeader())
            # wyslanie dolu = 1
            print("Wysylam: " + str(gora))
            conn2.send(Header.Header(0, 2, id, int(gora)).getHeader())
            # wyslanie gory = 2
        if (int(op) == 5):
            print("Klient 2 zgaduje: ", num)
            if (int(wyliczona) == int(num)):
                print("Klient 2 zgadl")
                conn2.send(Header.Header(0, 5, id, 0).getHeader())
                # 5 = zgadl
            else:
                print("Nie zgadnieto")
                conn2.send(Header.Header(0, 6, id, 0).getHeader())
                # 6 = nie zgadl

        if (int(op) == 6):
            print("Klient 1 zgaduje: ", -num)
            if (int(wyliczona) == int(-num)):
                print("Klient 1 zgadl")
                conn2.send(Header.Header(0, 5, id, 0).getHeader())
                # 5 = zgadl
            else:
                print("Nie zgadnieto")
                conn2.send(Header.Header(0, 6, id, 0).getHeader())
                # 6 = nie zgadl


print("Serwer dziala")
while True:
    s.listen(1)
    (conn, (ip, port)) = s.accept()
    t1 = Thread(target=klient1, args=(ip, port))
    t1.start()

    s.listen(1)
    (conn2, (ip2, port2)) = s.accept()
    t2 = Thread(target=klient2, args=(ip2, port2))
    t2.start()
    licz.start()
    break

while True:
    time.sleep(1)

s.close()
