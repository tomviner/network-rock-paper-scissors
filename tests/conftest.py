import pytest

import networkzero as nw0

@pytest.yield_fixture(autouse=True)
def beacon(request):
    yield
    nw0.discovery.reset_beacon()
