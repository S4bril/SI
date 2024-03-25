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

    # match direction:
    #     case "U":
    #         if board[x-1][y] != '#':
    #             return x-1, y
    #     case "D":
    #         if board[x+1][y] != '#':
    #             return x+1, y
    #     case "L":
    #         if board[x][y-1] != '#':
    #             return x, y-1
    #     case "R":
    #         if board[x][y+1] != '#':
    #             return x, y+1
    #     case _:
    #         raise InvalidDirectionException("move", direction)
    # return position

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
def preprocessed_moves(positions):
    state = positions, ""
    min_commanders = len(positions)
    i = 0
    while min_commanders > 2:
        perms = list(product(['L', 'D', 'U', 'R'], repeat=4))
        state_min = state
        for perm in perms:
            lol = state[0]
            path = state[1]
            for direction in perm:
                while True:
                    # if(length > 100):
                    #     break
                    if random.randint(0, 100) >= 90:
                        break
                    new = list(set([move(p, direction) for p in lol]))
                    path += direction
                    if new == lol:
                        break
                    # length += 1
                    lol = new
                #print(lol)
            number_of_pos = len(lol)
            if number_of_pos < min_commanders:
                state_min = (lol, state[1] + path)
                min_commanders = number_of_pos
        state = state_min
        if len(state[1]) > 120:
            i += 1
            #print("lol", min_commanders, len(state[1]))
            state = (positions, "")
            min_commanders = len(positions)
    return sorted(state[0]), state[1]


def find_best_moves(positions):
    # state = random_moves(board, positions)
    characters = ['L', 'R', 'U', 'D']
    perms = list(product(characters, repeat=5))

    # perms = ['RLDU', 'LRUD', 'LDUR', 'ULRD', 'RULD', 'DULR', 'DLRU', 'DRUL', 'LRDU', 'RDLU', 'DLUR', 'UDLR', 'DURL',
    #            'LUDR', 'DRLU', 'ULDR', 'URDL', 'URLD', 'UDRL', 'RLUD', 'LURD', 'LDRU', 'RUDL', 'RDUL', 'LUDLU']

    best_len = 10000
    best_perm = ""
    for perm in perms:
        state = positions
        perm_temp = ""
        for i in range(19):
            for p in perm:
                perm_temp += p
                state = [move(pos, p) for pos in state]
        state = sorted(list(set(state)))
        length = len(state)
        if length < best_len:
            best_state = state
            best_len = length
            best_perm = perm_temp

    return best_state, "".join(best_perm)

def main():
    load_data()
    positions = get_commanders_positions()
    goals = get_goals_positions()
    #start_node = find_best_moves(positions)
    #if len(start_node[0]) > 3:
    start_node = preprocessed_moves(positions)
    #print(start_node)
    #print(start_node)
    res = bfs(start_node, goals)
    with open("zad_output.txt", "w") as f:
        f.write(res)

if __name__ == "__main__":
    main()
