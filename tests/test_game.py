from grotten.models import Message


def test_begin_tick(game):
    game.create_message(kind="a_kind", title="A title")
    assert len(game.tick.messages) == 1
    game.tick.inventory_open = True
    game.tick.actions_allowed = False

    game.begin_tick()

    assert game.tick.messages == []
    assert game.tick.inventory_open is False
    assert game.tick.actions_allowed is True


def test_create_message(game):
    game.create_message(kind="a_kind", title="A title", content="Some content")

    assert game.tick.messages == [
        Message(kind="a_kind", title="A title", content="Some content")
    ]
