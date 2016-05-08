from multiprocessing import Pool

import pytest

from netrps.game import play


@pytest.fixture(scope='session')
def pool(processes=2):
    return Pool(processes=processes)

def test_game(pool, turn, beacon):
    res1 = pool.apply_async(play, args=(1, turn.p1_mv))
    res2 = pool.apply_async(play, args=(2, turn.p2_mv))
    assert res1.get() == turn.expected_res
    assert res2.get() == turn.expected_res
    assert res1.successful()
    assert res2.successful()
