import itertools
from queue import Queue
from copy import deepcopy
from time import time
from collections import deque

row_bindings = []
col_bindings = []

NUM_OF_ROWS = 0
NUM_OF_COLS = 0

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
    global best_targets
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

    variables = {}
    # generate row vars
    for i in range(NUM_OF_ROWS):
        length = NUM_OF_COLS
        how_many = len(row_bindings[i])
        poss_choices = itertools.combinations([x for x in range(0, length)], how_many)
        poss_choices = filter(lambda x: check(x, row_bindings[i]), poss_choices)
        poss_choices = list(map(lambda x: generate_line(x, row_bindings[i], length), poss_choices))
        midpoint = len(poss_choices) // 2
        variables[('r', i)] = poss_choices[midpoint:] + poss_choices[:midpoint]

    # generate col vars
    for i in range(NUM_OF_COLS):
        length = NUM_OF_ROWS
        how_many = len(col_bindings[i])
        poss_choices = itertools.combinations([x for x in range(0, length)], how_many)
        poss_choices = filter(lambda x: check(x, col_bindings[i]), poss_choices)
        poss_choices = list(map(lambda x: generate_line(x, col_bindings[i], length), poss_choices))
        midpoint = len(poss_choices) // 2
        variables[('c', i)] = poss_choices[midpoint:] + poss_choices[:midpoint]
    best_targets = variables.keys()
    return variables
def sure_values3(key, variables):
    lines = [int(''.join(map(str, x)), 2) for x in variables[key]]

    line_and = lines[0]
    line_or = lines[0]

    for line in lines[1:]:
        line_and &= line
        line_or |= line

    res = []
    for i in range(len(bin(line_and)) - 2):  # Determine the length of the binary representation
        if line_and & (1 << i):
            res.append(i)
        elif not line_or & (1 << i):
            res.append(i)

    return res
def sure_values2(key, variables):
    def helper(lst):
        return int(''.join(map(str, lst)), 2)

    lines = list(map(helper, variables[key]))

    def logical_or(str1, str2):
        return str1 or str2

    def logical_and(str1, str2):
        return str1 and str2

    # and
    line_and = lines[0]
    for line in lines[1:]:
        line_and &= line#[logical_and(x, y) for x, y in zip(line_and, line)]
    # or
    line_or = lines[0]
    for line in lines[1:]:
        line_or |= line#[logical_or(x, y) for x, y in zip(line_or, line)]

    res = []
    # for i in range(len(line_and)):
    #     if line_and[i]:
    #         res.append(i)
    #     elif not line_or[i]:
    #         res.append(i)
    length = line_and.bit_length()
    for i in range(length):
        if (line_and >> i) & 1 or not (line_or >> i) & 1:
            res.append(length - 1 - i)
    # print(variables[key])
    # print(res)
    return res
def sure_values(key, variables):
    lines = [list(map(bool, x)) for x in variables[key]]

    def logical_or(str1, str2):
        return str1 or str2

    def logical_and(str1, str2):
        return str1 and str2

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
        if line_and[i]:
            res.append(i)
        elif not line_or[i]:
            res.append(i)

    # print(res, sure_values2(key, variables))
    return res

def delete_lines(key, sure_v, index, variables):
    prev_len = len(variables[key])
    # print("lol", vars[key], sure_v)
    lines = list(filter(lambda line: line[index] == sure_v, variables[key]))
    variables[key] = lines
    # print("lol", lines)
    return not prev_len == len(lines)
counter = 0
def ac3(vars_local):
    # global counter
    # counter += 1
    # fill queue with all nodes
    # q = Queue()
    q = deque()
    # for key in vars.keys():
    #     q.put(key)
    for i in range(NUM_OF_ROWS):
        # q.put(('r', i))
        q.append(('r', i))
    for i in range(NUM_OF_COLS):
        # q.put(('c', i))
        q.append(('c', i))

    # while not q.empty():
    while q:
        # row_or_col, index = q.get()
        row_or_col, index = q.popleft()
        key = row_or_col, index

        if row_or_col == 'r':
            neighbors = 'c'
        else:
            neighbors = 'r'

        sure_cells = sure_values(key, vars_local)
        for cell in sure_cells:
            if (len(vars_local[(neighbors, cell)]) > 1
                    and delete_lines((neighbors, cell), vars_local[key][0][cell], index, vars_local)):
                if not vars_local[(neighbors, cell)]:
                    return False
                # q.put((neighbors, cell))
                q.append((neighbors, cell))
    return True

# def next_key(key):
#     if key[0] == 'r' and key[1] == NUM_OF_ROWS - 1:
#         return 'c', 0
#     if key[0] == 'c' and key[1] == NUM_OF_COLS - 1:
#         return None
#     return key[0], key[1] + 1

def next_key(key):
    key += 1
    # print(len(best_targets), NUM_OF_ROWS + NUM_OF_COLS)
    if key >= NUM_OF_ROWS + NUM_OF_COLS:
        return None
    return key

def is_solved(vars_local):
    for val in vars_local.values():
        if len(val) != 1:
            return False
    return True

def back_tracking(curr_vars):
    visited = set()
    not_visited = set(curr_vars.keys())
    def best_target(variables):
        min_len = 10000000
        res = None
        for key in list(not_visited):
            length = len(variables[key])
            if length < min_len:
                min_len = length
                res = key
        return res

    key = best_target(curr_vars)
    visited.add(key)
    not_visited.remove(key)
    def helper(key, curr_vars):
        if key is None:
            if is_solved(curr_vars):
                return curr_vars
            return None

        for poss in curr_vars[key]:
            curr_vars_copy = curr_vars.copy()
            curr_vars_copy[key] = [poss]
            if not ac3(curr_vars_copy):
                continue
            next_k = best_target(curr_vars_copy)
            visited.add(next_k)
            not_visited.remove(next_k)
            res = helper(next_k, curr_vars_copy)
            if res is not None:
                return res

        return None
    return helper(key, curr_vars)

def write_result(variables):

    def convert(num):
        if num == 1:
            return '#'
        return '.'

    with open('zad_output.txt', 'w') as f:
        for i in range(NUM_OF_ROWS):
            line = list(map(convert, variables[('r', i)][0]))
            f.write("".join(line) + '\n')

if __name__ == "__main__":
    start_time = time()
    load_data()
    variables = generate_vars()
    # print(best_targets)
    ac3(variables)
    result = back_tracking(variables.copy())
    # print(result)
    write_result(result)
    end_time = time()
    elapsed_time = end_time - start_time  # Calculate elapsed time
    print("Elapsed time:", elapsed_time, "seconds")
    # print(counter)
    # print("lol")