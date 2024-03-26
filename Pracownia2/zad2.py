import string
from queue import Queue
from itertools import permutations
from itertools import combinations
from itertools import product
import random
board = []

dict_moves = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}

class InvalidDirectionException(Exception):
    def __init__(self, function_name, direction):
        print(function_name + ": " + direction + " is not a valid direction")

WIDTH = 0
HEIGHT = 0

def load_data(path="zad_input.txt"):
    global WIDTH, HEIGHT
    with open(path) as f:
        lines = f.readlines()
        for line in lines:
            board.append(line.strip())
        WIDTH = len(board[0])
        HEIGHT = len(board)
    return board

def get_commanders_positions():
    res = []
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if board[i][j] == 'S' or board[i][j] == 'B':
                res.append((i, j))
    return res

def get_goals_positions():
    res = []
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if board[i][j] == 'G' or board[i][j] == 'B':
                res.append((i, j))
    return res

def check_mission(commanders, goals):
    for commander in commanders:
        if commander not in goals:
            return False
    return True

def move(position, direction):
    x, y = position
    z, w = dict_moves[direction]
    r1, r2 = x + z, y + w
    if board[r1][r2] != '#':
        return r1, r2
    return position

def bfs(start_node, goals):
    q = Queue()
    visited_states = set()
    q.put(start_node)
    visited_states.add(tuple(start_node[0]))
    while not q.empty():
        pos, path = q.get()
        if check_mission(pos, goals):
            return path
        for direction in "LRUD":
            next_pos = [move(p, direction) for p in pos]
            next_pos = sorted(list(set(next_pos)))
            next_path = path + direction
            my_hash = tuple(next_pos)
            if my_hash not in visited_states:
                q.put((next_pos, next_path))
                visited_states.add(my_hash)
    return None

def preprocessing(state):
    i = 0
    new_state = (state[0], state[1])
    lol = 6
    while len(new_state[0]) > 2 and i < lol:
        new_state = preprocessed_moves(new_state)
        i += 1

    if i == lol:
        preprocessing(state)

    return new_state


def preprocessed_moves(state):
    perms = list(product(['L', 'D', 'U', 'R'], repeat=4))

    min_state = (state[0], state[1])
    min_commanders = len(state[0])
    origin_state = (state[0], state[1])
    for perm in perms:
        for direction in perm:
            no_moves = False
            while not no_moves:
                if random.randint(0, 100) >= 90:
                    break
                new_positions = list(set([move(p, direction) for p in state[0]]))
                no_moves = (new_positions == state[0])
                if not no_moves:
                    state = new_positions, state[1] + direction

        new_commanders = len(state[0])
        moves = state[1]
        if (new_commanders == min_commanders and len(moves) < len(min_state[1])) or new_commanders < min_commanders:
            if len(moves) < 120:
                min_state = (state[0], moves)
                min_commanders = new_commanders
        state = origin_state
    return min_state

def main():
    load_data()
    positions = get_commanders_positions()
    goals = get_goals_positions()
    start_node = preprocessing((positions, ""))
    res = bfs(start_node, goals)
    with open("zad_output.txt", "w") as f:
        f.write(res)
    print(len(res))

if __name__ == "__main__":
    main()
