from grotten import actions
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
