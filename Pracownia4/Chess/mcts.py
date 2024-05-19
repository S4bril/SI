import sys
import math
import copy
import random
import chess

C = 1.5

class Node:

    def __init__(self, game: chess.Board, end, parent, move, player):
        self.children = None
        self.rollouts_sum = 0
        self.visit_count = 0
        self.game = game
        self.end = end
        self.parent = parent
        self.move = move
        self.player = player

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

        children = {}
        legal_moves = self.game.legal_moves
        # if legal_moves:
        for m in legal_moves:
            new_game = copy.deepcopy(self.game)
            new_game.push(m)
            children[m] = Node(new_game, new_game.is_game_over(), self, m, self.player)

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
        while not new_game.is_game_over():
            move = random.choice(list(new_game.legal_moves))
            new_game.push(move)
            v += Node.heuristic(new_game, self.player)
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

        return max_child, max_child.move.uci()

    def next_opponent(self, move):
        if self.end:
            raise ValueError("game has ended")

        # if not self.children and self.move == -1:
        #         self.create_children()

        if not self.children:
            self.create_children()
            # raise ValueError('no children found and game hasn\'t ended')

        children = self.children

        for mv in list(children.keys()):
            if mv.uci() == move:
                children[mv].parent = None
                return children[mv]

        # print(move, self.children.keys(), file=sys.stderr)
        # print(move in self.children.keys(), file=sys.stderr)

        raise ValueError("Opponent can't find a move")

    @staticmethod
    def heuristic(game: chess.Board, player: int):
        return 0

        # piece_values = {
        #     chess.PAWN: 1,
        #     chess.KNIGHT: 3,
        #     chess.BISHOP: 3,
        #     chess.ROOK: 5,
        #     chess.QUEEN: 9
        # }
        #
        # white_material = 0
        # black_material = 0
        #
        # for square in chess.SQUARES:
        #     piece = game.piece_at(square)
        #     if piece:
        #         value = piece_values.get(piece.piece_type, 0)
        #         if piece.color == chess.WHITE:
        #             white_material += value
        #         else:
        #             black_material += value
        # if player == 0:
        #     return white_material - black_material
        #
        # return black_material - white_material