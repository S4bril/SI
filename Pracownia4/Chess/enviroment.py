import random
import sys
import chess
import chess.engine

class Game:

    def __init__(self, player):
        self.player = player
        self.board = chess.Board()

    def legal_moves(self):
        return self.board.legal_moves

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
        return (self.board.is_checkmate()
                or self.board.is_stalemate()
                or self.board.is_insufficient_material())

    def do_move(self, move):
        self.board.push(move)

    def undo_move(self):
        return self.board.pop()

    def random_move(self):
        ms = self.moves()
        if ms:
            return random.choice(ms)
        return None

    def heuristic(self):
        w = 0
        coins_player = 0
        coins_opponent = 0
        for i in range(M):
            for j in range(M):
                if self.get(i, j) == self.player:
                    w += WEIGHTS[i][j]
                    coins_player += 1
                elif self.get(i, j) == 1 - self.player:
                    w -= WEIGHTS[i][j]
                    coins_opponent += 1
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