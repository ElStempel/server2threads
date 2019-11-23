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

        tmpINT = (self.all[3]<<4)
        arrayBH[2] += ((tmpINT & 0xFF000000) >> 24)
        arrayBH[3] += ((tmpINT & 0xFF0000) >> 16)
        arrayBH[4] += ((tmpINT & 0xFF00) >> 8)
        arrayBH[5] += (tmpINT & 0xF0)
        return arrayBH

    def setHeader(self, rec):
        data = int.from_bytes(rec, 'big')
        bitShift = ((2 ** 4), (2 ** 36), (2 ** 39), (2 ** 42), (2 ** 48))

        # operation
        tmp = data % bitShift[4]
        op = int(tmp/bitShift[3])
        # answer
        tmp = data % bitShift[3]
        ans = int(tmp / bitShift[2])
        # id
        tmp = data % bitShift[2]
        id = int(tmp / bitShift[1])
        # number
        tmp = data % bitShift[1]
        number = int(tmp / bitShift[0])

        self.all[0] = op
        self.all[1] = ans
        self.all[2] = id
        self.all[3] = number


    def getOp(self):
        return self.all[0]

    def getAns(self):
        return self.all[1]

    def getSesID(self):
        return self.all[2]

    def getNumber(self):
        return self.all[3]