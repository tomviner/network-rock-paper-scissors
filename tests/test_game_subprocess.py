import sys
from subprocess import PIPE, Popen


def test_game(turn, beacon):
    proc1 = Popen(
        [sys.executable, 'netrps/game.py', '1', turn.p1_mv],
        stdout=PIPE)
    proc2 = Popen(
        [sys.executable, 'netrps/game.py', '2', turn.p2_mv],
        stdout=PIPE)

    for proc in (proc1, proc2):
        output = str(proc.communicate()[0])
        assert proc.returncode == 0
        assert str(turn.expected_res) in output
