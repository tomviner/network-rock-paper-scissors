"""
Play with trust:

for player in game:
    if current player:
        send move
    else:
        listen for move
        receive move
decide winner
"""
from __future__ import unicode_literals, print_function
import sys

import networkzero as nw0
from netrps.rps import RPS, decide_winner


def play_first(my_move_char):
    my_move = RPS(my_move_char)

    moves = []
    # discover
    my_address = nw0.discover('RPS')
    # send my move, and get their move back
    their_move = RPS(
        nw0.send_message_to(my_address, my_move_char)
    )

    moves.append(their_move)
    moves.append(my_move)

    print('I play', my_move)
    print('They play', their_move)
    return decide_winner(moves)


def play_second(my_move_char):
    my_move = RPS(my_move_char)

    moves = []
    # advertise
    my_address = nw0.advertise("RPS")
    # receive their move
    their_move = RPS(
        nw0.wait_for_message_from(my_address)
    )
    # reply with my move
    nw0.send_reply_to(my_address, my_move_char)

    moves.append(my_move)
    moves.append(their_move)

    print('I play', my_move)
    print('They play', their_move)
    return decide_winner(moves)


def main():
    args = sys.argv[1:]
    if not args or len(args) != 2:
        print('Usage: netrps <player num: 1/2> <move: r/p/s>')
    else:
        player_num, move_char = args
        if player_num == '1':
            print(play_second(move_char))
        elif player_num == '2':
            print(play_first(move_char))
        else:
            print("player num must be 1 or 2, not {!r}".format(player_num))

if __name__ == '__main__':
    main()
