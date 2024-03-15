MAX_COST = 15


def from_last_list(lst, block_size):
    pass


def operations(row, sizes):
    all_ones = sum(row)
    len_of_sizes = len(sizes)
    common_block_size = sum(sizes) + len_of_sizes - 1
    states = {}  # (index, block_size) -> cost

    def operations_for_block_in_range(beg, end, block_size, ones_in_range):

        res = []  # (index, block_size, cost)
        steps = 1
        ones_inside = 0
        checked_cases = 1

        for i in range(beg, end):
            print(i, res)
            if steps < block_size:
                ones_inside += row[i]
            elif steps == block_size:
                cost_inside = block_size - ones_inside
                cost_outside = ones_in_range - ones_inside
                cost = cost_inside + cost_outside
                res.append((beg, beg + block_size, cost))
            else:
                # update ones inside block in current position
                ones_inside += row[i]
                ones_inside -= row[i - block_size - 1]

                # compute cost of block in current position
                cost_inside = block_size - ones_inside
                cost_outside = ones_in_range - ones_inside
                cost = cost_inside + cost_outside

                res.append((beg + checked_cases, block_size, cost))

                checked_cases += 1

            steps += 1

        return res

    print(0, len(row))
    print(operations_for_block_in_range(0, len(row), sizes[0], all_ones))

    # def helper(size_index, beg, end, ones_in_range):
    #
    #     if size_index >= len_of_sizes:
    #         return None
    #
    #     if end - beg < sizes[0]:
    #         return None
    #
    #     size = sizes[size_index]
    #     before = 0
    #     inside = sum(row[:size])
    #     after = all_ones - inside
    #
    #     for i in range(size, ):
    #         for i in range(x):
    #             inside += ls[i]
    #
    # helper(0, 0, len_of_sizes - 1, all_ones)


    # find block of y size


if __name__ == "__main__":
    operations([0, 1, 0, 0, 1, 1, 0, 0], [5])
