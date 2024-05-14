import sys
import math
import copy
from enviroment import Game

C = 1
class Node:

    def __init__(self, game: Game, ended, parent, heuristic_value, move):
        self.children = None
        self.rollouts_sum = 0
        self.visit_count = 0
        self.game = game
        self.heuristic_value = heuristic_value
        self.ended = ended
        self.parent = parent
        self.move = move

    def getUCBscore(self):
        if self.rollouts_sum == 0:
            return sys.maxsize

        if self.parent:
            return ((self.rollouts_sum / self.visit_count)
                    + C * math.sqrt(math.log(self.parent.visit_count) / self.visit_count))

        return ((self.rollouts_sum / self.visit_count)
                + C * math.sqrt(math.log(self.visit_count) / self.visit_count))

    def create_children(self):

        if self.ended:
            return

        games = []
        moves = self.game.moves()
        for m in moves:
            new_game = copy.deepcopy(self.game)
            new_game.do_move(m)
            games.append(new_game)

        children = {}
        for m, g in zip(moves, games):
            children[m] = Node(g, g.terminal(), self, g.heuristics(), m)

        self.children = children
