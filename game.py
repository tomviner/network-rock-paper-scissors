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

def play(n, my_name, move_char):
    n = int(n)

    if n == 1:
        my_address = nw0.advertise("RPS")
        print('player 1 advertising from', my_address)
        # print('player 2 ready?')
        # msg = nw0.wait_for_message(my_address)
        # print('GOT', msg)
        # reply = 'player 1 ready too'
        # print('Replying', reply)
        # nw0.send_reply(my_address, reply)
    else:
        print('player 2 want to discover RPS')
        my_address = nw0.discover('RPS', wait_for_s=60)
        print('discovered', my_address)
        # msg = 'player 2 ready'
        # print('send', msg)
        # reply = nw0.send_message(my_address, msg)
        # print('got reply', reply)

    print(nw0.discover_all())
    # while not get_services(my_name):
    #     print('.', end='', flush=True)
    #     time.sleep(1)
    # print()

    moves = []
    # for player in range(1, 3):
    #     print('player {}, enter your move:'.format(player))
    #     moves.append(get_local_move())

    topic = "player {} move".format(n)
    if n == 2:
        # send
        print(topic, 'send', move_char, my_address)
        reply = nw0.send_message(my_address, move_char)
        print('got reply', reply)
        moves.append(RPS(reply))
        moves.append(RPS(move_char))
    else:
        moves.append(RPS(move_char))
        # receive
        print('receiving', my_address)
        msg = nw0.wait_for_message(my_address)
        moves.append(RPS(msg))
        print('received', msg)
        nw0.send_reply(my_address, move_char)
    # while True:

    #     for name, address in services:
    #         topic, message = nw0.wait_for_notification(
    #             address, "quote", wait_for_s=0)
    #         if topic:
    print('moves', moves)
    return decide_winner(moves)

if __name__ == '__main__':
    print(play(*sys.argv[1:]))
