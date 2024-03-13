import random
import math
from enum import Enum

def load_data(filename="zad5_input.txt"):
    with open(filename, 'r') as file:
        lines = file.readlines()
        number_of_rows = lines[0].split(' ')[0]
        number_of_rows = int(number_of_rows)
        row = [int(line.strip()) for line in lines[1:number_of_rows+1]]
        col = [int(line.strip()) for line in lines[number_of_rows+1:]]
    return row, col

def count_ones(binary_string):
    return binary_string.count('1')

def count_zeros(binary_string):
    return binary_string.count('0')

def operations_needed(test):
    binary_string = ''.join(list(map(str, test[0])))
    block_size = test[1]

    n = len(binary_string)

    min = math.inf
    for i in range(n - block_size + 1):
        operations = (
                count_ones(binary_string[:i]) +
                count_zeros(binary_string[i:i+block_size]) +
                count_ones(binary_string[i+block_size:])
        )
        if operations < min:
            min = operations
    return min

def generate_table(n, k):
    return [[random.randint(0, 1) for _ in range(k)] for _ in range(n)]

def compute_wrong_coordinates(table, row_constraints, col_constraints):
    potential_rows = []
    for i, row in enumerate(table):
        if operations_needed((row, row_constraints[i])) != 0:
            potential_rows.append(i)

    potential_cols = []
    transposed_array = [list(row) for row in zip(*table)]

    for j, column in enumerate(transposed_array):
        if operations_needed((column, col_constraints[j])) != 0:
            potential_cols.append(j)

    return potential_rows, potential_cols

def print_table(table):
    for row in table:
        print("  ".join(map(lambda x: "#" if x else ".", row)))

class ModeName(Enum):
    ROW = 0
    COL = 1

def solve(n, k, row_constraints, col_constraints):

    table = generate_table(n, k)
    tab_trans = [list(row) for row in zip(*table)]

    col_scores = [operations_needed(([col[:]], col_constraints[x])) for x, col in enumerate(tab_trans)]
    row_scores = [operations_needed([[row[:]], row_constraints[x]]) for x, row in enumerate(table)]

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
                new_row_score = operations_needed((table[index], row_constraints[index]))
                new_col_score = operations_needed((tab_trans[i], col_constraints[i]))
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
                new_col_score = operations_needed([tab_trans[index], col_constraints[index]])
                new_row_score = operations_needed([table[i], row_constraints[i]])
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
        if iterations > 100:
            table = generate_table(n, k)
            tab_trans = [list(row) for row in zip(*table)]
            iterations = 0
        # update wrong cols and rows
        pot_rows_cols = compute_wrong_coordinates(table, row_constraints, col_constraints)
    print(iterations)
    return table

def write_table_to_file(table, filepath="zad5_output.txt"):
    with open(filepath, 'w') as file:
        for row in table:
            file.write(''.join(map(lambda x: "#" if x else ".", row)) + '\n')


if __name__ == '__main__':
    row_constraints, col_constraints = load_data()
    n = len(row_constraints)
    k = len(col_constraints)

    tab = solve(n, k, row_constraints, col_constraints)

    write_table_to_file(tab)