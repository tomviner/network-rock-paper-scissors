from __future__ import unicode_literals, print_function

from multiprocessing import Pool

import pytest

from netrps.game import play_second, play_first


@pytest.fixture(scope='session')
def pool(processes=2):
    return Pool(processes=processes)

def test_game(pool, turn, reset_beacon):
    res1 = pool.apply_async(play_second, args=(turn.p1_mv,))
    res2 = pool.apply_async(play_first, args=(turn.p2_mv,))
    assert res1.get() == turn.expected_res
    assert res2.get() == turn.expected_res
    assert res1.successful()
    assert res2.successful()
