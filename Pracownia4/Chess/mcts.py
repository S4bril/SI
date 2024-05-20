import sys
import math
import copy
import random
import chess

C = 1.0

board = chess.Board()

def reset_board():
    global board
    board = chess.Board()

def number_of_moves():
    return len(board.move_stack)

class Node:

    def __init__(self, end, parent, move, player):
        self.children = None
        self.rollouts_sum = 0
        self.visit_count = 0
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
        legal_moves = board.legal_moves
        # if legal_moves:
        for m in legal_moves:
            # new_game = self.game.copy()
            # new_game.push(m)
            board.push(m)
            children[m] = Node(board.is_game_over(), self, m, self.player)
            board.pop()

        self.children = children

    def explore(self):
        curr = self

        iterations = 0
        while curr.children:

            children = curr.children
            max_node_score = max(c.nodeScore() for c in children.values())
            actions = [a for a, c in children.items() if c.nodeScore() == max_node_score]
            if len(actions) == 0:
                print("error zero length ", max_node_score)
            move = random.choice(actions)
            board.push(move)
            curr = children[move]
            iterations += 1

        # play a random game, or expand if needed

        if curr.visit_count < 1:
            curr.rollouts_sum += curr.rollout()
        else:
            curr.create_children()
            if curr.children:
                curr = random.choice(list(curr.children.values()))
                board.push(curr.move)
                curr.rollouts_sum += curr.rollout()
                board.pop()
            else:
                curr.rollouts_sum += curr.rollout()

        curr.visit_count += 1

        # update statistics and backpropagate

        parent = curr

        while parent.parent:
            parent = parent.parent
            parent.visit_count += 1
            parent.rollouts_sum += curr.rollouts_sum

        for i in range(iterations):
            board.pop()

    def rollout(self):

        if self.end:
            return 0

        v = 0
        # new_game = copy.deepcopy(self.game)
        i = 0
        # while not board.is_game_over():
        for i in range(20):
            if board.is_game_over():
                break
            move = random.choice(list(board.legal_moves))
            board.push(move)
            v += Node.heuristic(board, self.player)
            i += 1
        for j in range(i):
            board.pop()
        # print(v, file=sys.stderr)
        return v


    def next(self):

        if self.end:
            raise ValueError("game has ended")

        if not self.children:
            raise ValueError('no children found and game hasn\'t ended')

        children = self.children

        max_visit_count = max(node.visit_count for node in children.values())

        max_children = [c for a, c in children.items() if c.visit_count == max_visit_count]

        max_child = random.choice(max_children)

        max_child.parent = None

        board.push(max_child.move)

        return max_child, max_child.move.uci()

    def next_opponent(self, move):
        if self.end:
            raise ValueError("game has ended")

        # if not self.children and self.move == -1:
        #     self.create_children()

        if not self.children:
            self.create_children()
            # raise ValueError('no children found and game hasn\'t ended')

        children = self.children

        for mv in list(children.keys()):
            if mv.uci() == move:
                children[mv].parent = None
                board.push(mv)
                return children[mv]

        raise ValueError("Opponent can't find a move")

    @staticmethod
    def heuristic(game: chess.Board, player):
        # check mate
        if board.is_checkmate():
            if board.turn == player:
                return -10000
            return 10000


        # material balance
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9
        }

        m = 0

        for square in chess.SQUARES:
            piece = game.piece_at(square)
            if piece:
                value = piece_values.get(piece.piece_type, 0)
                if piece.color == player:
                    m += value
                else:
                    m -= value

        # Piece activity
        a = 0
        if board.legal_moves:
            for move in board.legal_moves:
                if board.color_at(move.from_square) == player:
                    a += 1
                else:
                    a -= 1

        # Pawn structure (basic evaluation)
        # for square in chess.SQUARES:
        #     piece = board.piece_at(square)
        #     if piece and piece.piece_type == chess.PAWN:
        #         if piece.color == chess.WHITE:
        #             if not board.is_attacked_by(chess.BLACK, square):
        #                 score += 10  # Safe pawn
        #             if board.is_passed_pawn(square):
        #                 score += 20  # Passed pawn
        #         else:
        #             if not board.is_attacked_by(chess.WHITE, square):
        #                 score -= 10  # Safe pawn
        #             if board.is_passed_pawn(square):
        #                 score -= 20  # Passed pawn


        return m + 0.5*a

