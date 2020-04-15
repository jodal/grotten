import pytest

from grotten import actions
from grotten.actions import next_actions
from grotten.levels import load_level
from grotten.models import Direction, Game, Level


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
    assert game.game_done is False

    action.apply(game)

    assert game.game_done is True


def test_go_str():
    action = actions.Go(direction=Direction.NORTH)

    assert str(action) == "Go North"


def test_go_apply(game: Game, level_1: Level):
    action = actions.Go(direction=Direction.WEST)
    assert game.location == level_1.locations["entrance"]

    action.apply(game)

    assert game.location == level_1.locations["skeletons"]


def test_next_actions(game: Game):
    result = next_actions(game)

    assert result == [
        actions.Go(direction=Direction.NORTH),
        actions.Go(direction=Direction.WEST),
        actions.Exit(),
    ]
