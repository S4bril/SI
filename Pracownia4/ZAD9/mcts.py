import sys
import math
import copy
import random

from enviroment import Game

C = 1.5

class Node:

    def __init__(self, game: Game, end, parent, move):
        self.children = None
        self.rollouts_sum = 0
        self.visit_count = 0
        self.game = game
        self.end = end
        self.parent = parent
        self.move = move

    def nodeScore(self):
        if self.rollouts_sum == 0:
            return sys.maxsize

        if self.parent:
            return ((self.rollouts_sum / self.visit_count)
                    + C * math.sqrt(math.log(self.parent.visit_count) / self.visit_count))

        return ((self.rollouts_sum / self.visit_count)
                + C * math.sqrt(math.log(self.visit_count) / self.visit_count))

    def create_children(self):

        if self.end:
            return

        games = []
        children = {}
        moves = self.game.moves()
        if moves:
            for m in moves:
                new_game = copy.deepcopy(self.game)
                new_game.do_move(m)
                games.append(new_game)
            for m, g in zip(moves, games):
                children[m] = Node(g, g.terminal(), self, m)
        else:
            new_game = copy.deepcopy(self.game)
            new_game.do_move(None)
            children[None] = Node(new_game, new_game.terminal(), self, None)

        self.children = children

    def explore(self):
        curr = self

        while curr.children:

            children = curr.children
            max_node_score = max(c.nodeScore() for c in children.values())
            actions = [a for a, c in children.items() if c.nodeScore() == max_node_score]
            if len(actions) == 0:
                print("error zero length ", max_node_score)
            move = random.choice(actions)
            curr = children[move]

        # play a random game, or expand if needed

        if curr.visit_count < 1:
            curr.rollouts_sum += curr.rollout()
        else:
            curr.create_children()
            if curr.children:
                curr = random.choice(list(curr.children.values()))
            curr.rollouts_sum += curr.rollout()

        curr.visit_count += 1

        # update statistics and backpropagate

        parent = curr

        while parent.parent:
            parent = parent.parent
            parent.visit_count += 1
            parent.rollouts_sum += curr.rollouts_sum

    def rollout(self):

        if self.end:
            return 0

        v = 0
        new_game = copy.deepcopy(self.game)
        while not new_game.terminal():
            move = new_game.random_move()
            new_game.do_move(move)
            v += new_game.heuristic()
        return v


    def next(self):

        if self.end:
            raise ValueError("game has ended")

        if not self.children:
            raise ValueError('no children found and game hasn\'t ended')

        children = self.children

        max_visit_count = max(node.visit_count for node in children.values())

        max_children = [c for a, c in children.items() if c.visit_count == max_visit_count]

        if len(max_children) == 0:
            print("error zero length ", max_visit_count)

        max_child = random.choice(max_children)

        max_child.parent = None

        return max_child, max_child.move

    def next_opponent(self, move):
        if self.end:
            raise ValueError("game has ended")

        if not self.children:
            if self.move == (-1, -1):
                self.create_children()
            else:
                raise ValueError('no children found and game hasn\'t ended')

        children = self.children

        for mv in list(children.keys()):
            if mv == move:
                children[mv].parent = None
                return children[mv]

        # print(move, self.children.keys(), file=sys.stderr)
        # print(move in self.children.keys(), file=sys.stderr)

        raise ValueError("Opponent can't find a move")