"""Game state classes."""
from dataclasses import dataclass

from snake.sprites import Food, Snake


@dataclass
class _Scores:
    """Game score state."""
    current: int = 0
    best: int = 0


class GameState:
    """Current game state."""
    def __init__(self, config, sprite_config):
        self.scores = _Scores()
        self.snake = Snake(config, sprite_config)
        self.food = Food(config, sprite_config)
        self.delay = config.initial_update_delay

    def reset_current(self) -> None:
        """Reset current score."""
        self.scores.current = 0

    def add_to_score(self, value: int = 1) -> None:
        """Increase current score and handle high score."""
        self.scores.current += value
        self.scores.best = max(self.scores.current, self.scores.best)
