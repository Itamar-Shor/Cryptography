import ver
import secrets

MY_ID = '315129551'.encode() # 0

# signatures
a_sig_file = r'C:\Users\ItamarS\Desktop\חשמל מדעי המחשב\שנה ד\קריפטוגרפיה\hw7\a.sig'
with open(a_sig_file, 'rb') as fd:
    a_sig = fd.read()
b_sig_file = r'C:\Users\ItamarS\Desktop\חשמל מדעי המחשב\שנה ד\קריפטוגרפיה\hw7\b.sig'
with open(b_sig_file, 'rb') as fd:
    b_sig = fd.read()
c_sig_file = r'C:\Users\ItamarS\Desktop\חשמל מדעי המחשב\שנה ד\קריפטוגרפיה\hw7\c.sig'
with open(c_sig_file, 'rb') as fd:
    c_sig = fd.read()
d_sig_file = r'C:\Users\ItamarS\Desktop\חשמל מדעי המחשב\שנה ד\קריפטוגרפיה\hw7\d.sig'
with open(d_sig_file, 'rb') as fd:
    d_sig = fd.read()
e_sig_file = r'C:\Users\ItamarS\Desktop\חשמל מדעי המחשב\שנה ד\קריפטוגרפיה\hw7\e.sig'
with open(e_sig_file, 'rb') as fd:
    e_sig = fd.read()

# verification key
vk2_file = r'C:\Users\ItamarS\Desktop\חשמל מדעי המחשב\שנה ד\קריפטוגרפיה\hw7\vk2'
with open(vk2_file, 'rb') as fd:
    vk2 = fd.read()

VK2_32B_CHUNKS = [vk2[idx:idx + 32] for idx in range(0, len(vk2), 32)]


# all of the message was signed by the same sk2! so the first vk_sig contains chunks of sk2.
def extract_sk():
    offset = ver.VK_LEN*2
    SK_32B_CHUNKS = [bytes() for i in range(ver.VK_LEN//32)]
    curr_byte_idx = 0

    for idx in range(offset, offset + ver.ONE_TIME_SIG_LEN, 32):
        for sig in [a_sig, b_sig, c_sig, d_sig, e_sig]:
            msg_idx = 0 if ver.SHA(sig[idx:idx+32]) == VK2_32B_CHUNKS[curr_byte_idx] else 1
            SK_32B_CHUNKS[msg_idx+curr_byte_idx] = sig[idx:idx+32]
        curr_byte_idx += 2

    cnt = 0
    missing = []
    for chunk in SK_32B_CHUNKS:
        if len(chunk) == 0:
            missing.append(cnt)
        cnt += 1
    return SK_32B_CHUNKS, missing

# TODO: need to generate random bytes that would force us not to peek the holes!
sk2_chunks, missing_chunks = extract_sk()


def generate_key_pair_and_dummy(missing, order=0):
    sk = secrets.token_bytes(ver.VK_LEN)
    vk_list = [ver.SHA(sk[idx:idx + 32]) for idx in range(0, len(sk), 32)]
    vk = bytes()
    for chunk in vk_list:
        vk += chunk
    dummy = secrets.token_bytes(ver.VK_LEN)
    bits = ver.bits(ver.SHA(vk+dummy)) if order == 0 else ver.bits(ver.SHA(dummy+vk))
    flag = True
    while flag:
        flag = False
        for idx in missing:
            if bits[idx//2] == (idx % 2):
                print(idx//2, idx)
                flag = True
                sk = secrets.token_bytes(ver.VK_LEN)
                vk_list = [ver.SHA(sk[idx:idx + 32]) for idx in range(0, len(sk), 32)]
                vk = bytes()
                for chunk in vk_list:
                    vk += chunk
                dummy = secrets.token_bytes(ver.VK_LEN)
                bits = ver.bits(ver.SHA(vk + dummy)) if order == 0 else ver.bits(ver.SHA(dummy + vk))
                break

    return sk, vk, dummy


def sign2(msg, sk_chunks, missing):
    sk, vk, dummy = generate_key_pair_and_dummy(missing=missing_chunks, order=0)
    SK_32B_CHUNKS = sk_chunks
    msg = ver.SHA(msg)
    signature = bytes()
    for b in ver.bits(msg):
        one_time_ver_msg = vk + dummy if b == 0 else dummy + vk
        one_time_ver_msg_sha = ver.SHA(one_time_ver_msg)
        one_time_ver_sig = bytes()
        byte_idx = 0
        for one_time_ver_msg_bit in ver.bits(one_time_ver_msg_sha):
            one_time_ver_sig += SK_32B_CHUNKS[byte_idx+one_time_ver_msg_bit]
            byte_idx += 2
        signature += one_time_ver_msg + one_time_ver_sig
        SK_32B_CHUNKS = [sk[idx:idx + 32] for idx in range(0, len(sk), 32)]
    return signature


#id_sign = sign2(MY_ID, sk2_chunks, missing_chunks)
#print(ver.ver(vk=ver.init_vk(vk2), msg=MY_ID, sig=id_sign))

#with open(r'C:\Users\ItamarS\Desktop\חשמל מדעי המחשב\שנה ד\קריפטוגרפיה\hw7\{}.sig'.format(MY_ID), 'wb') as fd:
#    fd.write(id_sign)

with open(r'C:\Users\ItamarS\Desktop\חשמל מדעי המחשב\שנה ד\קריפטוגרפיה\hw7\315129551.sig', 'rb') as fd:
    print(ver.ver(vk=ver.init_vk(vk2), msg='315129551'.encode(), sig=fd.read()))