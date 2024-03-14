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

if __name__ ==  "__main__":
    with open('zad4_input.txt', 'r') as file:
        lines = file.readlines()
        tests = [line.strip() for line in lines]
        result = [solve_test([test.split(' ')[0], int(test.split(' ')[1])]) for test in tests]
        with open('zad4_output.txt', 'w') as file_out:
            file_out.write('\n'.join(list(map(str, result))))