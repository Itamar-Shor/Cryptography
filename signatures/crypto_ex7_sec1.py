import ver
import secrets

vk1_file = r'C:\Users\ItamarS\Desktop\חשמל מדעי המחשב\שנה ד\קריפטוגרפיה\hw7\vk1'
sk1_file = r'C:\Users\ItamarS\Desktop\חשמל מדעי המחשב\שנה ד\קריפטוגרפיה\hw7\sk1'
with open(vk1_file, 'rb') as fd:
    vk1 = fd.read()
with open(sk1_file, 'rb') as fd:
    sk1 = fd.read()

MY_FIRST_NAME = 'Itamar'
MY_LAST_NAME = 'Shor'


def sample_key_pair():
    sk = secrets.token_bytes(ver.VK_LEN)
    vk_list = [ver.SHA(sk[idx:idx+32]) for idx in range(0, len(sk), 32)]
    vk = bytes()
    for chunk in vk_list:
        vk += chunk
    return sk, vk


def update_key_state(sk):
    return [sk[idx:idx + 32] for idx in range(0, len(sk), 32)]


def sign(msg, sk):
    SK_32B_CHUNKS = update_key_state(sk)
    msg = ver.SHA(msg)
    signature = bytes()
    for b in ver.bits(msg):
        # sample new key pair at every round! this ensure the security
        next_sk, next_vk = sample_key_pair()
        random_bytes = secrets.token_bytes(ver.VK_LEN)
        one_time_ver_msg = next_vk + random_bytes if b == 0 else random_bytes + next_vk
        one_time_ver_msg_sha = ver.SHA(one_time_ver_msg)
        one_time_ver_sig = bytes()
        byte_idx = 0
        for one_time_ver_msg_bit in ver.bits(one_time_ver_msg_sha):
            one_time_ver_sig += SK_32B_CHUNKS[byte_idx+one_time_ver_msg_bit]
            byte_idx += 2
        signature += one_time_ver_msg + one_time_ver_sig
        SK_32B_CHUNKS = update_key_state(next_sk)
    return signature


if __name__ == '__main__':
    first_name_sig = sign(MY_FIRST_NAME.encode(), sk1)
    last_name_sig = sign(MY_LAST_NAME.encode(), sk1)

    with open(r'C:\Users\ItamarS\Desktop\חשמל מדעי המחשב\שנה ד\קריפטוגרפיה\hw7\{}.sig'.format(MY_FIRST_NAME), 'wb') as fd:
        fd.write(first_name_sig)

    with open(r'C:\Users\ItamarS\Desktop\חשמל מדעי המחשב\שנה ד\קריפטוגרפיה\hw7\{}.sig'.format(MY_LAST_NAME), 'wb') as fd:
        fd.write(last_name_sig)

    print(ver.ver(vk=ver.init_vk(vk1), msg=MY_FIRST_NAME.encode(), sig=first_name_sig))
    print(ver.ver(vk=ver.init_vk(vk1), msg=MY_LAST_NAME.encode(), sig=last_name_sig))

    #with open(r'C:\Users\ItamarS\Desktop\חשמל מדעי המחשב\שנה ד\קריפטוגרפיה\hw7\{}.sig'.format(MY_FIRST_NAME), 'rb') as fd:
    #    print(ver.ver(vk=ver.init_vk(vk1), msg=MY_FIRST_NAME.encode(), sig=fd.read()))

    #with open(r'C:\Users\ItamarS\Desktop\חשמל מדעי המחשב\שנה ד\קריפטוגרפיה\hw7\{}.sig'.format(MY_LAST_NAME), 'rb') as fd:
    #    print(ver.ver(vk=ver.init_vk(vk1), msg=MY_LAST_NAME.encode(), sig=fd.read()))