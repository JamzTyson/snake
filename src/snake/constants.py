"""Type definitions, Enums and other constants."""

from collections import namedtuple
from enum import Enum, auto


SpriteAttributes = namedtuple('SpriteAttributes',
                              ['color', 'shape'])
TextAttributes = namedtuple('TextAttributes',
                            ['color', 'bg_color', 'font', 'v_pos'])


class Direction(Enum):
    """Snake direction flags."""
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    STOP = auto()


KEY_BINDINGS = {
    Direction.UP: "Up",
    Direction.DOWN: "Down",
    Direction.LEFT: "Left",
    Direction.RIGHT: "Right",
    Direction.STOP: "space"
}
