import random
import sys

M = 8
DIRECTIONS = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
WEIGHTS = [
    [50, -20, 15,  8,  8, 15, -20, 50],
    [-20, -50, -4,  1,  1, -4, -50, -20],
    [15, -4,  2,  2,  2,  2, -4, 15],
    [ 8,  1,  2, -3, -3,  2,  1,  8],
    [ 8,  1,  2, -3, -3,  2,  1,  8],
    [15, -4,  2,  2,  2,  2, -4, 15],
    [-20, -50, -4,  1,  1, -4, -50, -20],
    [50, -20, 15,  8,  8, 15, -20, 50]
]

# def undo(rev):
#     global grid, fields, move_list
#
#     move = move_list.pop()
#
#     if move:
#         fields.add(move)
#         grid[move[0]][move[1]] = None
#
#         for cell in rev:
#             grid[cell[0]][cell[1]] = 1 - grid[cell[0]][cell[1]]


class Game:

    def __init__(self, player):
        self.player = player
        self.init_game()

    def init_game(self):
        self.curr_player = 0
        self.move_list = []
        self.grid = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None,  1,    0,   None, None, None],
            [None, None, None,  0,    1,   None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
        ]
        self.fields = {
            (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
            (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7),
            (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7),
            (3, 0), (3, 1), (3, 2),                 (3, 5), (3, 6), (3, 7),
            (4, 0), (4, 1), (4, 2),                 (4, 5), (4, 6), (4, 7),
            (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7),
            (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7),
            (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7),
        }

    def get(self, x, y):
        if 0 <= x < M and 0 <= y < M:
            return self.grid[x][y]
        return None

    def can_beat(self, x, y, d):
        dx, dy = d
        x += dx
        y += dy
        cnt = 0
        while self.get(x, y) == 1 - self.curr_player:
            x += dx
            y += dy
            cnt += 1
        return cnt > 0 and self.get(x, y) == self.curr_player


    def moves(self):
        res = []
        for (x, y) in self.fields:
            if any(self.can_beat(x, y, direction) for direction in DIRECTIONS):
                res.append((x, y))
        if not res:
            return None
        return res

    def result(self):
        res = 0
        for x in range(M):
            for y in range(M):
                b = self.get(x, y)
                if b == 0:
                    res -= 1
                elif b == 1:
                    res += 1
        return res

    def terminal(self):
        if not self.fields:
            return True
        if len(self.move_list) < 2:
            return False
        return self.move_list[-1] == self.move_list[-2] == None

    def do_move(self, move):
        self.move_list.append(move)

        if move == None:
            self.cur_player = 1 - self.curr_player
            return []

        x, y = move
        x0, y0 = move
        self.grid[x][y] = self.curr_player
        self.fields -= set([move])
        reversed_cells = []
        for dx, dy in DIRECTIONS:
            x, y = x0, y0
            to_beat = []
            x += dx
            y += dy
            while self.get(x, y) == 1 - self.curr_player:
                to_beat.append((x, y))
                x += dx
                y += dy
            if self.get(x, y) == self.curr_player:
                for (nx, ny) in to_beat:
                    self.grid[nx][ny] = self.curr_player
                    reversed_cells.append((nx, ny))
        self.cur_player = 1 - self.curr_player
        return reversed_cells

    def random_move(self):
        ms = self.moves()
        if ms:
            return random.choice(ms)
        return None

    def heuristic(self):
        weights_player = 0
        weights_opponent = 0
        coins_player = 0
        coins_opponent = 0
        for i in range(M):
            for j in range(M):
                if self.get(i, j) == self.player:
                    weights_player += WEIGHTS[i][j]
                    coins_player += 1
                elif self.get(i, j) == 1 - self.player:
                    weights_opponent += WEIGHTS[i][j]
                    coins_opponent += 1
        w = (weights_player - weights_opponent)
        return w #+ 5 * mobility(player)

    def print_grid(self):
        print("  ", end="", file=sys.stderr)
        for col_idx in range(len(self.grid[0])):
            print(f"{col_idx:2}", end="", file=sys.stderr)
        print("\n   ---------------", file=sys.stderr)
        for row_idx, row in enumerate(self.grid):
            print(f"{row_idx:2}|", end="", file=sys.stderr)
            for cell in row:
                if cell is None:
                    print(" ", end=" ", file=sys.stderr)  # Print empty cell
                else:
                    print(cell, end=" ", file=sys.stderr)  # Print cell value
            print(file=sys.stderr)
        print(file=sys.stderr)