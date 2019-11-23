import array
import math


class Header:
    def __init__(self, op, ans, sesID, number):
        self.all = []

        self.all.append(op)  # all[0]; 6 bits
        self.all.append(ans)  # all[1]; 3 bits
        self.all.append(sesID)  # all[2]; 3 bits
        self.all.append(number)  # all[3]; all[3] bytes

    def getHeader(self):
        arrayBH = bytearray(6)
        arrayBH[0] += self.all[0]
        arrayBH[0] <<= 2
        arrayBH[0] += ((self.all[1] & 6) >> 1)

        arrayBH[1] += self.all[1] & 1
        arrayBH[1] <<= 3
        arrayBH[1] += self.all[2]
        arrayBH[1] <<= 4
        arrayBH[1] += ((self.all[3] & 4026531840) >> 28)

        tmpINT = (self.all[3] << 4)
        arrayBH[2] += ((tmpINT & 0xF000) >> 24)
        arrayBH[3] += ((tmpINT & 0xF00) >> 16)
        arrayBH[4] += ((tmpINT & 0xF0) >> 8)
        arrayBH[5] += tmpINT
        return arrayBH