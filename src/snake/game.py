"""Python / Turtle implementation of classic Snake game."""

import turtle
from typing import Callable

from snake.config import Config, SpriteConfig
from snake.constants import KEY_BINDINGS
from snake.game_state import GameState
from snake.ui import ScreenManager


class SnakeGame:
    """Snake game."""

    def __init__(self, config: Config, sprite_config: SpriteConfig) -> None:
        """Initialise SnakeGame.

        Args:
            config: Default configuration settings.
            sprite_config: Sprite attributes.
        """

        self.config = config
        self.sprite_config = sprite_config

        self.screen_manager = ScreenManager(config, sprite_config)
        self.game_state = GameState(config, sprite_config)
        self.setup_listeners()

        # A little flourish before we start.
        self.game_state.snake.spin_head()
        self.game_state.add_food_item()

        # Handle updates.
        self.screen_manager.update_score(self.game_state)
        self.update()

    def setup_listeners(self) -> None:
        """Configure listeners."""
        self.screen_manager.screen.listen()

        for direction, char in KEY_BINDINGS.items():
            fun: Callable = (
                lambda d=direction: self.game_state.snake.set_direction(d)
            )
            self.screen_manager.screen.onkeypress(fun, char)

    def check_collision(self) -> bool:
        """Return True if snake collides with edge of board or its tail."""
        return self.edge_collision() or self.tail_collision()

    def tail_collision(self) -> bool:
        """Return True if head collides with edge of board."""
        head = self.game_state.head
        half_head_size = self.sprite_config.sprite_size // 2
        # Ignore first segment which will be closer to head.
        for segment in self.game_state.segments[1:]:
            if segment.distance(head) < half_head_size:
                return True
        return False

    def edge_collision(self) -> bool:
        """Return True if head collides with edge of board."""
        x_coord, y_coord = self.game_state.head_position
        half_head_size = self.sprite_config.sprite_size // 2
        half_width = self.config.display_width // 2
        half_height = self.config.display_height // 2

        x_min = -(half_width - half_head_size)  # Left
        x_max = -x_min
        y_min = -(half_height - half_head_size)  # Bottom
        y_max = -y_min - self.config.scoreboard_height

        return not (x_min <= x_coord <= x_max and
                    y_min <= y_coord <= y_max)

    def check_food_collision(self):
        """Return True if head collides with food_attributes sprite."""
        if self.game_state.food is not None:
            return (self.game_state.head.distance(self.game_state.food)
                    < self.sprite_config.sprite_size)
        return False

    def eat_food(self):
        """Handle actions when head touches a food_attributes sprite."""
        self.game_state.snake.add_segment()
        self.game_state.add_to_score()
        self.screen_manager.update_score(self.game_state)
        self.game_state.food.replace_food()

    def update(self) -> None:
        """Main game loop to keep updating the game state."""
        self.game_state.snake.move()
        if self.check_collision():
            self.end_game()
        if self.check_food_collision():
            self.eat_food()
        turtle.update()  # pylint: disable=no-member
        screen = self.screen_manager.screen
        screen.ontimer(self.update, self.game_state.delay)

    def end_game(self):
        """Handle game end."""
        self.game_state.reset_current()
        self.screen_manager.update_score(self.game_state)
        self.game_state.snake.reset_snake()
        self.game_state.head.spin_head()
        self.game_state.food.replace_food()


if __name__ == '__main__':
    game = SnakeGame(Config(), SpriteConfig())
    turtle.Screen().mainloop()
