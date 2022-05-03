from math import log2, floor
import gmpy2


def gcd(a, b):
    if b > a:
        c = b
        b = a
        a = c
    r = (a % b)
    while r > 0:
        a = b
        b = r
        r = (a % b)
    return b



def accuracy_test_processing(n, start, end):
    is_there_negative = False
    tests_completed = 1
    a_i = [gmpy2.mpz(start)]
    flag = True
    for i in range(gmpy2.mpz(start), gmpy2.mpz(end), 1):
        for num in a_i:
            cur_gcd = gcd(num, i)
            if cur_gcd != 1:
                flag = False
                break
            flag = True
        if flag:
            a_i.append(i)
            result, tmp = leman_test_step(n, i)
            if not result:
                return False, False
            if tmp:
                is_there_negative = True
            chance = 1 - pow(0.5, tests_completed)
            tests_completed += 1
            if chance > 0.999999:
                return True, is_there_negative
    return True, is_there_negative


def leman_test_step(n, a):  # a - randomly generated number
    t = gmpy2.powmod(a, (n-1)//2, n)
    if t == 1:
        return True, False
    if t == n-1:
        return True, True
    return False, False


Primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89,
          97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191,
          193, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307,
          311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421,
          431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547,
          557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659,
          661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797,
          809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929,
          937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049,
          1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171,
          1181, 1187, 1193, 1201, 1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283, 1289, 1291,
          1297, 1301, 1303, 1307, 1319, 1321, 1327, 1361, 1367, 1373, 1381, 1399, 1409, 1423, 1427, 1429, 1433,
          1439, 1447, 1451, 1453, 1459, 1471, 1481, 1483, 1487, 1489, 1493, 1499, 1511, 1523, 1531, 1543, 1549,
          1553, 1559, 1567, 1571, 1579, 1583, 1597, 1601, 1607, 1609, 1613, 1619, 1621, 1627, 1637, 1657, 1663,
          1667, 1669, 1693, 1697, 1699, 1709, 1721, 1723, 1733, 1741, 1747, 1753, 1759, 1777, 1783, 1787, 1789,
          1801, 1811, 1823, 1831, 1847, 1861, 1867, 1871, 1873, 1877, 1879, 1889, 1901, 1907, 1913, 1931, 1933,
          1949, 1951, 1973, 1979, 1987, 1993, 1997, 1999]


def fast_pow(a, n):  # a^x = 1 (mod n)
    bin_x = []
    x = n - 1
    while x >= 1:
        bin_x.append(x % 2)
        x = int(floor(x//2))
    size = floor(log2(n-1)) + 1
    bases = [a]
    for j in range(1, size, 1):
        tmp = (bases[j-1]*bases[j-1]) % n
        bases.append(tmp)
    func_res = 1
    for k in range(0, len(bin_x), 1):
        func_res *= (bases[k]**bin_x[k])
        func_res = func_res % n
    return func_res


if __name__ == '__main__':
    number_of_bits_max = int(input("Input number of bits: "))
    while number_of_bits_max < 1:
        print("Length bits of number must be positive integer value.")
        number_of_bits_max = int(input("Length : "))

    # Task 1
    # generate random bits for p with LFSRs from lab2
    # mpz_random(random_state, n) returns a uniformly distributed random integer between 0 and n-1.
    # The parameter random_state must be created by random_state() first.
    rs = gmpy2.random_state(hash(gmpy2.random_state()))
    P = gmpy2.mpz_random(rs, pow(2, number_of_bits_max) - 1)
    print(P)
    help = gmpy2.mpz(2**(number_of_bits_max-1) + 1)
    P = P | help
    # P = 2305843009213693951
    # 162259276829213363391578010288124

    res = False
    while not res:
        # Task 3
        # checking simple with small primes
        delim = 1
        for prime in Primes:
            if P % prime == 0:
                delim = prime
                break
        begin = floor(pow(P, 0.5))
        if gmpy2.powmod(P, 1, 2) == 0:
            res = False
        else:
            res, is_there_neg = accuracy_test_processing(P, begin, P)
            if res and is_there_neg:
                print(f"Leman: {P} is prime")
            else:
                print(f"Leman: {P} is not prime or probability wrong")
                print(f"{P}: {delim} * {int(P // delim)}")
        P += 1
