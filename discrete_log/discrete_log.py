import numpy as np


P = 461733370363
MY_ID = 315129551


def BinarySearch(a, x):
    low = 0
    high = len(a) - 1
    while low <= high:
        mid = low + (high - low)//2
        if a[mid][1] == x:
            return mid
        elif a[mid][1] < x:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def sample_t(m, t):
    return np.random.randint(low=0, high=m, size=t, dtype=np.int64)


# -------------------------------------- SEC 1 --------------------------------------------
# we set t according to the birthday paradox calculations we saw in class
# so t should be at least sqrt(2^n) where n is number of bits of a number in Z_m
def section_1(m, x):
    a = sample_t(m=m, t=int(np.ceil(np.sqrt(m))))
    a_plus_x = np.sort((a + x) % m)
    for i in range(len(a)):
        # search a[i] in a_plus_x
        j = BinarySearch(x=a[i], a=a_plus_x)
        if j >= 0:
            return i, j
    return None

# -------------------------------------- SEC 2 --------------------------------------------
# suppose we can find a,b in G s.t g^a = g^b * X, where G is cyclic group of size m with generator g.
# from here: g^a = g^b * X ---> g^(a mod m) = g^(b mod m) * X ---> g^(a-b mod m) = x ---> log_g(x) = a-b mod m.
# so in order to calculate the discrete log of x with base g, we need to find a,b that holds the above.


# -------------------------------------- SEC 3 --------------------------------------------
# we want to find x in Z*_p s.t: 2^x = MY_ID % p. (meaning g=2)
# from section 2, its enough to find a pair (a,b) that holds: g^a = g^b * g^x.
# we can alter section 1 so we'll find g^a = g^b * MY_ID mod p (g^x = MY_ID mod p)!

def section_3(p, g, ID):
    a = [(e, pow(g, int(e), p)) for e in sample_t(m=p, t=int(np.ceil(np.sqrt(p))))]
    a_plus_x = sorted([(idx, (a[idx][1] * ID) % p) for idx in range(len(a))], key=lambda x: x[1])
    for i in range(len(a)):
        # search a[i] in a_plus_x
        j = BinarySearch(x=a[i][1], a=a_plus_x)
        if j >= 0:
            return a[i][0], a[a_plus_x[j][0]][0]
    return None


if __name__ == '__main__':
    res = None
    while res is None:
        res = section_3(p=P, ID=MY_ID, g=2)
    print((res[0] - res[1]) % P)
