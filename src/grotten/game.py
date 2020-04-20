from __future__ import annotations

import random
from dataclasses import dataclass, field
from fractions import Fraction
from gettext import gettext as _, ngettext
from typing import List, Optional

from grotten import actions
from grotten.enums import Direction, Kind
from grotten.models import (
    Creature,
    Item,
    Inventory,
    Level,
    Location,
    Mailbox,
)
from grotten.levels import load_level


@dataclass
class Game:
    level: Level
    location: Location
    inventory: Inventory = field(default_factory=Inventory)
    lives: int = 3
    running: bool = True
    messages: Mailbox = field(default_factory=Mailbox)

    @classmethod
    def create(cls, *, level: Optional[Level] = None) -> Game:
        if level is None:
            level = load_level(1)
        return cls(level=level, location=level.start)

    # --- Actions

    def available_actions(self) -> List[actions.Action]:
        result: List[actions.Action] = []

        for creature in self.location.creatures:
            result.append(actions.Attack(creature=creature))

        for item in self.location.items:
            result.append(actions.PickUp(item=item))

        for direction in Direction:
            if direction in self.location.neighbors:
                result.append(actions.Go(direction=direction))

        result.append(actions.ShowInventory())
        result.append(actions.EndGame())

        return result

    def apply(self, action: actions.Action) -> None:
        if isinstance(action, actions.EndGame):
            self.end_game()
        elif isinstance(action, actions.Go):
            self.go(action.direction)
        elif isinstance(action, actions.Attack):
            self.attack(action.creature)
        elif isinstance(action, actions.PickUp):
            self.pick_up(action.item)
        elif isinstance(action, actions.ShowInventory):
            self.show_inventory()

    def end_game(self) -> None:
        self.running = False
        self.messages.add(kind=Kind.GAME, title=_("Welcome back"))

    def go(self, direction: Direction) -> None:
        self.location = self.location.neighbors[direction]
        self.messages.add(
            kind=Kind.ACTION,
            title=_("Going {direction}").format(direction=_(direction)),
        )
        self.describe_location()
        if self.location.effect is not None:
            self.location.effect(self)

    def attack(self, creature: Creature) -> Fraction:
        weapon = self.inventory.get_weapon()
        winning_odds = Fraction(weapon.attack_strength, creature.strength)
        self.messages.add(
            kind=Kind.ACTION,
            title=_("Attack {creature}").format(creature=creature.name),
            content=_(
                "You attack {creature} ({creature_strength}) "
                "with {weapon} ({weapon_strength})."
            ).format(
                creature=creature.name,
                creature_strength=creature.strength,
                weapon=weapon.name,
                weapon_strength=weapon.attack_strength,
            ),
        )

        won = random.random() < winning_odds

        if won:
            self.win_fight(creature)
        else:
            self.lose_fight(creature)

        return winning_odds

    def pick_up(self, item: Item) -> None:
        self.location.items.remove(item)
        self.inventory.add(item)
        self.messages.add(
            kind=Kind.ACTION,
            title=_("Picking up {item}").format(item=item.name),
        )

    def show_inventory(self) -> None:
        if not self.inventory.items:
            self.messages.add(
                kind=Kind.INVENTORY,
                title=_("empty"),
                content=_("The inventory is empty."),
            )

        for item in self.inventory.items:
            self.messages.add(kind=Kind.INVENTORY, title=item.name)

    # --- Action building blocks

    def describe_location(self) -> None:
        self.messages.add(
            kind=Kind.LOCATION,
            title=self.location.name,
            content=self.location.description,
        )

        for creature in self.location.creatures:
            self.messages.add(kind=Kind.CREATURE, title=creature.name)

        for item in self.location.items:
            self.messages.add(kind=Kind.ITEM, title=item.name)

    def win_fight(self, creature: Creature) -> None:
        self.messages.add(
            kind=Kind.ACTION,
            title=_("You won"),
            content=_("You defeated {creature}.").format(
                creature=creature.name
            ),
        )
        self.location.creatures.remove(creature)
        self.location.items.extend(creature.loot)

    def lose_fight(self, creature: Creature) -> None:
        self.messages.add(
            kind=Kind.ACTION,
            title=_("You lost"),
            content=_("You lost the battle with {creature}.").format(
                creature=creature.name
            ),
        )
        self.die()

    def die(self) -> None:
        self.lives -= 1
        self.messages.add(
            kind=Kind.LIFE,
            title=_("You died"),
            content=ngettext(
                _("You have only {lives} life left."),
                _("You have {lives} lives left."),
                self.lives,
            ).format(lives=self.lives),
        )
        if self.lives == 0:
            self.messages.add(kind=Kind.GAME, title=_("Game over"))

    def restart_level(self) -> None:
        self.location = self.level.start
        self.messages.add(
            kind=Kind.LEVEL,
            title=_("Restart"),
            content=_("You respawn at the beginning."),
        )
