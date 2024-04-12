def B(i, j):
    return 'B_%d_%d' % (i, j)


def domains(BS):
    return [q + ' in 0..1' for q in BS]


def get_column(j, R):
    return [B(i, j) for i in range(R)]


def get_raw(i, C):
    return [B(i, j) for j in range(C)]


def sum_equal(Bs, sum):
    return


def radar(Bs, constrain):
    return 'all_distinct([' + ', '.join(Bs) + '])'


def all_radars(rows, cols, R, C):
    res = []
    for i, row in enumerate(rows):
        res.append(radar(get_raw(i, R), row))
    for i, col in enumerate(cols):
        res.append(radar(get_column(i, C), col))
    return res


def print_constraints(Cs, indent, d):
    position = indent
    writeln(indent * ' ', end='')
    for c in Cs:
        writeln(c + ',', end=' ')
        position += len(c)
        if position > d:
            position = indent
            writeln()
            writeln(indent * ' ', end='')


def storms(rows, cols, triples):
    writeln(':- use_module(library(clpfd)).')

    R = len(rows)
    C = len(cols)

    bs = [B(i, j) for i in range(R) for j in range(C)]
    writeln('solve([' + ', '.join(bs) + ']) :- ')

    # TODO: add some constraints
    cs = all_radars(rows, cols, R, C) #TODO finish contrains
    # writeln('    [%s] = [1,1,0,1,1,0,1,1,0,1,1,0,0,0,0,0,0,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0],' % (
    # ', '.join(bs),))  # only for test 1
    for i, j, val in triples:
        cs.append('%s #= %d' % (B(i, j), val))
    print_constraints(cs, 4, 70)
    writeln('    labeling([ff], [' + ', '.join(bs) + ']).')
    writeln('')
    writeln(":- solve(X), write(X), nl, told.")


def writeln(s):
    output.write(s + '\n')


txt = open('zad_input.txt').readlines()
output = open('zad_output.txt', 'w')

rows = len(map(int, txt[0].split()))
cols = len(map(int, txt[1].split()))
triples = []

for i in range(2, len(txt)):
    if txt[i].strip():
        triples.append(map(int, txt[i].split()))

storms(rows, cols, triples)


