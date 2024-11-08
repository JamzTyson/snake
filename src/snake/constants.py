"""Type definitions, Enums and other constants."""

from typing import NamedTuple
from enum import Enum, auto


class SpriteAttributes(NamedTuple):
    """Color and shape of sprites."""
    color: str
    shape: str


class TextAttributes(NamedTuple):
    """Text attributes."""
    color: str
    bg_color: str
    font: tuple[str, int, str]
    v_pos: int


# noinspection SpellCheckingInspection
class Coords(NamedTuple):
    """x/y coordinates."""
    x: int
    y: int


class Direction(Enum):
    """Snake direction flags."""
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    STOP = auto()


KEY_BINDINGS: dict[Direction, str] = {
    Direction.UP: "Up",
    Direction.DOWN: "Down",
    Direction.LEFT: "Left",
    Direction.RIGHT: "Right",
    Direction.STOP: "space"
}


BACKTRACK_MAP: dict[Direction, Direction] = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT
}
"""BACKTRACK_MAP: Maps each Direction to its opposite."""
