from queue import Queue
import argparse
def refactor_data(data):
    return [data[0], int(data[1])]

def show_move(c, k_w, t_w, k_b):
    print(c)
    print(k_w)
    print(t_w)
    print(k_b)

def valid_pos(x, y):
    return (x >= 'a' and x <= 'h') and (y >= 1 and y <= 8)

def is_check(black_king, white_tower):
    return black_king[0] == white_tower[0] or black_king[1] == white_tower[1]

def are_colliding(king1, king2):
    diff1 = abs(ord(king1[0]) - ord(king2[0]))
    diff2 = abs(int(king1[1]) - int(king2[1]))
    return diff1 <= 1 and diff2 <= 1

def possible_black_king_moves(k_w, t_w, k_b):
    result = []
    moves = [[1, 1], [1, 0], [0, 1], [-1, -1], [-1, 0], [0, -1], [-1, 1], [1, -1]]
    for move in moves:
        new_move = [chr(ord(k_b[0]) + move[0]), k_b[1] + move[1]]
        # czy pole jest szachowane lub poza planszą
        if is_check(new_move, t_w) or not valid_pos(new_move[0], new_move[1]):
            continue
        # czy pole nie jest szachowane przez króla
        if are_colliding(new_move, k_w):
            continue
        result.append(new_move)
    return result

def possible_white_king_moves(k_w, t_w, k_b):
    result = []
    moves = [[1, 1], [1, 0], [0, 1], [-1, -1], [-1, 0], [0, -1], [-1, 1], [1, -1]]
    for move in moves:
        new_move = [chr(ord(k_w[0]) + move[0]), k_w[1] + move[1]]
        if not valid_pos(new_move[0], new_move[1]) or (new_move[0] == t_w[0] and new_move[1] == t_w[1]):
            continue
        if are_colliding(k_b, new_move):
            continue
        result.append(new_move)
    return result

def possible_white_tower_moves(k_w, t_w, k_b):
    result = []
    directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    for move in directions:
        i = 1
        while(True):
            new_move = [chr(ord(t_w[0]) + i * move[0]), t_w[1] + i * move[1]]
            # czy nie wychodzi za planszę
            if not valid_pos(new_move[0], new_move[1]):
                break
            # czy nie blokuje go biały król
            if new_move[0] == k_w[0] and new_move[1] == k_w[1]:
                break
            # czy nie blokuje go czarny król
            if new_move[0] == k_b[0] and new_move[1] == k_b[1]:
                break
            # dodaj ruch do wyniku
            result.append(new_move)
            i += 1
    return result

def check_if_black_king_kills_tower(k_w, t_w, k_b):
    return not are_colliding(k_w, t_w) and are_colliding(k_b, t_w)

def state_to_string(k_w, t_w, k_b):
    return k_w[0] + str(k_w[1]) + t_w[0] + str(t_w[1]) + k_b[0] + str(k_b[1])
def bfs(c, k_w, t_w, k_b):
    queue = Queue()
    queue.put([[0, c, k_w, t_w, k_b]])
    visited = {state_to_string(k_w, t_w, k_b)}
    while not queue.empty():
        state = queue.get()
        #print(state)
        moves, c, k_w, t_w, k_b = state[0]
        #-------------------black king---------------------
        if c == 'black':
            black = possible_black_king_moves(k_w, t_w, k_b)
            for pos in black:
                if state_to_string(k_w, t_w, pos) not in visited:
                    new_state = state[:]
                    new_state.insert(0, [moves + 1, 'white', k_w, t_w, pos])
                    queue.put(new_state)
                    visited.add(state_to_string(k_w, t_w, pos))
        else:
            # -------------------white tower---------------------
            tower = possible_white_tower_moves(k_w, t_w, k_b)
            for pos in tower:
                black = possible_black_king_moves(k_w, pos, k_b)
                if len(black) > 0:
                    if state_to_string(k_w, pos, k_b) not in visited:
                        new_state = state[:]
                        new_state.insert(0, [moves + 1, 'black', k_w, pos, k_b])
                        queue.put(new_state)
                        visited.add(state_to_string(k_w, pos, k_b))
                elif check_if_black_king_kills_tower(k_w, pos, k_b):
                    continue
                else:
                    state.insert(0, [moves + 1, 'black', k_w, pos, k_b])
                    #print("halo", state)
                    return state
            # -------------------white king---------------------
            king = possible_white_king_moves(k_w, t_w, k_b)
            for pos in king:
                black = possible_black_king_moves(pos, t_w, k_b)
                if len(black) > 0:
                    if state_to_string(pos, t_w, k_b) not in visited:
                        new_state = state[:]
                        new_state.insert(0, [moves + 1, 'black', pos, t_w, k_b])
                        queue.put(new_state)
                        visited.add(state_to_string(pos, t_w, k_b))
                    continue
                elif check_if_black_king_kills_tower(pos, t_w, k_b):
                    continue
                else:
                    state.insert(0, [moves + 1, 'black', pos, t_w, k_b])
                    #print("halo", state)
                    return state
    return "INF"

# Inicjalizacja parsera
parser = argparse.ArgumentParser(description="Program do obliczania minimalnej ilości ruchów do mata kooperacyjnego.")

# Dodanie argumentów
parser.add_argument('--debug', action='store_true', help='Włącz tryb debugowania')

# Parsowanie argumentów
args = parser.parse_args()

# Dostęp do argumentów

if args.debug:
    print("Tryb debugowania jest włączony.")

with open("zad1_input.txt", 'r') as file_in, open("zad1_output.txt", 'w') as file_out:
    lines = file_in.readlines()
    for i in range(0, len(lines)):
        data = lines[i].split(" ")
        color = data[0]
        white_king_pos = refactor_data(data[1])
        white_tower_pos = refactor_data(data[2])
        black_king_pos = refactor_data(data[3])
        result = bfs(color, white_king_pos, white_tower_pos, black_king_pos)
        if result == "INF":
            file_out.write("INF")
        else:
            file_out.write(str(result[0][0]))
        if args.debug:
            print(result)