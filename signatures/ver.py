import sys
import hashlib

Nb = 256
NB = Nb // 8  # 32
ONE_TIME_SIG_LEN = NB * Nb  # 256*32
VK_LEN = NB * Nb * 2  # 256*32*2
SIG_LEN = (2 * VK_LEN + ONE_TIME_SIG_LEN) * Nb  # 256*(5*256*32)


def str_pop(l, n):
    return l[:n], l[n:]


def bits(x):
    """
     convert x to bits (array of 1's and 0's)!
    """
    bits = []
    for y in x:
        for i in range(8):
            y, b = divmod(y, 2)
            bits.append(b)
    return bits


def SHA(x):
    return hashlib.sha256(x).digest()


def init_vk(vk_bytes):
    """
    generate key vk: vk = [(vk_bytes[i:i+32], vk_bytes[i+32:i+64]) for i in range(0,vk_bytes,64)]
    """
    vk = []
    while vk_bytes:
        k0, vk_bytes = str_pop(vk_bytes, NB)
        k1, vk_bytes = str_pop(vk_bytes, NB)
        vk.append((k0, k1))
    return vk


def one_time_ver(vk, msg, sig):
    """
    vk is list of tuples that correspond to each bit of hash(msg).
    in order to pass:
    vk[i][hash(msg)[i]] == hash(sig[i:i+NB])
    """
    msg = SHA(msg)
    for b, keys in zip(bits(msg), vk):
        # keys is tuple of 2!
        key, sig = str_pop(sig, NB)
        # the first key is not in our control! we need to break SHA???
        if keys[b] != SHA(key):
            return False
    return True


def ver(vk, msg, sig):
    if len(sig) != SIG_LEN:
        return False
    msg = SHA(msg)  # compute the hash of the message
    for b in bits(msg):
        vk0_bytes, sig = str_pop(sig, VK_LEN)  # vk0_bytes = signature[0:VK_LEN]
        vk1_bytes, sig = str_pop(sig, VK_LEN)  # vk1_bytes = signature[VK_LEN:2*VK_LEN]
        vk_sig, sig = str_pop(sig, ONE_TIME_SIG_LEN)  # vk_sig = signature[2*VK_LEN:2*VK_LEN + ONE_TIME_SIG_LEN]
        # in order to pass:
        # vk[i][hash(vk0_bytes + vk1_bytes)[i]] == hash(vk_sig[i:i+NB])
        if not one_time_ver(vk, vk0_bytes + vk1_bytes, vk_sig):
            return False
        vk = init_vk((vk0_bytes, vk1_bytes)[b])  # determine by the current bit of the message
        # the next vk is pairs from vk0_bytes or vk1_bytes depends on b (bit of hash(msg))
    return True


def main():
    try:
        (msg, vk_file, sig_file) = sys.argv[1:]
    except ValueError:
        print("Usage: ver.py message key_file signature_file")
        return

    vk = init_vk(open(vk_file, 'rb').read())
    sig = open(sig_file, 'rb').read()
    print(ver(vk, msg.encode(), sig))


# main()