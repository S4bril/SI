import random
import itertools


def opt_dist(line, setup):
    how_many = len(setup)
    length = len(line)

    def logical_xor(str1, str2):
        return bool(str1) ^ bool(str2)

    def check(choice):
        for idx, x in enumerate(choice):
            if x + setup[idx] > length:
                return False
            if idx + 1 < how_many:
                if x + setup[idx] + 1 > choice[idx + 1]:
                    return False
        return True

    def find_min(choice):
        temp_sum = 0
        for idx, x in enumerate(choice):
            temp_sum += logical_xor(x, line[idx])
        return temp_sum

    def generate_line(choice):
        new_line = [0] * length
        for idx, x in enumerate(choice):
            for i in range(setup[idx]):
                new_line[x + i] = 1
        return new_line

    poss_choices = itertools.combinations([x for x in range(0, length)], how_many)
    poss_choices = list(map(generate_line, filter(check, poss_choices)))
    how_many_inv = list(map(find_min, poss_choices))
    min_inv = min(how_many_inv)
    poss_choices = list(filter(lambda elem: how_many_inv[elem[0]] == min_inv, enumerate(poss_choices)))
    rand_choice = random.choice(poss_choices)
    return rand_choice[1]


def line_ok(line, setup):
    line_str = '0' + ''.join(map(str, line)) + '0'
    seqs = ['0' + '1' * x + '0' for x in setup]
    for idx, seq in enumerate(seqs):
        f = line_str.find(seq)
        if f == -1:
            return False
        else:
            line_str = line_str[f + setup[idx]:]
    if not (sum(map(int, setup)) == sum(map(int, line))):
        return False
    return True


def canvas_ok(canvas, rows, cols):
    for i in range(0, len(rows)):
        if not line_ok(canvas[i], rows[i]):
            return False
    res = [[canvas[j][i] for j in range(len(canvas))] for i in range(len(canvas[0]))]
    for i in range(0, len(cols)):
        if not line_ok(res[i], cols[i]):
            return False
    return True


def zad1(rows, cols, nrows, ncols):
    it = 0
    canvas = [[0 for j in range(ncols)] for i in range(nrows)]

    x = 0
    while not canvas_ok(canvas, rows, cols):
        if it > 2000:
            it = 0
            canvas = [[0 for j in range(len(cols))] for i in range(len(rows))]

        line = random.choice(canvas)
        it2 = 0
        while line_ok(line, rows[canvas.index(line)]) and it2 <= 100:
            it2 += 1
            line = random.choice(canvas)

        new_line = opt_dist(line, rows[canvas.index(line)])
        canvas[canvas.index(line)] = new_line

        transpose = random.randint(0, 100)
        if transpose >= 50:
            x += 1
            canvas = [[canvas[j][i] for j in range(len(canvas))] for i in range(len(canvas[0]))]
            cols, rows = rows, cols

        it += 1

    if x % 2:
        canvas = [[canvas[j][i] for j in range(len(canvas))] for i in range(len(canvas[0]))]
    return canvas


with open('zad_input.txt') as f:
    file = f.read().split("\n")
    rows, cols = map(int, file[0].split())
    idx = 1
    row_descs = []
    col_descs = []
    for i in range(rows):
        row_descs.append(list(map(int, file[idx].split())))
        idx += 1
    for i in range(cols):
        col_descs.append(list(map(int, file[idx].split())))
        idx += 1

with open('zad_output.txt', 'w') as f:
    res = zad1(row_descs, col_descs, rows, cols)
    for i in res:
        line = ""
        for j in range(len(i)):
            if i[j]:
                line += "#"
            else:
                line += "."
        print(line)
        line += "\n"
        f.write(line)