import time
import sys
from datetime import datetime

def send_message(message):
    sys.stdout.flush()
    sys.stdout.write(message + "\n")
    # print(message)
    sys.stdout.flush()

def handle_ugo(player, time_for_move):
    start = time.time()
    move = my_agent_minmax(player, start, time_for_move)
    do_move(move, player)
    return move

def handle_hedid(command, player):
    # print(f"{command[0]} {command[1]}", file=sys.stderr)
    move = int(command[3]), int(command[2])
    if move[0] == -1 and move[1] == -1:
        do_move(None, player)
    else:
        do_move(move, player)
    return handle_ugo(1 - player, float(command[0]))

def main():
    agent = 1
    reset_game()
    send_message("RDY")
    x = 0
    while True:
        # command = sys.stdin.readline().strip().split(" ")
        command = input().split()
        if command[0] == "UGO":
            agent = 1 - agent
            move = handle_ugo(agent, float(command[1]))
            if move:
                send_message(f"IDO {move[1]} {move[0]}")
            else:
                send_message(f"IDO -1 -1")

        elif command[0] == "HEDID":
            move = handle_hedid(command[1:], 1 - agent)
            if move:
                send_message(f"IDO {move[1]} {move[0]}")
            else:
                send_message(f"IDO -1 -1")


        elif command[0] == "ONEMORE":
            reset_game()
            agent = 1
            # time.sleep(2)
            send_message("RDY")
            x += 1
            # print("loool patryk to debil", file=sys.stderr)
            # print_grid()

        else:#elif command[0] == "BYE":
            print("Matches played:", x, file=sys.stderr)
            return
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("An error occurred:", e, file=sys.stderr)
