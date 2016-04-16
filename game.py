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
from rps import RPS, get_local_move, decide_winner

def play_round():
    moves = []
    for player in range(1, 3):
        print('player {}, enter your move:'.format(player))
        moves.append(get_local_move())
    return decide_winner(moves)

def play(n, my_move_char):
    n = int(n)

    moves = []
    if n == 1:
        # advertise
        my_address = nw0.advertise("RPS")
        # receive their move
        their_move = nw0.wait_for_message(my_address)
        # reply with my move
        nw0.send_reply(my_address, my_move_char)

        moves.append(RPS(my_move_char))
        moves.append(RPS(their_move))
    else:
        # discover
        my_address = nw0.discover('RPS')
        # send my move, and get their move back
        their_move = nw0.send_message(my_address, my_move_char)

        moves.append(RPS(their_move))
        moves.append(RPS(my_move_char))

    print('I play', RPS(my_move_char))
    print('They play', RPS(their_move))
    return decide_winner(moves)

if __name__ == '__main__':
    print(play(*sys.argv[1:]))
