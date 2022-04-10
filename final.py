import random
from decimal import Decimal

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
    with open("shares.txt", "w", encoding='utf8') as fout:
        for i in shares:
            fout.write(str(i) + "\n")
    return shares


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def encrypt():
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

    num = int(input("Enter the total number of shares you wish to make : "))
    threshold = int(input("Enter the threshold number of shares required to reconstruct the key : "))
    shares = generate_shares(num, threshold, d)
    print(f"\nThe shares are as follows : \n{shares}\nPlease store them securely.\n")

    with open("input.txt", "r", encoding='utf8') as fin:
        message = fin.read()
    print(f"The message in the file is :\n{message}")
    msg = [ord(i) for i in message]
    enc = [pow(i, e, n) for i in msg]
    print("\nThe encrypted message is :")
    with open("encrypted.txt", "w", encoding='utf8') as fout:
        for i in enc:
            fout.write(chr(i))
            print(chr(i), end="")


def decrypt():
    p = 13
    q = 31
    r = 157
    s = 173
    n = p * q * r
    totient = (p - 1) * (q - 1) * (r - 1)*(s-1)
    e = d = -1
    ct = 0
    t = int(input('Enter the number of shares you have :'))
    shares = []
    for i in range(t):
        ind = int(input("Enter the index number of the share : "))
        val = int(input("Enter the value of the share : "))
        shares.append((ind, val))
    # print(reconstruct_secret(shares))
    d = reconstruct_secret(shares)

    with open("encrypted.txt", "r", encoding='utf8') as fin:
        encmsg = fin.read()
    print(f"The encrypted message is :\n{encmsg}")
    enc = [ord(i) for i in encmsg]
    try:
        dec = [pow(i, d, n) for i in enc]
        print("\nThe decrypted message is :")
        with open("decrypted.txt", "w", encoding='utf8') as fout:
            for i in dec:
                fout.write(chr(i))
                print(chr(i), end="")
    except:
        print("Minimum shares not reached")


choice = int(input("MENU\n1.Encryption\n2.Decryption\n\nEnter your choice : "))
if choice == 1:
    encrypt()
elif choice == 2:
    decrypt()
