from collections import namedtuple

import pytest

import networkzero as nw0
from netrps.rps import Result


@pytest.yield_fixture
def beacon(request):
    yield
    nw0.discovery.reset_beacon()

game_space = (
    ('r', 's', Result.player_1_wins),
    ('r', 'p', Result.player_2_wins),
    ('p', 's', Result.player_2_wins),
    ('r', 'r', Result.draw),
    ('p', 'p', Result.draw),
    ('s', 's', Result.draw),
)

class Turn(namedtuple('Turn', ('p1_mv', 'p2_mv', 'expected_res'))):
    def __str__(self):
        return '-'.join(map(str, self))
param_ids = [str(Turn(*t)) for t in game_space]

@pytest.fixture(params=game_space, ids=param_ids)
def turn(request):
    return Turn(*request.param)
