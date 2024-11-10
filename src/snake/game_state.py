"""Game state classes."""
import turtle
from dataclasses import dataclass

from snake.constants import Coords
from snake.sprites import Food, Snake, SnakeHead


@dataclass
class _Scores:
    """Game score state."""
    current: int = 0
    best: int = 0


class GameState:
    """Current game state."""
    def __init__(self, config, sprite_config):
        self._scores = _Scores()
        self._snake = Snake(config, sprite_config)
        self._sprite_size = sprite_config.sprite_size
        self.delay = config.initial_update_delay
        self.config = config
        self.sprite_config = sprite_config
        self._food = None

    def reset_current(self) -> None:
        """Reset current score."""
        self._scores.current = 0

    @property
    def current_score(self) -> int:
        """Return current score."""
        return self._scores.current

    @property
    def best_score(self) -> int:
        """Return best_score."""
        return self._scores.best

    def add_to_score(self, value: int = 1) -> None:
        """Increase current score and handle high score."""
        self._scores.current += value
        self._scores.best = max(self._scores.current, self._scores.best)

    @property
    def snake(self) -> Snake:
        """Return snake instance."""
        return self._snake

    @property
    def head(self) -> SnakeHead:
        """Return Snake.head sprite."""
        return self._snake.head

    @property
    def head_position(self) -> Coords:
        """Return x/y coordinates of snake head."""
        return Coords(x=self._snake.head.xcor(), y=self._snake.head.ycor())

    @property
    def segments(self) -> list[turtle.Turtle]:
        """Return snake segments."""
        return self._snake.segments

    @property
    def food(self) -> Food:
        """Return food sprite."""
        return self._food

    def add_food_item(self) -> None:
        """Add a random food  item to the board."""
        self._food = Food(self.config, self.sprite_config)

    @property
    def sprite_size(self) -> int:
        """Return px size of turtles.

        sprite_size is a read-only property.
        """
        return self._sprite_size
