from grotten.models import Game, Message


def test_loads_level_1_by_default():
    game = Game.create()

    assert game.level.number == 1
    assert game.location == game.level.start


def test_end_game(game):
    assert game.running

    game.end_game()

    assert not game.running


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


def test_die_when_more_lives_left(game):
    lives_before = game.lives
    assert lives_before > 1

    game.die()

    assert game.lives == lives_before - 1
    assert game.tick.actions_allowed is True
    assert len(game.tick.messages) == 1
    assert game.tick.messages[0].title == "You died"


def test_die_when_running_out_of_lives(game):
    game.lives = 1

    game.die()

    assert game.lives == 0
    assert game.tick.actions_allowed is False
    assert len(game.tick.messages) == 1
    assert game.tick.messages[0].title == "You died"


def test_restart_level(game, level_1):
    game.location = level_1.locations["pit"]

    game.restart_level()

    assert game.location == level_1.start
    assert game.tick.actions_allowed is False
    assert len(game.tick.messages) == 1
    assert game.tick.messages[0].title == "Restart"


def test_show_inventory(game):
    assert game.tick.inventory_open is False

    game.show_inventory()

    assert game.tick.inventory_open is True
