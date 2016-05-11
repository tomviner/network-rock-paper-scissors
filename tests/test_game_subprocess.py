from __future__ import unicode_literals, print_function

from subprocess import PIPE, Popen


def test_game(turn, reset_beacon):
    proc1 = Popen(['netrps', '1', turn.p1_mv], stdout=PIPE)
    proc2 = Popen(['netrps', '2', turn.p2_mv], stdout=PIPE)

    for proc in (proc1, proc2):
        output = str(proc.communicate()[0])
        assert proc.returncode == 0
        assert str(turn.expected_res) in output
