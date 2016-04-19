import pytest

import networkzero as nw0

@pytest.yield_fixture
def beacon(request):
    yield
    nw0.discovery.reset_beacon()
