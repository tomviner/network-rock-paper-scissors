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
import sys

import networkzero as nw0
from netrps.rps import RPS, decide_winner


def play(n, my_move_char):
    n = int(n)
    my_move = RPS(my_move_char)

    moves = []
    if n == 1:
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
    else:
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

if __name__ == '__main__':
    print(play(*sys.argv[1:]))
