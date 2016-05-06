import sys
import time
from subprocess import PIPE, Popen

import pytest

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
    processes = []
    for p_num, mv in enumerate((p1_mv, p2_mv), start=1):
        processes.append(Popen(
            [
                sys.executable,
                'netrps/game.py',
                str(p_num),
                mv,
            ],
            stdout=PIPE
        ))

    while (
        processes[0].returncode is None and
        processes[1].returncode is None
    ):
        time.sleep(0.1)
        processes[0].poll()
        processes[1].poll()

    for process in processes:
        output = str(process.communicate()[0])
        assert str(expected_res) in output
