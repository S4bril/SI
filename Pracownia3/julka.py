def B(i, j):
    return 'B_%d_%d' % (i, j)


def domains(Vs):
    return [q + ' in 0..1' for q in Vs]


def get_row(i, cols_num):
    return [B(i, j) for j in range(cols_num)]


def get_column(j, rows_num):
    return [B(i, j) for i in range(rows_num)]


def is_sum_equal(Qs, q):
    return 'sum([' + ', '.join(Qs) + '], #=, ' + str(q) + ')'


def check_rows(rows, cols_num):
    return [is_sum_equal(get_row(i, cols_num), row) for i, row in enumerate(rows)]


def check_cols(cols, rows_num):
    return [is_sum_equal(get_column(i, rows_num), col) for i, col in enumerate(cols)]


# A + 2B + 3C != 2
# Jeżeli środkowy piksel jest ustawiony, to wówczas przynajmniej 1 z
# otaczających go jest jedynką.
def good_three_cells_in_rows(cols_num, rows_num):
    return [f"{B(i + 1, j)} #= 1 #==> {B(i, j)} + {B(i + 2, j)} #>= 1"
            for i in range(rows_num - 2) for j in range(cols_num)]


def good_three_cells_in_cols(cols_num, rows_num):
    return [f"{B(i, j + 1)} #= 1 #==> {B(i, j)} + {B(i, j + 2)} #>= 1"
            for i in range(rows_num) for j in range(cols_num - 2)]


# B × (A + C) != 2
def rectangle(cols_num, rows_num):
    return [f"{B(i, j)} + {B(i + 1, j + 1)} #= 2 #<==> {B(i, j + 1)} + {B(i + 1, j)} #= 2"
            for j in range(cols_num - 1) for i in range(rows_num - 1)]


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

    cs = domains(bs) + check_rows(rows, C) + check_cols(cols, R) + good_three_cells_in_cols(C, R) \
         + good_three_cells_in_rows(C, R) + rectangle(C, R)

    for i, j, val in triples:
        cs.append('%s #= %d' % (B(i, j), val))

    print_constraints(cs, 4, 70)
    writeln('')
    writeln('    labeling([ff], [' + ', '.join(bs) + ']).')
    writeln('')
    writeln(":- solve(X), write(X), nl, told.")


def writeln(s):
    output.write(s + '\n')


txt = open('zad_input.txt').readlines()
output = open('zad_output.txt', 'w')

rows = list(map(int, txt[0].split()))
cols = list(map(int, txt[1].split()))
triples = []

for i in range(2, len(txt)):
    if txt[i].strip():
        triples.append(map(int, txt[i].split()))

storms(rows, cols, triples)