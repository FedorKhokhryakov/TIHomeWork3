import filecmp


def DFA_minimize(file_in, file_out):
    with open(file_in, "r") as file:
        lines = file.readlines()

    # Parse the input
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

    # Step 1: Initialize the partitions
    non_accepting_states = set(range(n)) - accepting_states
    partitions = [non_accepting_states, accepting_states]
    state_to_partition = {}
    for idx, part in enumerate(partitions):
        for state in part:
            state_to_partition[state] = idx

    # Step 2: Refine the partitions until they are stable
    while True:
        new_partitions = []
        partition_mapping = {}

        for part in partitions:
            # Check if each state in the partition has the same transition behavior
            transition_groups = {}
            for state in part:
                key = tuple(state_to_partition.get(transitions.get(state, {}).get(sym, -1), -1) for sym in range(m))

                if key not in transition_groups:
                    transition_groups[key] = set()
                transition_groups[key].add(state)

            # Add the refined groups to new partitions
            for group in transition_groups.values():
                new_partitions.append(group)
                for state in group:
                    partition_mapping[state] = len(new_partitions) - 1

        # Check for stability
        if len(new_partitions) == len(partitions):
            break

        partitions = new_partitions
        state_to_partition = partition_mapping

    # Step 3: Map states and build minimized DFA
    minimized_transitions = {}
    new_initial_state = state_to_partition[initial_state]
    new_accepting_states = {state_to_partition[state] for state in accepting_states if state in state_to_partition}

    for part in partitions:
        representative = next(iter(part))  # Take a representative of the partition
        new_state = state_to_partition[representative]
        minimized_transitions[new_state] = {}

        for sym in range(m):
            target_state = transitions.get(representative, {}).get(sym)
            if target_state is not None and target_state in state_to_partition:
                minimized_transitions[new_state][sym] = state_to_partition[target_state]

    # Write the minimized DFA to output file
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
