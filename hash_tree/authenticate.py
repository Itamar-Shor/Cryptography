import hashlib


def find_index(students, name):
    for idx in range(len(students)):
        if name in students[idx]:
            return idx
    return -1


def calc_initial_hash(students):
    res = []
    for student in students:
        m = hashlib.sha256()
        m.update(student.replace('\n', '').encode('ASCII'))
        res.append(m.digest())
    return res


def get_root_hash(students):
    students_hash = calc_initial_hash(students)
    while len(students_hash) > 1:
        temp = []
        for idx in range(0, len(students_hash), 2):
            m = hashlib.sha256()
            m.update(students_hash[idx])
            m.update(students_hash[idx+1])
            temp.append(m.digest())
        students_hash = temp
    return students_hash[0].hex()


def calc_auth_path(students, name):
    students_hash = calc_initial_hash(students)
    target_idx = find_index(students, name)
    res = []
    while len(students_hash) > 1:
        temp = []
        for idx in range(0, len(students_hash), 2):
            m = hashlib.sha256()
            m.update(students_hash[idx])
            m.update(students_hash[idx+1])
            temp.append(m.digest())
            if (idx // 2) == (target_idx // 2):
                res.append(students_hash[idx] + students_hash[idx+1])

        target_idx = target_idx // 2
        students_hash = temp

    return res


if __name__ == '__main__':
    me = 'Itamar Shor'
    students_path = r'C:\Users\ItamarS\Desktop\חשמל מדעי המחשב\שנה ד\קריפטוגרפיה\hw3\students.txt'
    with open(students_path, 'r') as fd:
        data = fd.readlines()
        root_hash = get_root_hash(data)
        my_auth_path = calc_auth_path(data, me)

    print('root hash:', root_hash)
    print('my authentication path:', '\n'.join([line.hex() for line in my_auth_path]) + '\n')