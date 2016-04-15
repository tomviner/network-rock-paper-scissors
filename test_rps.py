import pytest

import rps
from rps import Result, play_round


@pytest.fixture
def fake_input(monkeypatch):
    def make_fake_input(*values):
        values = iter(values)

        def fake_inputer(*args):
            return next(values)
        monkeypatch.setattr(rps, 'input_function', fake_inputer)
    return make_fake_input

@pytest.mark.parametrize('moves', ('rr', 'pp', 'ss'))
def test_draws(moves, fake_input):
    fake_input(*moves)
    assert play_round() == Result.draw

@pytest.mark.parametrize('moves', ('rs', 'pr', 'sp'))
def test_p1_wins(moves, fake_input):
    fake_input(*moves)
    assert play_round() == Result.player_1_win

@pytest.mark.parametrize('moves', ('sr', 'rp', 'ps'))
def test_p2_wins(moves, fake_input):
    fake_input(*moves)
    assert play_round() == Result.player_2_win
