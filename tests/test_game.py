from fractions import Fraction

from grotten import actions
from grotten.enums import Direction, Kind
from grotten.models import Game, Item, Message


def test_loads_level_1_by_default():
    game = Game.create()

    assert game.level.number == 1
    assert game.location == game.level.start


def test_create_message(game):
    game.create_message(kind=Kind.GAME, title="A title", content="Some content")

    assert game.messages == [
        Message(kind=Kind.GAME, title="A title", content="Some content")
    ]


def test_pop_messages(game):
    game.create_message(kind=Kind.GAME, title="A title")
    assert len(game.messages) == 1

    messages = game.pop_messages()

    assert game.messages == []
    assert messages == [Message(kind=Kind.GAME, title="A title")]


def test_available_actions(game):
    result = game.available_actions()

    assert result == [
        actions.Go(direction=Direction.NORTH),
        actions.Go(direction=Direction.WEST),
        actions.ShowInventory(),
        actions.EndGame(),
    ]


def test_available_actions_with_inventory(game, level_1):
    game.location = level_1.locations["skeletons"]
    assert len(game.location.items) == 1
    item = game.location.items[0]

    result = game.available_actions()

    assert result == [
        actions.PickUp(item=item),
        actions.Go(direction=Direction.NORTH),
        actions.Go(direction=Direction.EAST),
        actions.ShowInventory(),
        actions.EndGame(),
    ]


def test_end_game(game):
    assert game.running

    game.end_game()

    assert not game.running
    assert len(game.messages) == 1
    assert game.messages[0].title == "Welcome back"


def test_go(game, level_1):
    assert game.location == level_1.locations["entrance"]

    game.go(Direction.WEST)

    assert game.location == level_1.locations["skeletons"]
    assert len(game.messages) >= 2
    assert game.messages[0].title == "Going west"
    assert game.messages[1].title == "Skeletons"


def test_go_with_new_location_effect(game, level_1):
    lives_before = game.lives

    game.go(Direction.NORTH)

    # Effect causes you to die
    assert game.lives == lives_before - 1


def test_go_to_location_with_creature(game, level_1):
    game.location = level_1.locations["skeletons"]

    game.go(Direction.NORTH)

    assert game.location == level_1.locations["dragon_lair"]
    assert Message(kind=Kind.CREATURE, title="Green Dragon") in game.messages


def test_attack_with_bare_hands(game, level_1):
    game.location = level_1.locations["dragon_lair"]
    creature = game.location.creatures[0]
    assert creature.strength == 12
    assert game.inventory.get_weapon().attack_strength == 3

    winning_odds = game.attack(creature)

    assert winning_odds == Fraction(3, 12)


def test_attack_with_sword(game, level_1):
    game.location = level_1.locations["dragon_lair"]
    game.inventory.add(Item(name="sword", attack_strength=8))
    creature = game.location.creatures[0]
    assert creature.strength == 12
    assert game.inventory.get_weapon().attack_strength == 8

    winning_odds = game.attack(creature)

    assert winning_odds == Fraction(8, 12)


def test_pick_up(game, level_1):
    game.location = level_1.locations["skeletons"]
    item = game.location.items[0]

    assert len(game.location.items) == 1
    assert len(game.inventory.items) == 0

    game.pick_up(item)

    assert len(game.location.items) == 0
    assert len(game.inventory.items) == 1
    assert item in game.inventory.items


def test_show_inventory_when_empty(game):
    game.show_inventory()

    assert len(game.messages) == 1
    assert game.messages == [
        Message(
            kind=Kind.INVENTORY,
            title="empty",
            content="The inventory is empty.",
        )
    ]


def test_show_inventory_with_content(game):
    game.inventory.add(Item(name="Sword"))

    game.show_inventory()

    assert Message(kind=Kind.INVENTORY, title="Sword") in game.messages


def test_die_when_more_lives_left(game):
    lives_before = game.lives
    assert lives_before > 1

    game.die()

    assert game.lives == lives_before - 1
    assert len(game.messages) == 1
    assert game.messages[0].title == "You died"


def test_die_when_running_out_of_lives(game):
    game.lives = 1

    game.die()

    assert game.lives == 0
    assert len(game.messages) == 2
    assert game.messages[0].title == "You died"
    assert game.messages[1].title == "Game over"


def test_restart_level(game, level_1):
    game.location = level_1.locations["pit"]

    game.restart_level()

    assert game.location == level_1.start
    assert len(game.messages) == 1
    assert game.messages[0].title == "Restart"
