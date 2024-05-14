import random
import time
import sys
import math
from datetime import datetime

M = 8

move_list = []

directions = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]

grid = []

weights = [
    [50, -20, 15,  8,  8, 15, -20, 50],
    [-20, -50, -4,  1,  1, -4, -50, -20],
    [15, -4,  2,  2,  2,  2, -4, 15],
    [ 8,  1,  2, -3, -3,  2,  1,  8],
    [ 8,  1,  2, -3, -3,  2,  1,  8],
    [15, -4,  2,  2,  2,  2, -4, 15],
    [-20, -50, -4,  1,  1, -4, -50, -20],
    [50, -20, 15,  8,  8, 15, -20, 50]
]

fields = set()

def last_step_back(rev):
    global grid, fields, move_list

    move = move_list.pop()

    if move:
        fields.add(move)
        grid[move[0]][move[1]] = None

        for cell in rev:
            grid[cell[0]][cell[1]] = 1 - grid[cell[0]][cell[1]]

def print_grid():
    print("  ", end="", file=sys.stderr)
    for col_idx in range(len(grid[0])):
        print(f"{col_idx:2}", end="", file=sys.stderr)
    print("\n   ---------------", file=sys.stderr)
    for row_idx, row in enumerate(grid):
        print(f"{row_idx:2}|", end="", file=sys.stderr)
        for cell in row:
            if cell is None:
                print(" ", end=" ", file=sys.stderr)  # Print empty cell
            else:
                print(cell, end=" ", file=sys.stderr)  # Print cell value
        print(file=sys.stderr)
    print(file=sys.stderr)

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
        [None, None, None, None, None, None, None, None],
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
    if 0 <= x < M and 0 <= y < M:
        return grid[x][y]
    return None

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

    x, y = move
    x0, y0 = move
    grid[x][y] = player
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
    return reversed_cells

def random_move(player):
    ms = moves(player)
    if ms:
        return random.choice(ms)
    return None

def mobility(player):
    moves_player = 0
    moves_opponent = 0
    m = moves(player)
    if m:
        moves_player = len(m)
    m = moves(1 - player)
    if m:
        moves_opponent = len(m)
    return moves_player - moves_opponent

def heuristic(player):
    weights_player = 0
    weights_opponent = 0
    coins_player = 0
    coins_opponent = 0
    for i in range(M):
        for j in range(M):
            if get(i, j) == player:
                weights_player += weights[i][j]
                coins_player += 1
            elif get(i, j) == 1 - player:
                weights_opponent += weights[i][j]
                coins_opponent += 1
    w = (weights_player - weights_opponent)#*1000
    # coin_parity = 1000 * (coins_player - coins_opponent ) / (coins_player + coins_opponent)
    return w + 5 * mobility(player)#+ coin_parity

def my_agent_minmax(agent, start, time_for_move):
    def minimax(depth, maximizingPlayer, player, alpha, beta):
        global grid

        if terminal():
            if agent == 1:
                return None, result() * sys.maxsize
            else:
               return None, -result() * sys.maxsize

        if depth == 0:
            return None, heuristic(agent)


        # if(time.time() - start > time_for_move * 0.5):
        #     print(f"time ended", file=sys.stderr)
        #     return None, heuristic(agent)

        ms = moves(player)

        if not ms:
            rev = do_move(None, player)
            res = minimax(depth-1, not maximizingPlayer, 1 - player, alpha, beta)
            last_step_back(rev)
            return res

        if maximizingPlayer:
            maxEval = -sys.maxsize
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
            minEval = sys.maxsize
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

    x = len(move_list)**3 // 15000 + 1
    return minimax(x, True, agent, -sys.maxsize, sys.maxsize)[0]

def send_message(message):
    sys.stdout.flush()
    sys.stdout.write(message + "\n")
    # print(message)
    sys.stdout.flush()

def handle_ugo(player, time_for_move):
    start = time.time()
    move = my_agent_minmax(player, start, time_for_move)
    do_move(move, player)
    return move

def handle_hedid(command, player):
    # print(f"{command[0]} {command[1]}", file=sys.stderr)
    move = int(command[3]), int(command[2])
    if move[0] == -1 and move[1] == -1:
        do_move(None, player)
    else:
        do_move(move, player)
    return handle_ugo(1 - player, float(command[0]))

def main():
    agent = 1
    reset_game()
    send_message("RDY")
    x = 0
    while True:
        # command = sys.stdin.readline().strip().split(" ")
        command = input().split()
        if command[0] == "UGO":
            agent = 1 - agent
            move = handle_ugo(agent, float(command[1]))
            if move:
                send_message(f"IDO {move[1]} {move[0]}")
            else:
                send_message(f"IDO -1 -1")

        elif command[0] == "HEDID":
            move = handle_hedid(command[1:], 1 - agent)
            if move:
                send_message(f"IDO {move[1]} {move[0]}")
            else:
                send_message(f"IDO -1 -1")


        elif command[0] == "ONEMORE":
            reset_game()
            agent = 1
            # time.sleep(2)
            send_message("RDY")
            x += 1
            # print("loool patryk to debil", file=sys.stderr)
            # print_grid()

        else:#elif command[0] == "BYE":
            print("Matches played:", x, file=sys.stderr)
            return
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("An error occurred:", e, file=sys.stderr)
