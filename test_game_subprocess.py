import sys
from subprocess import PIPE, Popen

import pytest
from rps import Result

game_space = (
    ('r', 's', Result.player_1_wins),
    ('r', 'p', Result.player_1_winsr_2_wins),
    ('p', 's', Result.player_2_wins),
    ('r', 'r', Result.draw),
    ('p', 'p', Result.draw),
    ('s', 's', Result.draw),
)
@pytest.mark.parametrize('p1_mv, p2_mv, expected_res', game_space)
def test_game(p1_mv, p2_mv, expected_res):
    processes = []
    for i, mv in enumerate((p1_mv, p2_mv), start=1):
        processes.append(Popen(
            [
                sys.executable,
                'game.py',
                str(i),
                mv,
            ],
            stdout=PIPE
        ))

    for process in processes:
        output = str(process.communicate()[0])
        assert str(expected_res) in output
