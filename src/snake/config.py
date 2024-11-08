"""Configuration classes."""

from dataclasses import dataclass
from snake.constants import SpriteAttributes, TextAttributes


@dataclass
class Config:
    """Configure game defaults."""

    # Game speed.
    initial_update_delay: int = 25  # milliseconds
    move_delta: float = 5.0  # Distance to move snake head per step.

    # Scoreboard.
    scoreboard_height: int = 50
    text: TextAttributes = TextAttributes(color='white',
                                          bg_color='black',
                                          font=("sans", 20, "normal"),
                                          v_pos=50)

    # App window properties.
    display_width: int = 600
    display_height: int = 600
    border: int = 25  # Ensure that all the display area is visible.
    background_color: str = 'black'
    # noinspection SpellCheckingInspection
    board_color: str = 'navyblue'

    @property
    def bg(self) -> str:
        """Alias for background."""
        return self.background_color


@dataclass
class SpriteConfig:
    """Game Turtle attributes."""
    head: SpriteAttributes = SpriteAttributes(color='white',
                                              shape='square')
    segment: SpriteAttributes = SpriteAttributes(color='white',
                                                 shape='circle')
    sprite_size: int = 20  # px size of head.
    # noinspection SpellCheckingInspection
    food_attributes: tuple[SpriteAttributes, ...] = (
        SpriteAttributes(color='red', shape='circle'),
        SpriteAttributes(color='yellow', shape='circle'),
        SpriteAttributes(color='limegreen', shape='circle')
    )
