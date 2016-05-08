import threading

from netrps.game import play


def test_game(turn, beacon):
    results = []

    def wrapped_play(n, my_move_char):
        result = play(n, my_move_char)
        results.append(result)

    t1 = threading.Thread(target=wrapped_play, args=(1, turn.p1_mv))
    t2 = threading.Thread(target=wrapped_play, args=(2, turn.p2_mv))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    assert results[0] == turn.expected_res
    assert results[1] == turn.expected_res
