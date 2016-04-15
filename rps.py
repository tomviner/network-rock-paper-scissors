from __future__ import print_function

from collections import deque
from enum import IntEnum
from functools import total_ordering

input_function = input

class Result(IntEnum):
    player_1_win = 1
    player_2_win = 2
    draw = 3

@total_ordering
class RPS(object):
    def __init__(self, move):
        assert move in 'rps'
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

def get_move():
    while True:
        print('Enter [r]ock, [p]aper or [s]cissors')
        move = input_function('> ').lower()
        if move in 'rps':
            return RPS(move)

def play_round():
    moves = []
    for player in range(1, 3):
        print('player {}, enter your move:'.format(player))
        moves.append(get_move())

    winning_move = max(moves)
    loosing_move = min(moves)
    if winning_move == loosing_move:
        return Result.draw
    winner_index = moves.index(winning_move)
    return list(Result.__members__.values())[winner_index]

def main():
    print(play_round().name.replace('_', ' '), '!')

if __name__ == '__main__':
    main()
