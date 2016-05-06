import time
import sys
from multiprocessing import Pool

import pytest
from netrps.game import play
from netrps.rps import Result

# @pytest.mark.skipif(sys.version_info < (3, 0), reason="2.7")
game_space = (
    ('r', 's', Result.player_1_wins),
    ('r', 'p', Result.player_2_wins),
    ('p', 's', Result.player_2_wins),
    ('r', 'r', Result.draw),
    ('p', 'p', Result.draw),
    ('s', 's', Result.draw),
)
@pytest.mark.xfail
@pytest.mark.parametrize('p1_mv, p2_mv, expected_res', game_space)
def test_game(p1_mv, p2_mv, expected_res, beacon):
    pool = Pool(2, maxtasksperchild=1)
    res1 = pool.apply_async(play, args=(1, p1_mv))
    res2 = pool.apply_async(play, args=(2, p2_mv))
    time.sleep(3)
    res1.wait(timeout=5)
    res2.wait(timeout=5)
    pool.close()
    pool.join()
    assert res1.successful()
    assert res2.successful()
    assert res1.get() == expected_res
    assert res2.get() == expected_res
