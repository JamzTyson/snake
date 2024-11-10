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
    x: float
    y: float


# Global dictionary for opposite directions
_BACKTRACK_MAP = {
    'UP': 'DOWN',
    'DOWN': 'UP',
    'LEFT': 'RIGHT',
    'RIGHT': 'LEFT',
}


class Direction(Enum):
    """Snake direction flags."""
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    STOP = auto()

    def is_opposite(self, d: 'Direction') -> bool:
        """Return True if d is opposite direction."""
        return self.name == _BACKTRACK_MAP.get(d.name)


KEY_BINDINGS: dict[Direction, str] = {
    Direction.UP: "Up",
    Direction.DOWN: "Down",
    Direction.LEFT: "Left",
    Direction.RIGHT: "Right",
    Direction.STOP: "space"
}
