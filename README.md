# server2threads
Projekt z Technologii Sieciowych (wariant 13) na PP.

Wykonany przez:
Aleksander Stęplewski i Łukasz Wylegała

Przesyłanie przez klientów liczby L, tworzenie przedziału (L1-L2, L1+L2), odsyłanie przedziału, przyjmowanie liczby od klienta i sprawdzanie wyniku z serwerem.

Przesyłanie systemem binarnym:
    Pole operacji: 6 bitów,
    Pole odpowiedzi: 3 bity,
    Pole identyfikatora sesji: 3 bity,
    Pole danych: 32 bity,
    Pole uzupełnienia: 4 bity,
    
Pola operacji:
    001001 - prośba o id sesji,
    000001 - przesłanie liczby L,
    000101 - wysłanie zgadywanej liczby,
    000110 - wysłanie zgadywanej liczby gdy jest ujemna,
    000111 - zakończenie połączenia,
    
Pola odpowiedzi:
    111 - wysłanie identyfikatora,
    001 - wysłanie dołu przedziału,
    011 - wysłanie dołu przedziału gdy jest ujemny,
    010 - wysłanie górnej granicy przedziału,
    101 - wysłanie potwierdzenia zgadnięcia,
    110 - wysłanie zaprzeczenia zgadnięcia,
    
Pole identyfikatora sesji:
    001 - id klienta 1,
    010 - id klienta 2,
    
Pole danych:
    liczba zapisana na 32 bitach,
    
Pole uzupełnienia:
    0000 - zawsze takie samo,



