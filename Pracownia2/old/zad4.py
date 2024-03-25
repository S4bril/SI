import math

def count_ones(binary_string):
     return binary_string.count('1')

def count_zeros(binary_string):
    return binary_string.count('0')

def solve_test(test):
    binary_string, block_size = test

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

def operations_needed(row, sizes):
    end = len(row)
    len_of_sizes = len(sizes)
    #states = {}  # (beg, size_index) -> cost

    def helper(beg, size_index):
        if size_index >= len_of_sizes:
            return 0
        block_size = sizes[size_index]
        if end - beg < sizes[size_index]:
            return None
        # if (beg, size_index) in states:
        #     return states[(beg, size_index)]
        best_cost = MAX_COST
        steps = 1
        ones_before = 0
        ones_inside = 0
        counter = 0
        for i in range(beg, end):
            if steps < block_size:
                ones_inside += row[i]
            else:
                # update ones inside block in current position
                ones_inside += row[i]
                if steps != block_size:
                    temp = row[i - block_size - 1]
                    ones_inside -= temp
                    ones_before += temp
                # compute cost of block in current position
                cost_inside = block_size - ones_inside
                cost_rest = helper(i + 2, size_index + 1)
                if cost_rest is not None:
                    counter += 1
                    cost = (cost_inside + ones_before +
                            helper(i + 2, size_index + 1))
                    if i + 2 < end:
                        cost += row[i + 1]
                    if cost < best_cost:
                        best_cost = cost
            steps += 1
        if counter == 0:
            #states[(beg, size_index)] = None
            return None
        #states[(beg, size_index)] = best_cost
        return best_cost
    return helper(0, 0)
    #print(operations_for_block_in_range(0, 0))

if __name__ ==  "__main__":
    with open('zad4_input.txt', 'r') as file:
        lines = file.readlines()
        tests = [line.strip() for line in lines]
        result = [solve_test([test.split(' ')[0], int(test.split(' ')[1])]) for test in tests]
        with open('zad4_output.txt', 'w') as file_out:
            file_out.write('\n'.join(list(map(str, result))))