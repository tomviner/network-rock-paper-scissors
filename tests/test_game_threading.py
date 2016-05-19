from __future__ import unicode_literals, print_function

import threading

from netrps.game import play_second, play_first


def test_game(turn, reset_beacon):
    results = []

    def wrapped_play(n, my_move_char):
        if n == 1:
            result = play_first(my_move_char)
        else:
            result = play_second(my_move_char)
        results.append(result)

    t1 = threading.Thread(target=wrapped_play, args=(1, turn.p1_mv))
    t2 = threading.Thread(target=wrapped_play, args=(2, turn.p2_mv))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    assert results[0] == turn.expected_res
    assert results[1] == turn.expected_res
