import tracemalloc
import datetime
import os
tracemalloc.start()
def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)
# stime=datetime.datetime.now()
p = 13
q = 31
r = 157
s = 173
n = p * q * r
totient = (p - 1) * (q - 1) * (r - 1)*(s-1)
e = d = -1
ct = 0
for i in range(2, totient):
    if ct == 1:
        break
    if gcd(i, totient) == 1:
        e = i
        ct += 1
ed = 1
while True:
    ed = ed + totient
    if ed % e == 0:
        d = int(ed / e)
        break


    with open("input.txt", "r", encoding='utf8') as fin:
        message = fin.read()
    #print(f"The message in the file is :\n{message}")
    msg = [ord(i) for i in message]
    enc = [pow(i, e, n) for i in msg]
    #print("\nThe encrypted message is :")
    with open("encrypted.txt", "w", encoding='utf8') as fout:
        for i in enc:
            fout.write(chr(i))
            #print(chr(i), end="")
# etime=datetime.datetime.now()
# print("Time taken for Encryption",etime-stime)
snapshot = tracemalloc.take_snapshot()
for stat in snapshot.statistics("filename"):
    print(stat) 
tracemalloc.stop()