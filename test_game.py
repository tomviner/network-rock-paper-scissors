import time
import threading

import pytest

from game import play
from rps import Result

game_space = (
    ('r', 's', Result.player_1_wins),
    ('r', 'p', Result.player_2_wins),
    ('p', 's', Result.player_2_wins),
    ('r', 'r', Result.draw),
    ('p', 'p', Result.draw),
    ('s', 's', Result.draw),
)
@pytest.mark.parametrize('p1_mv, p2_mv, res', game_space)
def test_game(p1_mv, p2_mv, res):
    results = []

    def wrapped_play(n, my_move_char):
        result = play(n, my_move_char)
        results.append(result)

    t1 = threading.Thread(target=wrapped_play, args=(1, p1_mv))
    t2 = threading.Thread(target=wrapped_play, args=(2, p2_mv))
    t1.start()
    t2.start()
    for i in range(3):
        time.sleep(0.1)
        t1.join(timeout=0.5)
        t2.join(timeout=0.5)
    assert not t1.is_alive()
    assert not t2.is_alive()
    assert results[0] == res
    assert results[1] == res
