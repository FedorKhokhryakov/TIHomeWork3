class Virtual_mashine_regex:
    def __init__(self, instructions):
        self.instructions = instructions

    def run(self, string):
        states = [(0, 0)]

        while states:
            program_counter, string_index = states.pop()
            if program_counter >= len(self.instructions):
                continue

            inst = self.instructions[program_counter]

            if inst.op_type == "char":
                if string_index < len(string) and string[string_index] == inst.param1:
                    states.append((program_counter + 1, string_index + 1))
            elif inst.op_type == "match" and string_index == len(string):
                return True
            elif inst.op_type == "jump":
                states.append((inst.param1, string_index))
            elif inst.op_type == "branch":
                states.append((inst.param1, string_index))
                states.append((inst.param2, string_index))

        return False


class Instruction:
    def __init__(self, op_type, p1=None, p2=None):
        self.op_type = op_type
        self.param1 = p1
        self.param2 = p2

    def __repr__(self):
        if self.op_type == "char":
            return f'char {self.param1}'
        elif self.op_type == "match":
            return 'match'
        elif self.op_type == "jump":
            return f'jump {self.param1}'
        elif self.op_type == "branch":
            return f'branch {self.param1}, {self.param2}'

def build_pattern(pattern):
    instructions = {}
    pos = 0
    neg = -1

    for i in range(len(pattern)):
        if pattern[i] == "a" or pattern[i] == "b":
            instructions[pos] = Instruction("char", pattern[i])
            pos += 1
        elif pattern[i] == "*":
            branch_inst = Instruction("branch", pos, pos + 2)
            instructions[pos] = instructions[pos - 1]
            instructions[pos - 1] = branch_inst
            instructions[pos + 1] = Instruction("jump", pos - 1)
            pos += 2
        elif pattern[i] == "+":
            branch_inst = Instruction("branch", pos - 1, pos + 1)
            instructions[pos] = branch_inst
            pos += 1
        elif pattern[i] == "?":
            branch_inst = Instruction("branch", pos, pos + 1)
            instructions[pos] = instructions[pos - 1]
            instructions[pos - 1] = branch_inst
            pos += 1
        elif pattern[i] == "|":
            branch_inst = Instruction("branch", neg + 1, pos + 1)
            instructions[neg] = branch_inst
            instructions[pos] = Instruction("jump", -1)
            pos += 1
            neg -= 1

    instructions[pos] = Instruction("match")

    for i in sorted(instructions.keys()):
        if instructions[i].op_type == "jump" and instructions[i].param1 == -1:
            instructions[i].param1 = pos

    corrected_instructions = []
    neg += 1
    for i in sorted(instructions.keys()):
        if instructions[i].op_type in {"jump", "branch"}:
            instructions[i].param1 -= neg
        if instructions[i].op_type == "branch":
            instructions[i].param2 -= neg
        corrected_instructions.append(instructions[i])

    return corrected_instructions
