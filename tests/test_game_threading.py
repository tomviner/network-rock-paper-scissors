import sys
import threading
import time

import pytest

from netrps.game import play
from netrps.rps import Result

game_space = (
    ('r', 's', Result.player_1_wins),
    ('r', 'p', Result.player_2_wins),
    ('p', 's', Result.player_2_wins),
    ('r', 'r', Result.draw),
    ('p', 'p', Result.draw),
    ('s', 's', Result.draw),
)
@pytest.mark.parametrize('p1_mv, p2_mv, expected_res', game_space)
def test_game(p1_mv, p2_mv, expected_res, beacon):
    results = []

    def wrapped_play(n, my_move_char):
        result = play(n, my_move_char)
        results.append(result)

    t1 = threading.Thread(target=wrapped_play, args=(1, p1_mv))
    t2 = threading.Thread(target=wrapped_play, args=(2, p2_mv))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    assert results[0] == expected_res
    assert results[1] == expected_res
