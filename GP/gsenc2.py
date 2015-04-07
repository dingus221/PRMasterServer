#6 procedures related to encoding in GP
#Sources: GSOpenSDK, aluigi's works
import base64
import hashlib

def gsPWDecHash(pwenc):
    md5 = hashlib.md5()
    md5.update(gsPWDecodeFunc0(pwenc))
    return md5.hexdigest()

def gsPWDecodeFunc0(pwenc):
    pwencx = base64.b64decode(pwenc)
    return gsPWDecodeFunc1(pwencx)

def gsPWDecodeFunc1(pwencx):
    num = 2037412711
    for i in xrange(0,len(pwencx)):
        d = 255
        if d != 0:
            num = gsPWDecodeFunc2(num)
            a = num % d
        else:
            a = 0
        pwencx = pwencx[:i] + chr(ord(pwencx[i]) ^ (a % 256) ) + pwencx[i+1:]       
    return pwencx

def gsPWDecodeFunc2(num):
    c = (num >> 16) & 65535
    a = num & 65535
    c *= 16807
    a *= 16807
    a += (c & 32767) << 16
    if a < 0:
        a &= 2147483647
        a += 1
    a += c >> 15
    if a < 0:
        a &= 2147483647
        a += 1
    return a

def PW_Hash_to_Resp(pwhash,unick,schal,cchal):
    md5 = hashlib.md5()
    md5.update(pwhash + (' '*48) + unick + cchal + schal + pwhash)
    return md5.hexdigest()

def PW_Hash_to_Proof(pwhash,unick,schal,cchal):
    md5 = hashlib.md5(pwhash + (' '*48) + unick + schal + cchal + pwhash)
    md5.update()
    return md5.hexdigest()
