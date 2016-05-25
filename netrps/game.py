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
import random

import click
import six

import networkzero as nw0
from netrps.rps import RPS, decide_winner, get_local_move


def play_first(choose_move):
    moves = []
    # discover
    my_address = nw0.discover('RPS')
    if isinstance(choose_move, six.string_types):
        my_move = RPS(choose_move)
    else:
        # we don't know their move yet!
        my_move = choose_move(their_move=None)
    # send my move, and get their move back
    their_move = RPS(
        nw0.send_message_to(my_address, my_move.char)
    )

    moves.append(my_move)
    moves.append(their_move)

    print('I play', my_move)
    print('They play', their_move)
    return decide_winner(moves)


def play_second(choose_move):
    moves = []
    # advertise
    my_address = nw0.advertise("RPS")
    # receive their move
    their_move = RPS(
        nw0.wait_for_message_from(my_address)
    )
    # reply with my move
    if isinstance(choose_move, type('')):
        my_move = RPS(choose_move)
    else:
        my_move = choose_move(their_move)
    nw0.send_reply_to(my_address, my_move.char)

    my_move = RPS(my_move.char)
    moves.append(their_move)
    moves.append(my_move)

    print('I play', my_move)
    print('They play', their_move)
    return decide_winner(moves)

class Strategies:
    @staticmethod
    def interactive(their_move):
        move = get_local_move('Their move was {}. > '.format(their_move))
        return move

    @staticmethod
    def auto_cheat(their_move):
        move = {'r': 'p', 'p': 's', 's': 'r'}[their_move.char]
        return RPS(move)

    @staticmethod
    def random(their_move):
        move = random.choice('rps')
        return RPS(move)

@click.command()
@click.argument('move', type=click.Choice('rps'), required=False)
@click.option('--random/--no-random', 'rnd')
def player_one(move, rnd):
    """Usage: player_one [OPTIONS] [MOVE]

    Options:
      --random / --no-random
      --help                  Show this message and exit.
    """
    if rnd:
        move = Strategies.random
    print(play_first(move))

@click.command()
@click.argument('move', type=click.Choice('rps'), required=False)
@click.option('--random/--no-random', 'rnd')
@click.option('--interactive/--no-interactive')
@click.option('--auto-cheat/--no-auto-cheat')
def player_two(move, rnd, interactive, auto_cheat):
    """Usage: player_two [OPTIONS] [MOVE]

    Options:
      --random / --no-random
      --interactive / --no-interactive
      --auto-cheat / --no-auto-cheat
      --help                          Show this message and exit.
    """
    if rnd:
        move = Strategies.random
    elif interactive:
        move = Strategies.interactive
    elif auto_cheat:
        move = Strategies.auto_cheat
    elif not move:
        move = Strategies.interactive
    print(play_second(move))
