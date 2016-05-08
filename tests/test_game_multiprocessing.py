from multiprocessing import Pool

import pytest

from netrps.game import play
from netrps.rps import Result


@pytest.fixture(scope='session')
def pool(processes=2):
    return Pool(processes=processes)

game_space = (
    ('r', 's', Result.player_1_wins),
    ('r', 'p', Result.player_2_wins),
    ('p', 's', Result.player_2_wins),
    ('r', 'r', Result.draw),
    ('p', 'p', Result.draw),
    ('s', 's', Result.draw),
)
@pytest.mark.parametrize('p1_mv, p2_mv, expected_res', game_space)
def test_game(pool, p1_mv, p2_mv, expected_res, beacon):
    res1 = pool.apply_async(play, args=(1, p1_mv))
    res2 = pool.apply_async(play, args=(2, p2_mv))
    assert res1.get() == expected_res
    assert res2.get() == expected_res
    assert res1.successful()
    assert res2.successful()
