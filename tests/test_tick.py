from grotten.models import Tick


def test_tick():
    tick = Tick()

    assert tick.messages == []
    assert tick.inventory_open is False
