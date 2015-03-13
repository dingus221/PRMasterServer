# Based on http://aluigi.altervista.org/papers.htm#peerchat
class GsPeerchat:
    def __init__(self, gamekey):
        chall=b"0" * 16
        self.i1 = 0
        self.i2 = 0
        self.crypt = bytearray(256)
        assert(len(chall) == 16)
        chall = bytearray(chall)
        gamekey = bytearray(gamekey)
        challenge = bytearray(16)
        for i in range(0, 16):
            challenge[i] = chall[i] ^ gamekey[i % len(gamekey)]
        for i in range(0, 256):
            self.crypt[i] = 255 - i
        tl = 0
        for i in range(0, 256):
            tl = (tl + self.crypt[i] + challenge[i % 16]) % 256
            self.crypt[tl], self.crypt[i] = self.crypt[i], self.crypt[tl]
    def call(self, data):
        data = bytearray(data)
        for i in range(0, len(data)):
            self.i1 = (self.i1 + 1) % 256
            self.i2 = (self.i2 + self.crypt[self.i1]) % 256
            self.crypt[self.i1], self.crypt[self.i2] = self.crypt[self.i2], self.crypt[self.i1]
            t = (self.crypt[self.i1] + self.crypt[self.i2]) % 256
            data[i] ^= self.crypt[t]
        return bytes(data)
