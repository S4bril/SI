import string
from queue import PriorityQueue
from queue import Queue

class InvalidDirectionException(Exception):
    def __init__(self, function_name, direction):
        print(function_name + ": " + direction + " is not a valid direction")

WIDTH = 0
HEIGHT = 0

dist = {}

def load_data(path="zad_input.txt"):
    global WIDTH, HEIGHT
    with open(path) as f:
        lines = f.readlines()
        board = [line.strip() for line in lines]
        WIDTH = len(board[0])
        HEIGHT = len(board)
    return board

def get_commanders_positions(board):
    res = []
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if board[i][j] == 'S' or board[i][j] == 'B':
                res.append((i, j))
    return res

def get_goals_positions(board):
    res = []
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if board[i][j] == 'G' or board[i][j] == 'B':
                res.append((i, j))
    return res
def bfs(board, start_node, goals):
    q = Queue()
    visited_states = set()
    q.put(start_node)
    visited_states.add(start_node[0])
    while not q.empty():
        pos, moves = q.get()
        if check_mission([pos], goals):
            return moves
        for direction in "LRUD":
            next_pos = move(board, pos, direction)
            next_path = moves + 1
            my_hash = tuple(next_pos)
            if my_hash not in visited_states:
                q.put((next_pos, next_path))
                visited_states.add(my_hash)
    return None
def compute_distances(board, goals):
    # def distance(p1, p2):
    #     return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    # for i in range(HEIGHT):
    #     for j in range(WIDTH):
    #         if board[i][j] != '#':
    #             dist[(i, j)] = min([distance((i, j), goal) for goal in goals])
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if board[i][j] != '#':
                dist[(i, j)] = bfs(board, ((i, j), 0), goals)
    #print(dist)

def check_mission(commanders, goals):
    for commander in commanders:
        if commander not in goals:
            return False
    return True

def move(board, position, direction: string):
    x = position[0]
    y = position[1]
    match direction:
        case "U":
            if board[x-1][y] != '#':
                return x-1, y
        case "D":
            if board[x+1][y] != '#':
                return x+1, y
        case "L":
            if board[x][y-1] != '#':
                return x, y-1
        case "R":
            if board[x][y+1] != '#':
                return x, y+1
        case _:
            raise InvalidDirectionException("move", direction)
    return position

def heuristic(state, scale):
    positions, path = state
    res = 0
    # for pos in positions:
    #     res += min([distance(pos, goal) for goal in goals])
    return max([dist[pos] for pos in positions])*scale + len(path)

def A_star(board, start_node, goals, scale):
    pq = PriorityQueue()
    visited_states = set()
    pq.put((heuristic(start_node, scale), start_node))
    visited_states.add(tuple(sorted(start_node[0])))
    while not pq.empty():
        _, node = pq.get()
        pos, path = node
        if len(path) == 3:
            pass
        if check_mission(pos, goals):
            return path
        for direction in "LRUD":
            next_pos = [move(board, p, direction) for p in pos]
            next_pos = sorted(list(set(next_pos)))
            next_path = path + direction
            my_hash = tuple(next_pos)
            if my_hash not in visited_states:
                pq.put((heuristic((next_pos, next_path), scale), (next_pos, next_path)))
                visited_states.add(my_hash)
    return None

def main():
    board = load_data()
    positions = get_commanders_positions(board)
    goals = get_goals_positions(board)
    compute_distances(board, goals)
    res = A_star(board, (positions, ""), goals, 1.0)
    print(len(res))
    with open("zad_output.txt", "w") as f:
        f.write(res)

if __name__ == "__main__":
    main()
