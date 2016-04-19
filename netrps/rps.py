from __future__ import print_function

from collections import deque
from functools import total_ordering

from enum import IntEnum

input_function = input

class Result(IntEnum):
    player_1_wins = 1
    player_2_wins = 2
    draw = 3

    def __str__(self):
        return self.name.replace('_', ' ').title()

@total_ordering
class RPS(object):
    keys = {
        'r': 'Rock',
        'p': 'Paper',
        's': 'Scissors',
    }

    def __init__(self, move):
        assert move in self.keys, move
        self.move = move

    def __hash__(self):
        return hash(self.move)

    def __eq__(self, other):
        return self.move == other.move

    def __lt__(self, other):
        loses_to = deque('rps')
        while loses_to[0] != self.move:
            loses_to.rotate(1)
        return other.move == loses_to[1]

    def __repr__(self):
        return self.keys[self.move]


def get_local_move():
    while True:
        print('Enter [r]ock, [p]aper or [s]cissors')
        move = input_function('> ').lower()
        if move in 'rps':
            return RPS(move)

def play_round():
    moves = []
    for player in range(1, 3):
        print('player {}, enter your move:'.format(player))
        moves.append(get_local_move())
    return decide_winner(moves)

def decide_winner(moves):
    assert len(moves) == 2, moves
    winning_move = max(moves)
    loosing_move = min(moves)
    if winning_move == loosing_move:
        print(winning_move, 'draws', loosing_move)
        return Result.draw
    methods = {
        'r': 'Blunts',
        'p': 'Covers',
        's': 'Cut',
    }
    winner_index = moves.index(winning_move)
    print(winning_move, methods[winning_move.move], loosing_move)
    return list(Result.__members__.values())[winner_index]

def main():
    print(play_round().name.replace('_', ' '), '!')

if __name__ == '__main__':
    main()