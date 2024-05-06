import random
import time
import copy
from tqdm import tqdm
import math

M = 8

states = {}

rev = []

move_list = []

directions = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]

grid = [
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None,  1,    0,   None, None, None],
    [None, None, None,  0,    1,   None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None]
]

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

fields = set()

def last_step_back():
    global grid, fields, move_list, rev

    move = move_list[-1]
    move_list = move_list[:-1]

    r = rev[-1]
    rev = rev[:-1]
    if move:
        fields.add(move)
        grid[move[0]][move[1]] = None

        for cell in r:
            grid[cell[0]][cell[1]] = 1 - grid[cell[0]][cell[1]]

def print_grid():
    print("  ", end="")
    for col_idx in range(len(grid[0])):
        print(f"{col_idx:2}", end="")
    print("\n   ---------------")
    for row_idx, row in enumerate(grid):
        print(f"{row_idx:2}|", end="")
        for cell in row:
            if cell is None:
                print("X", end=" ")  # Print empty cell
            else:
                print(cell, end=" ")  # Print cell value
        print()
    print()

def reset_game():
    global grid, fields, move_list, rev
    rev = []
    move_list = []
    grid = [
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None,  1,    0,   None, None, None],
        [None, None, None,  0,    1,   None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None]
    ]
    fields = set()
    for i in range(M):
        for j in range(M):
            if grid[i][j] is None:
                fields.add((i, j))

def get(x,y):
    if 0 <= x < M and 0 <= y < M:
        return grid[x][y]
    return None

def can_beat(x, y, d, player):
    dx, dy = d
    x += dx
    y += dy
    cnt = 0
    while get(x, y) == 1-player:
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
            b = grid[x][y]
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
        rev.append(None)
        return

    # print(move)
    x, y = move
    x0, y0 = move
    grid[x][y] = player # y x ????
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
                grid[nx][ny] = player
                reversed_cells.append((nx, ny))
    rev.append(reversed_cells)

def heuristics(player):
    res = 0
    for i in range(M):
        for j in range(M):
            if grid[i][j] == player:
                res += weights[i][j]
    return res

def random_move(player):
    ms = moves(player)
    if ms:
        return random.choice(ms)
    return None

def my_agent_weights(player):
    ms = moves(player)
    if ms:
        best = -10000
        best_move = None
        for (mx, my) in ms:
            if weights[mx][my] > best:
                best = weights[mx][my]
                best_move = (mx, my)
        return best_move
    return None

def my_agent_heuristics(player):
    global grid
    ms = moves(player)
    if ms:
        best = -10000
        best_move = None
        for (mx, my) in ms:
            grid_copy = copy.deepcopy(grid)
            do_move((mx, my), player)
            h = heuristics(player)
            if player == 0:
                h -= result()
            else:
                h += result()
            last_step_back(grid_copy)
            if h > best:
                best = h
                best_move = (mx, my)
        return best_move
    return None

def my_agent_minmax(agent):
    # if len(move_list) < 10:
    #     # print("lol")
    #     return random_move(agent)
    def minimax(depth, maximizingPlayer, player, alpha, beta):
        global grid

        if terminal():
            if agent == 1:
                return None, result()
            else:
                return None, -result()

        if depth == 0:
            return None, heuristics(agent) - heuristics(1 - agent)
            # if maximizingPlayer:
            #     return None, heuristics(player)
            # else:
            #     return None, -heuristics(player)

        ms = moves(player)

        if not ms:
            do_move(None, player)
            res = minimax(depth-1, not maximizingPlayer, 1 - player, alpha, beta)
            last_step_back()
            return res

        # random.shuffle(ms)

        if maximizingPlayer:
            maxEval = -1000
            bestMove = None
            for (mx, my) in ms:
                do_move((mx, my), player)
                eval = minimax(depth-1, False, 1 - player, alpha, beta)
                last_step_back()
                if eval[1] > maxEval:
                    maxEval = eval[1]
                    bestMove = (mx, my)
                alpha = max(alpha, eval[1])
                if beta <= alpha:
                    break
            return bestMove, maxEval

        else:
            # ms = ms[:len(ms)]
            minEval = 1000
            bestMove = None
            for (mx, my) in ms:
                do_move((mx, my), player)
                eval = minimax(depth-1, True, 1 - player, alpha, beta)
                last_step_back()
                if eval[1] < minEval:
                    minEval = eval[1]
                    bestMove = (mx, my)
                beta = min(beta, eval[1])
                if beta <= alpha:
                    break
            return bestMove, minEval


            # mv = random.choice(ms)
            # do_move(mv, player)
            # eval = minimax(depth - 1, True, 1 - player)
            # last_step_back()
            # return mv, eval[1]

    x = len(move_list) // 10 + 1 #40?
    return minimax(x, True, agent, -1000000, 1000000)[0]

def main():
    games = 1000
    my_agent_loses = 0
    for i in tqdm(range(games), desc="Simulating games"):
        player = 0
        if i < games / 2:
            agent = 0
        else:
            agent = 1
        reset_game()

        while True:
            # print(rev)
            if agent == player:
                m = my_agent_minmax(player)
            else:
                m = random_move(player)
            do_move(m, player)
            player = 1 - player
            if terminal():
                break

        if agent == 1:
            my_agent_loses += int(result() < 0)
        else:
            my_agent_loses += int(result() > 0)
    print('My agent loses:', my_agent_loses)

if __name__ == '__main__':
    start_time = time.time()
    main()
    elapsed_time = time.time() - start_time
    print('Elapsed time:', elapsed_time, "seconds")