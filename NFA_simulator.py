def NFA_simulator(filename, str):
    file = open(filename, "r")
    strings = file.readlines()
    n, m = int(strings[0]), int(strings[1])
    q_start, q_finish, q_current = [], [], []
    p = [[] * n for i in range(n)]
    for x in strings[2].split():
        q_start.append(int(x))
    q_current = q_start
    for x in strings[3].split():
        q_finish.append(int(x))
    for i in range(4, len(strings)):
        x = strings[i].split()
        p[int(x[0])].append((int(x[1]), int(x[2])))
    for c in str:
        new_q = []
        for q in q_current:
            for i in p[q]:
                if i[0] == int(c):
                    new_q.append(i[1])
        q_current = new_q
    return len(set(q_finish) & set(q_current)) != 0