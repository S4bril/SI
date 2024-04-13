def B(i, j):
    return 'B_%d_%d' % (i, j)


def domains(BS):
    return [q + ' in 0..1' for q in BS]


def get_column(j, R):
    return [B(i, j) for i in range(R)]


def get_raw(i, C):
    return [B(i, j) for j in range(C)]


def sum_equal(Bs, constrain):
    return 'sum([' + ', '.join(Bs) + '], #=, ' + str(constrain) + ')'


def sum_different(Bs, constrain):
    return r'sum([' + ', '.join(Bs) + r'], #\=, ' + str(constrain) + ')'


def radar(rows, cols, R, C):
    res = []
    for i, row in enumerate(rows):
        res.append(sum_equal(get_raw(i, R), row))
    for i, col in enumerate(cols):
        res.append(sum_equal(get_column(i, C), col))
    return res


def check_squares(R, C):
    square = [(0, 0), (0, 1), (1, 0), (1, 1)]

    def get_square(offset):
        return [B(sq[0] + offset[0], sq[1] + offset[1]) for sq in square]

    offsets = [get_square((i, j)) for i in range(R - 1) for j in range(C - 1)]

    def sum_on_diagonals(sq):
        return "{0} + {3} #= 2 #<==> {1} + {2} #= 2".format(sq[0], sq[1], sq[2], sq[3])

    return [sum_on_diagonals(off) for off in offsets]


def check_rectangles(R, C):
    cells_horizontal = [(0, 0), (0, 1), (0, 2)]
    cells_vertical = [(0, 0), (1, 0), (2, 0)]
    offsets_horizontal = [(i, j) for i in range(R) for j in range(C - 2)]
    offsets_vertical = [(i, j) for i in range(R - 2) for j in range(C)]

    def get_rectangle(cells, offset):
        return [B(cell[0] + offset[0], cell[1] + offset[1]) for cell in cells]

    rectangles = [get_rectangle(cells_horizontal, off) for off in offsets_horizontal]
    rectangles += [get_rectangle(cells_vertical, off) for off in offsets_vertical]

    def implication(rec):
        return "{1} #==> {0} + {2} #> 0".format(rec[0], rec[1], rec[2])

    return [implication(rec) for rec in rectangles]


def print_constraints(Cs, indent, d):
    position = indent
    output.write(indent * ' ')
    for c in Cs:
        output.write(c + ', ')
        position += len(c)
        if position > d:
            position = indent
            output.write('\n' + indent * ' ')


def storms(rows, cols, triples):
    writeln(':- use_module(library(clpfd)).')

    R = len(rows)
    C = len(cols)

    bs = [B(i, j) for i in range(R) for j in range(C)]
    writeln('solve([' + ', '.join(bs) + ']) :- ')

    # TODO: add some constraints
    cs = domains(bs) + radar(rows, cols, R, C) + check_rectangles(R, C) + check_squares(R, C)
    # cs = domains(bs) + radar(rows, cols, R, C) + good_three_cells_in_rows(R, C) + good_three_cells_in_cols(R, C) + rectangle(R, C)
    # cs = domains(bs) + radar(rows, cols, R, C) + good_three_cells_in_rows(R, C) + good_three_cells_in_cols(R, C) + check_squares(R, C)

    for i, j, val in triples:
        cs.append('%s #= %d' % (B(i, j), val))

    print_constraints(cs, 4, 70)
    writeln('')
    writeln('    labeling([ff], [' + ', '.join(bs) + ']).')
    writeln('')
    writeln(":- solve(X), write(X), nl, told.")
    # print(check_squares(R, C))
    # print(check_rectangles(R, C))


def writeln(s):
    output.write(s + '\n')


txt = open('zad_input.txt').readlines()
output = open('zad_output.txt', 'w')

rows = list(map(int, txt[0].split()))
cols = list(map(int, txt[1].split()))
triples = []

for i in range(2, len(txt)):
    if txt[i].strip():
        triples.append(list(map(int, txt[i].split())))

storms(rows, cols, triples)
