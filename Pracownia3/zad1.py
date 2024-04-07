import itertools
from queue import Queue

row_bindings = []
col_bindings = []

NUM_OF_ROWS = 0
NUM_OF_COLS = 0

vars = {}

def load_data():
    global NUM_OF_ROWS, NUM_OF_COLS
    with open('zad_input.txt') as f:
        file = f.read().split("\n")
        rows, cols = map(int, file[0].split())
        idx = 1
        for i in range(rows):
            row_bindings.append(list(map(int, file[idx].split())))
            idx += 1
        for i in range(cols):
            col_bindings.append(list(map(int, file[idx].split())))
            idx += 1
    NUM_OF_ROWS = len(row_bindings)
    NUM_OF_COLS = len(col_bindings)


def generate_vars():

    def generate_line(choice, binding, length):
        new_line = [0] * length
        for idx, x in enumerate(choice):
            for i in range(binding[idx]):
                new_line[x + i] = 1
        return new_line

    def check(choice, binding):
        for idx, x in enumerate(choice):
            if x + binding[idx] > length:
                return False
            if idx + 1 < how_many:
                if x + binding[idx] + 1 > choice[idx + 1]:
                    return False
        return True

    # generate row vars
    for i in range(NUM_OF_ROWS):
        length = NUM_OF_COLS
        how_many = len(row_bindings[i])
        poss_choices = itertools.combinations([x for x in range(0, length)], how_many)
        poss_choices = filter(lambda x: check(x, row_bindings[i]), poss_choices)
        poss_choices = list(map(lambda x: generate_line(x, row_bindings[i], length), poss_choices))
        vars[('r', i)] = poss_choices

    # generate col vars
    for i in range(NUM_OF_COLS):
        length = NUM_OF_ROWS
        how_many = len(col_bindings[i])
        poss_choices = itertools.combinations([x for x in range(0, length)], how_many)
        poss_choices = filter(lambda x: check(x, col_bindings[i]), poss_choices)
        poss_choices = list(map(lambda x: generate_line(x, col_bindings[i], length), poss_choices))
        vars[('c', i)] = poss_choices

def sure_values(key):
    lines = vars[key]

    def logical_or(str1, str2):
        return int(bool(str1) or bool(str2))

    def logical_and(str1, str2):
        return int(bool(str1) and bool(str2))

    # and
    line_and = lines[0]
    for line in lines[1:]:
        line_and = [logical_and(x, y) for x, y in zip(line_and, line)]
    # or
    line_or = lines[0]
    for line in lines[1:]:
        line_or = [logical_or(x, y) for x, y in zip(line_or, line)]

    res = []
    for i in range(len(line_and)):
        if bool(line_and[i]):
            res.append(i)
        elif not bool(line_or[i]):
            res.append(i)

    return res

# def ac3():
#     # fill queue with all nodes
#     q = Queue()
#     for key in vars.keys():
#         q.put(key)
#
#     while not q.empty():
#         current_key = q.get()

# def write_result():
#     with open('zad_output.txt', 'w') as f:
#         res = zad1(row_descs, col_descs, rows, cols)
#         for i in res:
#             line = ""
#             for j in range(len(i)):
#                 if i[j]:
#                     line += "#"
#                 else:
#                     line += "."
#             print(line)
#             line += "\n"
#             f.write(line)

if __name__ == "__main__":
    load_data()
    print(row_bindings, col_bindings)
    print(NUM_OF_ROWS, NUM_OF_COLS)
    generate_vars()
    print(vars)
    print(sure_values(('r', 2)))