"""Configuration classes."""

from dataclasses import dataclass
from snake.constants import SpriteAttributes, TextAttributes


# pylint: disable=too-many-instance-attributes
@dataclass
class Config:
    """Configure game defaults."""

    # Game speed.
    initial_update_delay: int = 50  # milliseconds
    move_delta: float = 10.0  # Distance to move snake head per step.

    # Scoreboard.
    scoreboard_height: int = 50
    scoreboard_text: TextAttributes = TextAttributes(
        color='white',
        bg_color='black',
        font=("sans", 20, "normal")
    )
    splash_text: TextAttributes = TextAttributes(
        color='blue',
        bg_color='',
        font=("sans", 20, "normal")
    )

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
    head: SpriteAttributes = SpriteAttributes(color='limegreen',
                                              shape='square')
    segment: SpriteAttributes = SpriteAttributes(color='limegreen',
                                                 shape='circle')
    segment_alternate_color: str = 'green'
    sprite_size: int = 20  # px size of head.
    # noinspection SpellCheckingInspection
    food_attributes: tuple[SpriteAttributes, ...] = (
        SpriteAttributes(color='limegreen', shape='lime.gif', value=1),
        SpriteAttributes(color='red', shape='cherry.gif', value=2),
        SpriteAttributes(color='yellow', shape='banana.gif', value=3),
    )
