import random
import time
import copy

M = 8

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

weights = [[100, -20, 10, 5, 5, 10, -20, 100],
           [-20, -50, -2, -2, -2, -2, -50, -20],
           [10, -2, -1, -1, -1, -1, -2, 10],
           [5, -2, -1, -1, -1, -1, -2, 5],
           [5, -2, -1, -1, -1, -1, -2, 5],
           [10, -2, -1, -1, -1, -1, -2, 10],
           [-20, -50, -2, -2, -2, -2, -50, -20],
           [100, -20, 10, 5, 5, 10, -20, 100]]

fields = set()

for i in range(M):
    for j in range(M):
        if grid[i][j] is None:
            fields.add((j, i))

def reset_game():
    global grid, fields, move_list
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
                fields.add((j, i))

def get(x,y):
    if 0 <= x < M and 0 <= y < M:
        return grid[y][x]
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
    for (x, y) in fields:
        if any(can_beat(x, y, direction, player) for direction in directions):
            res.append((x, y))
    if not res:
        return None
    return res

def result():
    res = 0
    for y in range(M):
        for x in range(M):
            b = grid[y][x]
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

def result():
    res = 0
    for y in range(M):
        for x in range(M):
            b = grid[y][x]
            if b == 0:
                res -= 1
            elif b == 1:
                res += 1
    return res

def do_move(move, player):
    global grid, fields
    move_list.append(move)

    if move == None:
        return

    x, y = move
    x0, y0 = move
    grid[y][x] = player
    fields -= set([move])
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
                grid[ny][nx] = player

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
            # if player == 0:
            #     h -= result()
            # else:
            #     h += result()
            grid = grid_copy
            if h > best:
                best = h
                best_move = (mx, my)
        return best_move
    return None

def my_agent_minmax(player):
    def minimax()

def main():
    games = 1000
    my_agent_loses = 0
    agents = [random_move, my_agent_heuristics]
    for i in range(games):
        player = 0
        if i < games / 2:
            agent = 0  # random agent is starting
        else:
            agent = 1  # my agent is starting
        reset_game()

        while True:
            m = agents[agent](player)
            do_move(m, player)
            player = 1 - player
            agent = 1 - agent
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