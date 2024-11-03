import filecmp


def DFA_minimize(file_in, file_out):
    with open(file_in, "r") as file:
        lines = file.readlines()

    n = int(lines[0].strip())  # Number of states
    m = int(lines[1].strip())  # Number of alphabet symbols
    initial_state = int(lines[2].strip())
    accepting_states = set(map(int, lines[3].strip().split()))
    transitions = {}

    for line in lines[4:]:
        start, symbol, end = map(int, line.strip().split())
        if start not in transitions:
            transitions[start] = {}
        transitions[start][symbol] = end

    reachable_states = set()
    stack = [initial_state]

    while stack:
        state = stack.pop()
        if state not in reachable_states:
            reachable_states.add(state)
            for symbol in range(m):
                next_state = transitions.get(state, {}).get(symbol)
                if next_state is not None and next_state not in reachable_states:
                    stack.append(next_state)

    transitions = {state: {sym: end for sym, end in trans.items() if end in reachable_states}
                   for state, trans in transitions.items() if state in reachable_states}
    accepting_states &= reachable_states

    state_mapping = {old: new for new, old in enumerate(sorted(reachable_states))}
    transitions = {state_mapping[state]: {sym: state_mapping[end] for sym, end in trans.items()}
                   for state, trans in transitions.items()}
    initial_state = state_mapping[initial_state]
    accepting_states = {state_mapping[state] for state in accepting_states}

    non_accepting_states = set(state_mapping.values()) - accepting_states
    partitions = [non_accepting_states, accepting_states]
    state_to_partition = {}
    for idx, part in enumerate(partitions):
        for state in part:
            state_to_partition[state] = idx

    while True:
        new_partitions = []
        partition_mapping = {}

        for part in partitions:
            transition_groups = {}
            for state in part:
                key = tuple(state_to_partition.get(transitions.get(state, {}).get(sym, -1), -1) for sym in range(m))

                if key not in transition_groups:
                    transition_groups[key] = set()
                transition_groups[key].add(state)

            for group in transition_groups.values():
                new_partitions.append(group)
                for state in group:
                    partition_mapping[state] = len(new_partitions) - 1

        if len(new_partitions) == len(partitions):
            break

        partitions = new_partitions
        state_to_partition = partition_mapping

    minimized_transitions = {}
    new_initial_state = state_to_partition[initial_state]
    new_accepting_states = {state_to_partition[state] for state in accepting_states if state in state_to_partition}

    for part in partitions:
        representative = next(iter(part))
        new_state = state_to_partition[representative]
        minimized_transitions[new_state] = {}

        for sym in range(m):
            target_state = transitions.get(representative, {}).get(sym)
            if target_state is not None and target_state in state_to_partition:
                minimized_transitions[new_state][sym] = state_to_partition[target_state]

    with open(file_out, "w") as file:
        file.write(f"{len(partitions)}\n")
        file.write(f"{m}\n")
        file.write(f"{new_initial_state}\n")
        file.write(" ".join(map(str, sorted(new_accepting_states))) + "\n")

        for state, transition in minimized_transitions.items():
            for symbol, target in transition.items():
                file.write(f"{state} {symbol} {target}\n")


def is_accept_all(file_name):
    file = open(file_name, "r")
    strings = file.readlines()
    if strings[0].strip() == "1" and strings[3].strip() == "0":
        return True
    return False


def is_DFA_eq(file1, file2):
    minimized_file1 = "minimized_1.txt"
    minimized_file2 = "minimized_2.txt"

    DFA_minimize(file1, minimized_file1)
    DFA_minimize(file2, minimized_file2)

    with open(minimized_file1, "r") as f1, open(minimized_file2, "r") as f2:
        dfa1 = f1.readlines()
        dfa2 = f2.readlines()

    return dfa1 == dfa2
