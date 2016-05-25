"""
Play with trust:

for player in game:
    if current player:
        send move
    else:
        listen for move
        receive move
decide winner


Play trusting no one:

Swap hashes:
    for player in game:
        if current player:
            send hasher(move + salt)
        else:
            listen for hash
            receive hash

Swap salts:
    for player in game:
        if current player:
            send move + salt
        else:
            listen for move + salt
            receive move + salt
            verify hasher(move + salt) == hash

decide winner
"""
from __future__ import unicode_literals, print_function
import random
import hmac
import sys

import click
from clint.textui import colored

import networkzero as nw0
from netrps.rps import RPS, decide_winner, get_local_move


def make_salt():
    return random.randint(0, 999)

def make_hash(move, salt):
    mac = hmac.new(bytes(salt), move.char.encode('utf-8'))
    return mac.hexdigest()

def guess_real_move(salt, hash):
    for char in 'rps':
        move = RPS(char)
        if make_hash(move, salt) == hash:
            return move
    return '<unknown>'

def check_hash(move, salt, hash):
    expected_hash = make_hash(move, salt)
    if hash != expected_hash:
        msg = colored.red('\tCheat Detected!\n', bold=True)
        msg += '\texpected hash({}+{})=={}\n'.format(
            move, salt, expected_hash)

        real_move = guess_real_move(salt, hash)
        msg += '\tgot hash({}+{})=={}\n'.format(
            real_move, salt, hash)
        print(msg, file=sys.stderr)
        sys.exit()
    return hash == expected_hash

def decide_move(choose_move, their_move):
    if isinstance(choose_move, type('')):
        return RPS(choose_move)
    return choose_move(their_move)


def play_first(choose_move):
    moves = []
    # discover
    my_address = nw0.discover('RPS')

    # we don't know their move yet!
    my_move = decide_move(choose_move, their_move='None')

    my_salt = make_salt()
    my_hash = make_hash(my_move, my_salt)
    print(my_salt, my_hash)

    # comm 1
    # send my hash
    # recv their hash back
    their_hash = nw0.send_message_to(my_address, my_hash)
    print('I send a sealed {}'.format(my_move))

    # comm 2
    # send my move + salt
    # recv their move + salt back
    their_move_char, their_salt = nw0.send_message_to(
        my_address, (my_move.char, my_salt))
    their_move = RPS(their_move_char)

    check_hash(their_move, their_salt, their_hash)

    moves.append(my_move)
    moves.append(their_move)

    print('I play', my_move)
    print('They play', their_move)
    return decide_winner(moves)


def play_second(choose_move):
    moves = []
    # advertise
    my_address = nw0.advertise("RPS")
    # comm 1a
    # recv their hash
    their_hash = nw0.wait_for_message_from(my_address)

    # we don't know their move yet!
    my_move = decide_move(choose_move, their_move=None)

    my_salt = make_salt()
    my_hash = make_hash(my_move, my_salt)

    # comm 1b
    # reply with hash
    nw0.send_reply_to(my_address, my_hash)
    print('I send a sealed {}'.format(my_move))

    # comm 2a
    # receive their move + salt
    their_move_char, their_salt = nw0.wait_for_message_from(my_address)
    their_move = RPS(their_move_char)

    check_hash(their_move, their_salt, their_hash)

    # now we know their move, let's choose again!
    my_move = decide_move(choose_move, their_move=their_move)

    # comm 2b
    # reply with my move + salt
    nw0.send_reply_to(my_address, (my_move.char, my_salt))

    # my_move = RPS(my_move.char)
    moves.append(their_move)
    moves.append(my_move)

    print('They play', their_move)
    print('I play', my_move)
    return decide_winner(moves)

class Strategies:
    @staticmethod
    def interactive(their_move):
        move = get_local_move('Their move was {}. > '.format(their_move))
        return move

    @staticmethod
    def auto_cheat(their_move):
        if their_move is None:
            return Strategies.random(their_move)
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
