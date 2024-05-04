import random

M = 8

move_list = []

directions = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]

grid = [
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, 1, 0, None, None, None],
    [None, None, None, 0, 1, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None]
]

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
        [None, None, None, 1, 0, None, None, None],
        [None, None, None, 0, 1, None, None, None],
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
        return [None]
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

def random_move(player):
    ms = moves(player)
    if ms:
        return random.choice(ms)
    return [None]

if __name__ == '__main__':
    games = 2000
    for i in range(games):
        player = 0
        reset_game()

        while True:
            m = random_move(player)
            do_move(m, player)
            player = 1 - player
            # raw_input()
            if terminal():
                break
    print('Result', result())
