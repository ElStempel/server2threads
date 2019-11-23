import random
import socket
import string
import queue
from threading import Thread
import array
import time
import Header

TCP_IP = 'localhost'
TCP_PORT = 5005
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

lista = []
wyliczona = 0
uzyto = 0
L1 = 0
L2 = 0
dol = 0
gora = 0


def setHeader(rec):
    recTab = []

    data = int.from_bytes(rec, 'big')
    bitShift = ((2**4), (2**36), (2**39), (2**42), (2**48))
    tmp = data % bitShift[1]
    number = int(tmp/bitShift[0])

    tmp = data % bitShift[2]
    id = int(tmp/bitShift[1])

    tmp = data % bitShift[3]
    ans = int(tmp/bitShift[2])

    print("Liczba: ", number)
    print("Odp: ", ans)
    print("ID: ", id)

    recTab.append(ans)
    recTab.append(id)
    recTab.append(number)

    return recTab




def wylicz():
    global uzyto
    global wyliczona
    global lista
    global L1
    global L2
    global dol
    global gora
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
        gora = L1 + L2
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
    conn.send(bytes(id, "utf-8"))


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
    print('Starting thread1\n')
    id = sessionID()
    gib = conn.recv(BUFFER_SIZE)
    gib = setHeader(gib)
    conn.send(Header.Header(0, 9, 1, 0).getHeader())
    #wysylanie id = 9
    odebrana = conn.recv(BUFFER_SIZE)
    recTab = setHeader(odebrana)
    #conn.send(odebrana)
    lista.append(int(recTab[2]))
    licz.start()
    licz.join()
    time.sleep(5)
    print("Wysyłam: " + str(dol))
    conn.send(Header.Header(0, 1, 1, dol).getHeader())
    #wyslanie dolu = 1
    print("Wysyłam: " + str(gora))
    conn.send(Header.Header(0, 2, 1, gora).getHeader())
    #wyslanie gory = 2
    while True:
        c1los = conn.recv(BUFFER_SIZE)
        print("Klient wysyla: ", c1los.decode())
        if(int(wyliczona) == int(c1los)):
            print("Klient zgadl")
            conn.send(bytes('tak', 'utf-8'))
            break
        else:
            print("Nie zgadnieto")
            conn.send(bytes('nie','utf-8'))



def klient2(ip, port):
    global wyliczona
    global lista
    global L1
    global L2
    global dol
    global gora
    print('Starting thread2\n')
    id = sessionID()
    gib = conn2.recv(BUFFER_SIZE)
    gib = setHeader(gib)
    conn2.send(Header.Header(0, 9, 2, 0).getHeader())
    # wysylanie id = 9
    odebrana = conn.recv(BUFFER_SIZE)
    recTab = setHeader(odebrana)
    # conn.send(odebrana)
    lista.append(int(recTab[2]))
    licz.start()
    licz.join()
    time.sleep(5)
    print("Wysyłam: " + str(dol))
    conn2.send(Header.Header(0, 1, 2, dol).getHeader())
    # wyslanie dolu = 1
    print("Wysyłam: " + str(gora))
    conn2.send(Header.Header(0, 2, 2, gora).getHeader())
    # wyslanie gory = 2
    while True:
        c2los = conn2.recv(BUFFER_SIZE)
        print("Klient wysyla: ", c2los.decode())
        if(int(wyliczona) == int(c2los)):
            print("Klient zgadl")
            conn2.send(bytes('tak', 'utf-8'))
            break
        else:
            print("Nie zgadnieto")
            conn2.send(bytes('nie','utf-8'))


while True:
    s.listen(1)
    (conn, (ip, port)) = s.accept()
    t1 = Thread(target=klient1, args=(ip, port))
    t1.start()

    s.listen(1)
    (conn2, (ip2, port2)) = s.accept()
    t2 = Thread(target=klient2, args=(ip2, port2))
    t2.start()

    break

while True:
    time.sleep(1)

s.close()
