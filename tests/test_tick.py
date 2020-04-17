from grotten.models import Tick


def test_tick():
    tick = Tick()

    assert tick.messages == []
