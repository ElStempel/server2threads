import socket
import random
import Header


# Dane serwera
host = str(input("Wpisz IP serwera: "))
port = 5005
BUFFER_SIZE = 2000


# polaczenie ip i portu z socketem
tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpClientA.connect((host, port))


#funkcja losujaca
def losuj(dol, gora):
    losowa = random.randint(int(dol), int(gora))
    print("Losuje: " + str(losowa))
    return losowa


#dzialanie serwera
while True:
    tcpClientA.send(Header.Header(9, 0, 0, 0).getHeader())  # prośba o id

    while True:
        odebrana = tcpClientA.recv(BUFFER_SIZE)
        gib = Header.Header(0, 0, 0, 0)
        gib.setHeader(odebrana)
        ans = gib.getAns()
        num = gib.getNumber()
        id = gib.getSesID()


        # otrzymanie id
        if (int(ans) == 7):
            sesid = id
            print("\nID sesji to: ", sesid)
            # podawanie id = 7


        # wyslanie liczby L
        while True:
            MESSAGE = input("\nPodaj liczbe L wieksza niz 0: ")
            if MESSAGE.isnumeric() and int(MESSAGE) > 0:
                break
        # podawanie liczby = 1
        tcpClientA.send(Header.Header(1, 0, id, int(MESSAGE)).getHeader())


        # otrzymywanie granic przedzialu
        x = 2
        while (x > 0):
            odps = tcpClientA.recv(BUFFER_SIZE)
            gib.setHeader(odps)
            ans = gib.getAns()
            num = gib.getNumber()
            if (int(ans) == 1):
                dol = num
                print("\nDolna granica przedzialu: ", dol)
                x = x - 1

            if (int(ans) == 3):
                dol = -num
                print("\nDolna granica przedzialu: ", dol)
                x = x - 1

            if (int(ans) == 2):
                gora = num
                print("\nGorna granica przedzialu: ", gora)
                x = x - 1


        # losowanie i wysylanie liczby
        zle = []
        while True:
            while True: # sprawdzanie czy liczba sie nie powtarza
                losowa = losuj(dol, gora)
                if(losowa not in zle):
                    print("Pierwsze wystapienie")
                    break

            if (losowa < 0):
                bzlosowa = abs(losowa)
                print("Wysylam")
                tcpClientA.send(Header.Header(6, 0, id, bzlosowa).getHeader())
            else:
                print("Wysylam")
                tcpClientA.send(Header.Header(5, 0, id, losowa).getHeader())
                # 5 = zgadywanie
                # 6 = zgadywanie gdy ujemna


            # otrzymywanie odpowiedzi o zgadnieciu od serwera
            odpx = tcpClientA.recv(BUFFER_SIZE)
            gib.setHeader(odpx)
            odp = gib.getAns()

            if odp == 5:
                print('Zgadles')
                break
            elif odp == 6:
                zle.append(losowa)
                print('Nie zgadles')


        # zakonczenie i zamkniecie polaczenia
        print("Koniec gry")
        print("\n\nZamykam polaczenie\n\n")
        tcpClientA.send(Header.Header(7, 0, id, 0).getHeader())
        break
    break

tcpClientA.close()
