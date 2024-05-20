import time
import sys
from mcts import Node, reset_board, number_of_moves
import chess

MCTS_POLICY_EXPLORE = 5

class MainGame:
    def __init__(self, player):
        self.tree = Node(
            end=False,
            parent=None,
            move=-1,
            player=player
        )
        reset_board()
        self.lol = 2

    def change_player(self):
        if self.tree.player == chess.WHITE:
            self.tree.player = chess.BLACK
        else:
            self.tree.player = chess.WHITE

    def mcts(self):
        start_time = time.time()
        for i in range(self.lol):#MCTS_POLICY_EXPLORE + number_of_moves()**2//1000):
            self.tree.explore()
        end_time = time.time()
        elapsed_time = end_time - start_time
        if elapsed_time > 0.5:
            if self.lol > 2:
                self.lol -= 1
        else:
            self.lol += 1
        # print("Elapsed time:", elapsed_time, "seconds", file=sys.stderr)

    def send_message(self, message):
        sys.stdout.flush()
        sys.stdout.write(message + "\n")
        sys.stdout.flush()

    def handle_ugo(self):
        self.mcts()
        root, move = self.tree.next()
        self.tree = root
        return move

    def handle_hedid(self, command):
        # print(f"{command[0]} {command[1]}", file=sys.stderr)
        move = command[2]
        self.tree = self.tree.next_opponent(move)
        return self.handle_ugo()

def main():
    game = MainGame(player=chess.BLACK)
    game.send_message("RDY")
    while True:
        command = input().split()
        if command[0] == "UGO":
            game.change_player()
            move = game.handle_ugo()
            game.send_message(f"IDO {move}")

        elif command[0] == "HEDID":
            move = game.handle_hedid(command[1:])
            game.send_message(f"IDO {move}")


        elif command[0] == "ONEMORE":
            game = MainGame(player=chess.BLACK)
            game.send_message("RDY")

        else:
            return

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("An error occurred:", e, file=sys.stderr)
