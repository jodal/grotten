import pytest

from grotten import actions
from grotten.actions import next_actions
from grotten.levels import load_level
from grotten.models import Direction, Game, Item, Level


@pytest.fixture
def level_1() -> Level:
    return load_level(1)


@pytest.fixture
def game(level_1: Level) -> Game:
    return Game.create(level=level_1)


def test_exit_str():
    action = actions.Exit()

    assert str(action) == "Exit game"


def test_exit_apply(game: Game):
    action = actions.Exit()
    assert game.running is True

    action.apply(game)

    assert game.running is False


def test_go_str():
    action = actions.Go(direction=Direction.NORTH)

    assert str(action) == "Go North"


def test_go_apply(game: Game, level_1: Level):
    action = actions.Go(direction=Direction.WEST)
    assert game.location == level_1.locations["entrance"]

    action.apply(game)

    assert game.location == level_1.locations["skeletons"]


def test_pick_up_str():
    action = actions.PickUp(item=Item(name="Sword"))

    assert str(action) == "Pick up Sword"


def test_pick_up_apply(game: Game, level_1: Level):
    game.location = level_1.locations["skeletons"]
    item = game.location.items[0]
    action = actions.PickUp(item=item)

    assert len(game.location.items) == 1
    assert len(game.inventory) == 0

    action.apply(game)

    assert len(game.location.items) == 0
    assert len(game.inventory) == 1
    assert item in game.inventory


def test_show_inventory_str():
    action = actions.ShowInventory()

    assert str(action) == "Show inventory"


def test_show_inventory_apply(game: Game):
    action = actions.ShowInventory()
    assert not game.tick.inventory_open

    action.apply(game)

    assert game.tick.inventory_open


def test_next_actions(game: Game):
    result = next_actions(game)

    assert result == [
        actions.Go(direction=Direction.NORTH),
        actions.Go(direction=Direction.WEST),
        actions.ShowInventory(),
        actions.Exit(),
    ]


def test_next_actions_with_items(game: Game, level_1: Level):
    game.location = level_1.locations["skeletons"]
    assert len(game.location.items) == 1
    item = game.location.items[0]

    result = next_actions(game)

    assert result == [
        actions.PickUp(item=item),
        actions.Go(direction=Direction.NORTH),
        actions.Go(direction=Direction.EAST),
        actions.ShowInventory(),
        actions.Exit(),
    ]
