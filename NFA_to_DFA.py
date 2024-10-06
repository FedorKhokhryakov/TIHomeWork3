def update_step(pos, symbol, moves):
    next_pos = set()
    for p in pos:
        if (p, symbol) in moves:
            next_pos.update(moves[(p, symbol)])
    return next_pos


def NFA_to_DFA(file_in, file_out):
    input = open(file_in, "r")
    strings = input.readlines()
    n, m = int(strings[0]), int(strings[1])
    symbols = [str(i) for i in range(m)]
    q_start, q_finish = [], []
    q = {}
    for x in strings[2].split():
        q_start.append(int(x))
    for x in strings[3].split():
        q_finish.append(int(x))
    for i in range(4, len(strings)):
        x = strings[i].split()
        if (int(x[0]), x[1]) not in q:
            q[(int(x[0]), x[1])] = []
        q[(int(x[0]), x[1])].append(int(x[2]))

    moves = {}
    pos = {}
    queue = []
    for x in q_start:
        st_pos = frozenset({x})
        pos[st_pos] = 0
        queue.append(st_pos)
    cnt = 1
    while queue:
        cur = queue.pop()
        for symbol in symbols:
            p = frozenset(update_step(cur, symbol, q))
            if not p:
                continue
            if p not in pos:
                pos[p] = cnt
                cnt += 1
                queue.append(p)
            moves[(pos[cur], symbol)] = [pos[p]]

    new_finish = {pos[p] for p in pos if any(s in q_finish for s in p)}

    output = open(file_out, "w")
    output.write(f"{str(len(pos))}\n{str(m)}\n{str(*q_start)}\n")
    output.writelines([str(i) + ' ' for i in new_finish])
    output.write('\n')
    for move in moves.items():
        output.write(f"{str(move[0][0])} {str(move[0][1])} {str(move[1][0])}\n")
