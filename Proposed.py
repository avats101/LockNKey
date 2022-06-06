import random
from decimal import Decimal
import tracemalloc
import datetime
import os
FIELD_SIZE = 10 ** 3

def reconstruct_secret(shares):
    sums = 0
    for j, share_j in enumerate(shares):
        xj, yj = share_j
        prod = Decimal(1)
        for i, share_i in enumerate(shares):
            xi, _ = share_i
            if i != j:
                prod *= Decimal(Decimal(xi) / (xi - xj))
        prod *= yj
        sums += Decimal(prod)
    return int(round(Decimal(sums), 0))


def polynom(x, coefficients):
    point = 0
    for coefficient_index, coefficient_value in enumerate(coefficients[::-1]):
        point += x ** coefficient_index * coefficient_value
    return point


def coeff(t, secret):
    coeff = [random.randrange(0, FIELD_SIZE) for _ in range(t - 1)]
    coeff.append(secret)
    return coeff


def generate_shares(n, m, secret):
    coefficients = coeff(m, secret)
    shares = []
    for i in range(1, n + 1):
        x = i
        shares.append((x, polynom(x, coefficients)))
    return shares


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def encrypt():

    # tracemalloc.start()
    num = int(input("Enter the total number of shares you wish to make : "))
    threshold = int(input("Enter the threshold number of shares required to reconstruct the key : "))
    dstime=datetime.datetime.now()
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
    shares = generate_shares(num, threshold, d)
    print(f"\nThe shares are as follows : \n{shares}\nPlease store them securely.\n")
    with open("shares.txt", "w", encoding='utf8') as fout:
        for i in shares:
            fout.write(str(i))
            fout.write("\n")
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
    detime=datetime.datetime.now()
    print("Time taken for Encryption",detime-dstime)
    # snapshot = tracemalloc.take_snapshot()
    # for stat in snapshot.statistics("filename"):
    #     print(stat) 
    # tracemalloc.stop()


def decrypt():
   # tracemalloc.1start()
    stime=datetime.datetime.now()
    p = 13
    q = 31
    r = 157
    n = p * q * r
    with open("shares.txt", "r", encoding='utf8') as fin:
        shares = fin.read()
    shares = shares.split('\n')[:-1]
    for i in range(len(shares)):
        shares[i] = shares[i][1:-1]
        shares[i] = tuple(map(int, shares[i].split(',')))
    d = reconstruct_secret(shares)
    with open("encrypted.txt", "r", encoding='utf8') as fin:
        encmsg = fin.read()
    #print(f"The encrypted message is :\n{encmsg}")
    enc = [ord(i) for i in encmsg]
    dec = [pow(i, d, n) for i in enc]
    #print("\nThe decrypted message is :")
    with open("decrypted.txt", "w", encoding='utf8') as fout:
        for i in dec:
            fout.write(chr(i))
            #print(chr(i), end="")
    etime=datetime.datetime.now()
    print("Time taken for Decryption",etime-stime)
    # snapshot = tracemalloc.take_snapshot()
    # for stat in snapshot.statistics("filename"):
    #     print(stat) 
    # tracemalloc.stop()


choice = int(input("MENU\n1.Encryption\n2.Decryption\n\nEnter your choice : "))
if choice == 1:
    encrypt()
elif choice == 2:
    decrypt()