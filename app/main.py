from __future__ import annotations
from enum import Enum
from collections import Counter


class BattleshipError(Exception):
    pass


class ShipsTooCloseError(BattleshipError):
    pass


class ShipTotalCountError(BattleshipError):
    pass


class ShipTypesCountError(BattleshipError):
    pass


class Tile(Enum):
    EMPTY = " ~ "


class Deck(Enum):
    ALIVE = " ■ "
    HIT = " □ "
    SUNK = " x "

    def next(self) -> Deck:
        states = (Deck.ALIVE, Deck.HIT, Deck.SUNK)
        current_index = states.index(self)
        next_index = min(current_index + 1, len(states) - 1)
        return states[next_index]


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.decks = Ship.create_decks(start, end)
        self.is_drowned = is_drowned

    def __len__(self) -> int:
        return len(self.decks)

    @staticmethod
    def create_decks(
            start: tuple[int, int],
            end: tuple[int, int]
    ) -> dict[tuple[int, int], Deck]:
        decks = {}

        column = start[1]
        while column <= end[1]:
            decks[(start[0], column)] = Deck.ALIVE
            column += 1

        row = start[0]
        while row <= end[0]:
            decks[(row, start[1])] = Deck.ALIVE
            row += 1

        return decks

    def get_ship_cells(self) -> tuple[tuple[int, int], ...]:
        return tuple(self.decks.keys())

    def get_deck(self, row: int, column: int) -> Deck:
        return self.decks[(row, column)]

    def fire(self, row: int, column: int) -> None:
        if not self.is_drowned:
            self.decks[(row, column)] = self.decks[(row, column)].next()
            if all(status == Deck.HIT for status in self.decks.values()):
                self.is_drowned = True
                for key in self.decks:
                    self.decks[key] = self.decks[key].next()


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], ...]],
            title_word: str | None = "РЕСПУБЛІКА"
    ) -> None:
        self.title_word = title_word
        self.fields = Battleship.create_fields(ships)
        self._validate_field()

    @staticmethod
    def create_fields(
            ships: list[tuple[tuple[int, int], ...]]
    ) -> dict[tuple, Ship]:
        fields = {}
        for ship in ships:
            ship_object = Ship(*ship)
            for cell in ship_object.get_ship_cells():
                fields[cell] = ship_object
        return fields

    def fire(self, location: tuple[int, int]) -> str:
        if location in self.fields:
            ship = self.fields[location]
            ship.fire(*location)
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def column_coordinates_string(self) -> str:
        if self.title_word is None or len(self.title_word) != 10:
            return "   " + " ".join(str(i) + " " for i in range(10)) + "\n"
        return "   " + " ".join(char + " " for char in self.title_word) + "\n"

    def print_field(self) -> None:
        field_str = self.column_coordinates_string()

        for row in range(10):
            field_str += str(row) + " "
            for col in range(10):
                cell = (row, col)
                if cell in self.fields:
                    field_str += self.fields[cell].get_deck(*cell).value
                else:
                    field_str += Tile.EMPTY.value
            field_str += "\n"
        print(field_str)

    @staticmethod
    def _validate_ship_types(ships: set) -> None:
        ship_deck_counts = Counter(len(ship) for ship in ships)

        required_counts = {1: 4, 2: 3, 3: 2, 4: 1}

        for size, required in required_counts.items():
            if ship_deck_counts.get(size, 0) != required:
                raise ShipTypesCountError(
                    f"Field must have {required} {size}-deck ships"
                )

    @staticmethod
    def _validate_ship_placement(ships: set) -> None:
        for ship in ships:
            ship_cells = ship.get_ship_cells()
            for cell in ship_cells:
                # check adjacent
                ...

    def _validate_field(self) -> None:
        ships = set(self.fields.values())

        if len(ships) != 10:
            raise ShipTotalCountError("Field must have 10 ships")

        Battleship._validate_ship_types(ships)

        Battleship._validate_ship_placement(ships)


if __name__ == "__main__":
    battle_ship = Battleship(
        ships=[
            ((2, 0), (2, 3)),
            ((4, 5), (4, 6)),
            ((3, 8), (3, 9)),
            ((6, 0), (8, 0)),
            ((6, 4), (6, 6)),
            ((6, 8), (6, 9)),
            ((9, 9), (9, 9)),
            ((9, 5), (9, 5)),
            ((9, 3), (9, 3)),
            ((9, 7), (9, 7)),
        ]
    )
    battle_ship.print_field()

    battle_ship.fire((0, 4))
    battle_ship.print_field()
    battle_ship.fire((1, 7))
    battle_ship.print_field()
    battle_ship.fire((2, 0))
    battle_ship.print_field()
    battle_ship.fire((2, 1))
    battle_ship.print_field()
    battle_ship.fire((2, 2))
    battle_ship.print_field()
    battle_ship.fire((2, 3))
    battle_ship.print_field()
    battle_ship.fire((4, 3))
    battle_ship.print_field()
    battle_ship.fire((4, 5))
    battle_ship.print_field()
    battle_ship.fire((5, 5))
    battle_ship.print_field()
    battle_ship.fire((4, 6))
    battle_ship.print_field()
    battle_ship.fire((9, 5))
    battle_ship.print_field()
    battle_ship.fire((9, 6))
    battle_ship.print_field()
