import pytest

from grotten import actions
from grotten.models import Creature, Direction, Item


def test_base():
    action = actions.Action()

    with pytest.raises(NotImplementedError):
        str(action)

    assert not action.is_meta_action()


def test_end_game():
    action = actions.EndGame()

    assert str(action) == "End game"
    assert action.is_meta_action()


def test_go():
    action = actions.Go(direction=Direction.NORTH)

    assert str(action) == "Go north"
    assert not action.is_meta_action()

    action = actions.Go(direction=Direction.EAST)

    assert str(action) == "Go east"


def test_attack():
    action = actions.Attack(creature=Creature(name="Dragon"))

    assert str(action) == "Attack Dragon"
    assert not action.is_meta_action()


def test_pick_up():
    action = actions.PickUp(item=Item(name="Sword"))

    assert str(action) == "Pick up Sword"
    assert not action.is_meta_action()


def test_show_inventory():
    action = actions.ShowInventory()

    assert str(action) == "Show inventory"
    assert action.is_meta_action()
