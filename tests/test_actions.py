from grotten import actions
from grotten.actions import next_actions
from grotten.models import Direction, Item


def test_end_game():
    action = actions.EndGame()

    assert str(action) == "End game"


def test_go():
    action = actions.Go(direction=Direction.NORTH)

    assert str(action) == "Go north"

    action = actions.Go(direction=Direction.EAST)

    assert str(action) == "Go east"


def test_pick_up():
    action = actions.PickUp(item=Item(name="Sword"))

    assert str(action) == "Pick up Sword"


def test_show_inventory():
    action = actions.ShowInventory()

    assert str(action) == "Show inventory"


def test_next_actions(game):
    result = next_actions(game)

    assert result == [
        actions.Go(direction=Direction.NORTH),
        actions.Go(direction=Direction.WEST),
        actions.ShowInventory(),
        actions.EndGame(),
    ]


def test_next_actions_with_items(game, level_1):
    game.location = level_1.locations["skeletons"]
    assert len(game.location.items) == 1
    item = game.location.items[0]

    result = next_actions(game)

    assert result == [
        actions.PickUp(item=item),
        actions.Go(direction=Direction.NORTH),
        actions.Go(direction=Direction.EAST),
        actions.ShowInventory(),
        actions.EndGame(),
    ]
