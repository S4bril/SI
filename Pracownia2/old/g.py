from contextlib import redirect_stdout
from collections import deque
import heapq

board = []
dist = {}
allpos = set()

X = [-1, 0, 1, 0]
Y = [0, -1, 0, 1]
L = ["U", "L", "D", "R"]


def won(Fin, Kom):
    for k in Kom:
        if k not in Fin:
            return False
    return True


def shortest_paths(pos):
    q = deque()
    dist[pos] = 1e9
    vis = {}
    vis[pos] = True
    q.append((pos, 0))

    while len(q) > 0:
        position = q.popleft()
        P = position[0]
        D = position[1]

        if P in finish:
            dist[pos] = min(dist[pos], D)

        for i in range(4):
            if board[P[0] + X[i]][P[1] + Y[i]] != "#" and (P[0] + X[i], P[1] + Y[i]) not in vis:
                vis[(P[0] + X[i], P[1] + Y[i])] = True
                q.append(((P[0] + X[i], P[1] + Y[i]), D + 1))


def heura(positions, moves):
    distances = [dist[pos] for pos in positions]
    return max(distances) + moves


def Astar(K, M):
    Q = []
    heapq.heappush(Q, (heura(K, 0), K, M))
    allpos.add(tuple(K))

    while len(Q) > 0:
        pos = heapq.heappop(Q)
        K = pos[1]
        moves = pos[2]
        if won(finish, K):
            return moves

        for i in range(4):
            temp_pos = []
            for k in K:
                temp = list(k)
                if board[temp[0] + X[i]][temp[1] + Y[i]] != "#":
                    temp[0] = temp[0] + X[i]
                    temp[1] = temp[1] + Y[i]
                temp_pos.append(tuple(temp))

            temp_pos = sorted(list(set(temp_pos)))
            hasz = tuple(temp_pos)
            if hasz not in allpos:
                allpos.add(hasz)
                heapq.heappush(Q, (heura(temp_pos, len(moves) + 1), temp_pos, moves + L[i]))


# wczytaj planszę
with open('../zad_input.txt') as f:
    for line in f:
        board.append(list(line.strip()))

n, m = len(board) - 1, len(board[0])

komando, finish = [], set()
# znajdz pozycje
for i in range(n):
    for j in range(m):
        if board[i][j] == 'G':
            finish.add((i, j))
        if board[i][j] == 'S':
            komando.append((i, j))
        if board[i][j] == 'B':
            finish.add((i, j))
            komando.append((i, j))
        if board[i][j] != '#':
            board[i][j] = '.'

# znajdź najkrótsze ścieżki
for i in range(n):
    for j in range(m):
        if board[i][j] != "#":
            shortest_paths((i, j))

M = Astar(komando, "")
with open('../zad_output.txt', 'w') as f:
    ans = ""
    with redirect_stdout(f):
        for i in M:
            ans += i
        print(ans)