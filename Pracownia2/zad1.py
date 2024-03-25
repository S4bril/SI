import itertools
import random
from enum import Enum

MAX_COST: int = 15
# def random_moves(board, positions):
#     letters = ['L', 'R', 'U', 'D']
#     random_list = [random.choice(letters) for _ in range(10)]
#     return direction_moves(board, positions, 1, random_list, "")
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
    #print(list(poss_choices))
    how_many_inv = list(map(find_min, poss_choices))
    #print(how_many_inv)
    min_inv = min(how_many_inv)
    # poss_choices = list(filter(lambda elem: how_many_inv[elem[0]] == min_inv, enumerate(poss_choices)))
    # rand_choice = random.choice(poss_choices)
    # return rand_choice[1]
    return min_inv

def solve(n, k, row_constraints, col_constraints):

    table = generate_table(n, k)
    tab_trans = [list(row) for row in zip(*table)]

    col_scores = [opt_dist(col, col_constraints[x]) for x, col in enumerate(tab_trans)]
    row_scores = [opt_dist(row, row_constraints[x]) for x, row in enumerate(table)]

    pot_rows_cols = compute_wrong_coordinates(table, row_constraints, col_constraints)
    iterations = 0
    while len(pot_rows_cols[0]) > 0 or len(pot_rows_cols[1]) > 0:
        if len(pot_rows_cols[0]) == 0:
            row_or_col = 1
        elif len(pot_rows_cols[1]) == 0:
            row_or_col = 0
        else:
            row_or_col = random.choice([0, 1])

        index = random.choice(pot_rows_cols[row_or_col])

        best_dif = -1
        best_i = -1
        # find the best pixel in row
        if row_or_col == 0:
            for i in range(k):
                # neg bit
                table[index][i] = 1 - table[index][i]
                tab_trans[i][index] = 1 - tab_trans[i][index]
                # new scores
                new_row_score = opt_dist(table[index], row_constraints[index])
                new_col_score = opt_dist(tab_trans[i], col_constraints[i])
                # back changes
                table[index][i] = 1 - table[index][i]
                tab_trans[i][index] = 1 - tab_trans[i][index]
                # save 'i'
                new_dif = (row_scores[index] + col_scores[i]) - (new_row_score + new_col_score)
                if new_dif > best_dif:
                    best_dif = new_dif
                    best_i = i
            # use best result
            if best_i >= 0:
                row_scores[index] = new_row_score
                col_scores[best_i] = new_col_score
                table[index][best_i] = 1 - table[index][best_i]
                tab_trans[best_i][index] = 1 - tab_trans[best_i][index]

        # find the best pixel in col
        else:
            for i in range(n):
                # neg bit
                table[i][index] = 1 - table[i][index]
                tab_trans[index][i] = 1 - tab_trans[index][i]
                # new scores
                new_col_score = opt_dist(tab_trans[index], col_constraints[index])
                new_row_score = opt_dist(table[i], row_constraints[i])
                # back changes
                table[i][index] = 1 - table[i][index]
                tab_trans[index][i] = 1 - tab_trans[index][i]
                # save 'i'
                new_dif = (col_scores[index] + row_scores[i]) - (new_row_score + new_col_score)
                if new_dif > best_dif:
                    best_dif = new_dif
                    best_i = i
            # use best result
            if best_i >= 0:
                row_scores[best_i] = new_row_score
                col_scores[index] = new_col_score
                table[best_i][index] = 1 - table[best_i][index]
                tab_trans[index][best_i] = 1 - tab_trans[index][best_i]
        # update iterations
        iterations += 1
        # after some attempts start with new random tab
        if iterations > 2000:
            table = generate_table(n, k)
            tab_trans = [list(row) for row in zip(*table)]
            iterations = 0
        # update wrong cols and rows
        pot_rows_cols = compute_wrong_coordinates(table, row_constraints, col_constraints)
    print(iterations)
    return table

def load_data(filename="zad_input.txt"):
    with open(filename, 'r') as file:
        lines = file.readlines()
        number_of_rows = lines[0].split(' ')[0]
        number_of_rows = int(number_of_rows)
        row = [line.strip().split(" ") for line in lines[1:number_of_rows+1]]
        col = [line.strip().split(" ") for line in lines[number_of_rows+1:]]
        row = [list(map(int, row)) for row in row]
        col = [list(map(int, col)) for col in col]
    return row, col


def generate_table(n, k):
    return [[random.randint(0, 1) for _ in range(k)] for _ in range(n)]


def compute_wrong_coordinates(table, row_constraints, col_constraints):
    potential_rows = []
    for i, row in enumerate(table):
        if opt_dist(row, row_constraints[i]) != 0:
            potential_rows.append(i)

    potential_cols = []
    transposed_array = [list(row) for row in zip(*table)]

    for j, column in enumerate(transposed_array):
        if opt_dist(column, col_constraints[j]) != 0:
            potential_cols.append(j)

    return potential_rows, potential_cols


def print_table(table):
    for row in table:
        print("  ".join(map(lambda x: "#" if x else ".", row)))


class ModeName(Enum):
    ROW = 0
    COL = 1



def write_table_to_file(table, filepath="zad_output.txt"):
    with open(filepath, 'w') as file:
        for row in table:
            file.write(''.join(map(lambda x: "#" if x else ".", row)) + '\n')


if __name__ == "__main__":
    # print(opt_dist([1, 1, 1, 1, 0, 0, 1], [2, 2]))

    row_constraints, col_constraints = load_data()
    n = len(row_constraints)
    k = len(col_constraints)

    tab = solve(n, k, row_constraints, col_constraints)

    write_table_to_file(tab)