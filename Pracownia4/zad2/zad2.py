import random
import time
import sys
from collections import OrderedDict

M = 8

length = 0

states = {}

move_list = []

directions = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]

grid = []

weights = [
    [ 4, -3,  2,  2,  2,  2, -3,  4],
    [-3, -4, -1, -1, -1, -1, -4, -3],
    [ 2, -1,  1,  0,  0,  1, -1,  2],
    [ 2, -1,  0,  1,  1,  0, -1,  2],
    [ 2, -1,  0,  1,  1,  0, -1,  2],
    [ 2, -1,  1,  0,  0,  1, -1,  2],
    [-3, -4, -1, -1, -1, -1, -4, -3],
    [ 4, -3,  2,  2,  2,  2, -3,  4]
]
# weights = [
#     [20, -3, 11,  8,  8, 11, -3, 20],
#     [-3, -7, -4,  1,  1, -4, -7, -3],
#     [11, -4,  2,  2,  2,  2, -4, 11],
#     [ 8,  1,  2, -3, -3,  2,  1,  8],
#     [ 8,  1,  2, -3, -3,  2,  1,  8],
#     [11, -4,  2,  2,  2,  2, -4, 11],
#     [-3, -7, -4,  1,  1, -4, -7, -3],
#     [20, -3, 11,  8,  8, 11, -3, 20]
# ]

fields = set()

def last_step_back(rev):
    global grid, fields, move_list

    move = move_list.pop()

    if move:
        fields.add(move)
        grid[move[0] + 1][move[1] + 1] = None

        for cell in rev:
            grid[cell[0] + 1][cell[1] + 1] = 1 - grid[cell[0] + 1][cell[1] + 1]

def print_grid():
    print("  ", end="")
    for col_idx in range(len(grid[0])):
        print(f"{col_idx:2}", end="")
    print("\n   ---------------")
    for row_idx, row in enumerate(grid):
        print(f"{row_idx:2}|", end="")
        for cell in row:
            if cell is None:
                print(" ", end=" ")  # Print empty cell
            else:
                print(cell, end=" ")  # Print cell value
        print()
    print()

def reset_game():
    global grid, fields, move_list, length
    length = 0
    move_list = []
    grid = [
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None,  1,    0,   None, None, None, None],
        [None, None, None, None,  0,    1,   None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
    ]
    fields = {
        (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
        (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7),
        (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7),
        (3, 0), (3, 1), (3, 2),                 (3, 5), (3, 6), (3, 7),
        (4, 0), (4, 1), (4, 2),                 (4, 5), (4, 6), (4, 7),
        (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7),
        (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7),
        (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7),
    }

def get(x, y):
    return grid[x + 1][y + 1]

def can_beat(x, y, d, player):
    dx, dy = d
    x += dx
    y += dy
    cnt = 0
    while get(x, y) == 1 - player:
        x += dx
        y += dy
        cnt += 1
    return cnt > 0 and get(x, y) == player

def moves(player):
    res = []
    # print(fields)
    for (x, y) in fields:
        if any(can_beat(x, y, direction, player) for direction in directions):
            res.append((x, y))
    if not res:
        return None
    return res

def result():
    res = 0
    for x in range(M):
        for y in range(M):
            b = get(x, y)
            if b == 0:
                res -= 1
            elif b == 1:
                res += 1
    return res

def terminal():
    if not fields:
        return True
    if len(move_list) < 2:
        return False
    return move_list[-1] == move_list[-2] == None

def do_move(move, player):
    global grid, fields, rev
    move_list.append(move)

    if move == None:
        return []

    # print(move)
    x, y = move
    x0, y0 = move
    grid[x + 1][y + 1] = player # y x ????
    fields -= set([move])
    reversed_cells = []
    for dx, dy in directions:
        x, y = x0, y0
        to_beat = []
        x += dx
        y += dy
        while get(x, y) == 1 - player:
            to_beat.append((x, y))
            x += dx
            y += dy
        if get(x, y) == player:
            for (nx, ny) in to_beat:
                grid[nx + 1][ny + 1] = player
                reversed_cells.append((nx, ny))
    return reversed_cells

def random_move(player):
    ms = moves(player)
    if ms:
        return random.choice(ms)
    return None

def heuristics(player):
    res_player = 0
    res_opponent = 0
    for i in range(M):
        for j in range(M):
            if get(i, j) == player:
                res_player += weights[i][j]
            elif get(i, j) == 1 - player:
                res_opponent += weights[i][j]
    return res_player, res_opponent

def heuristics_function(moves, player) -> OrderedDict:
    global grid
    res = {}
    for m in moves:
        do_move(m, player)
        p, o = heuristics(player)
        res[m] = p - o
        last_step_back()
    return OrderedDict(sorted(res.items(), key=lambda item: item[1]))

def my_agent_minmax(agent):
    def minimax(depth, maximizingPlayer, player, alpha, beta):
        global grid

        if terminal():
            if agent == 1:
                return None, result()
            else:
                return None, -result()

        if depth == 0:
            p, o = heuristics(agent)
            return None, p - o

        ms = moves(player)

        if not ms:
            rev = do_move(None, player)
            res = minimax(depth-1, not maximizingPlayer, 1 - player, alpha, beta)
            last_step_back(rev)
            return res

        # random.shuffle(ms)
        # print(heuristics_function(ms, player))
        # ms = heuristics_function(ms, player).keys()

        if maximizingPlayer:
            maxEval = -1000
            bestMove = None
            for (mx, my) in ms:
                rev = do_move((mx, my), player)
                eval = minimax(depth-1, False, 1 - player, alpha, beta)
                last_step_back(rev)
                if eval[1] > maxEval:
                    maxEval = eval[1]
                    bestMove = (mx, my)
                alpha = max(alpha, eval[1])
                if beta <= alpha:
                    break
            return bestMove, maxEval

        else:
            # ms = ms[:len(ms)//2]
            minEval = 1000
            bestMove = None
            for (mx, my) in ms:
                rev = do_move((mx, my), player)
                eval = minimax(depth-1, True, 1 - player, alpha, beta)
                last_step_back(rev)
                if eval[1] < minEval:
                    minEval = eval[1]
                    bestMove = (mx, my)
                beta = min(beta, eval[1])
                if beta <= alpha:
                    break
            return bestMove, minEval

    x = len(move_list)**3 // 30000 + 1
    return minimax(x, True, agent, -1000000, 1000000)[0]

def send_message(message):
    sys.stdout.write(message + "\n")
    sys.stdout.flush()

def handle_ugo(command, player):
    move = my_agent_minmax(player)
    do_move(move, player)
    return move

def handle_hedid(command, player):
    move = int(command[3]), int(command[4])
    do_move(move, player)

if __name__ == '__main__':
    agent = 1
    for line in sys.stdin:
        command = line.strip().split(" ")

        if command[0] == "UGO":
            agent = 1 - agent
            move = handle_ugo(command[1:], agent)
            send_message(f"IDO {move[0]} {move[1]}")

        elif command[0] == "HEDID":
            agent = 1 - agent
            handle_hedid(command[1:], agent)

        elif command[0] == "ONEMORE":
            reset_game()
            agent = 1
            send_message("RDY")

        else:
            break