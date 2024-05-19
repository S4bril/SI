import time
import sys
from mcts import Node
import chess

MCTS_POLICY_EXPLORE = 10

class MainGame:
    def __init__(self, player):
        self.tree = Node(
            game=chess.Board(),
            end=False,
            parent=None,
            move=-1,
            player=player
        )

    def change_player(self):
        self.tree.player = 1 - self.tree.player

    def mcts(self):
        # start_time = time.time()
        for i in range(MCTS_POLICY_EXPLORE):# + len(self.tree.game.move_stack)**2):
            self.tree.explore()
        # end_time = time.time()
        # elapsed_time = end_time - start_time
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
    game = MainGame(player=1)
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
            game = MainGame(player=1)
            game.send_message("RDY")

        else:
            return

if __name__ == '__main__':
    main()
    try:
        main()
    except Exception as e:
        print("An error occurred:", e, file=sys.stderr)
