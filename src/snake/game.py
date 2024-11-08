"""Python / Turtle implementation of classic Snake game."""

from collections.abc import Callable
from itertools import pairwise
from random import choice, randint
import turtle

from snake.config import Config, SpriteConfig
from snake.constants import (Direction,
                             KEY_BINDINGS,
                             BACKTRACK_MAP,
                             SpriteAttributes)
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

        # Initialise speed (delay) and scores.
        self.delay = config.initial_update_delay
        self.scores: dict[str, int] = {'current_score': 0, 'high_score': 0}

        # Initialise game components.
        self.screen_manager = ScreenManager(config, sprite_config)
        self.snake = Snake(self.config, self.sprite_config)
        self.food = Food(config, sprite_config)

        self.setup_listeners()

        # Handle updates.
        self.screen_manager.update_score(self.scores)
        self.update()

    def setup_listeners(self) -> None:
        """Configure listeners."""
        self.screen_manager.screen.listen()
        for direction, char in KEY_BINDINGS.items():
            fun: Callable = lambda d=direction: self.snake.set_direction(d)
            self.screen_manager.screen.onkeypress(fun, char)

    def check_collision(self) -> bool:
        """Return True if snake collides with edge of board or its tail."""
        return self.edge_collision() or self.tail_collision()

    def tail_collision(self) -> bool:
        """Return True if head collides with edge of board."""
        head = self.snake.head
        half_head_size = self.sprite_config.sprite_size // 2
        for segment in self.snake.segments:
            if segment.distance(head) <= half_head_size:
                return True
        return False

    def edge_collision(self) -> bool:
        """Return True if head collides with edge of board."""
        x_coord = self.snake.head.xcor()
        y_coord = self.snake.head.ycor()
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
        return (self.snake.head.distance(self.food)
                < self.sprite_config.sprite_size)

    def eat_food(self):
        """Handle actions when head touches a food_attributes sprite."""
        self.scores['current_score'] += 1
        if self.scores['current_score'] > self.scores['high_score']:
            self.scores['high_score'] = self.scores['current_score']
        self.screen_manager.update_score(self.scores)
        self.food.replace_food()

    def update(self) -> None:
        """Main game loop to keep updating the game state."""
        self.snake.move()
        if self.check_collision():
            self.scores['current_score'] = 0
            self.screen_manager.update_score(self.scores)
            self.snake.reset_snake()
        if self.check_food_collision():
            self.eat_food()
        turtle.update()  # pylint: disable=no-member
        screen = self.screen_manager.screen
        screen.ontimer(self.update, self.delay)


class Snake:
    """Snake character as compound turtle."""
    _backtrack_map = BACKTRACK_MAP
    _move_delta_map: dict[Direction, tuple[float, float]] = {}

    def __init__(self, config: Config, sprite_config: SpriteConfig) -> None:
        self.config = config
        self.sprite_config = sprite_config

        # Map direction of movement to x,y delta.
        if not Snake._move_delta_map:
            Snake.set_move_delta_map(config.move_delta)

        self.head = turtle.Turtle()
        self.head.shape(self.sprite_config.head.shape)
        self.head.color(self.sprite_config.head.color)
        self.head.penup()
        self.head_direction = Direction.STOP
        self.segments: list[turtle.Turtle] = []
        self.reset_snake()

    def reset_snake(self):
        """Reset snake and tail to initial state."""
        self.head.goto(0, 0)
        self.head_direction = Direction.STOP
        self.segments = []

    @classmethod
    def set_move_delta_map(cls, delta: float) -> None:
        """Initialize or update the class-level movement delta map.

        Maps the direction of movement to x,y delta.
        """
        cls._move_delta_map = {
            Direction.UP: (0, delta),
            Direction.DOWN: (0, -delta),
            Direction.LEFT: (-delta, 0),
            Direction.RIGHT: (delta, 0)
        }

    def set_direction(self, direction: Direction) -> None:
        """Set snake head direction.

        Snake cannot double back on itself.
        """
        if self.head_direction is not Snake._backtrack_map.get(direction):
            self.head_direction = direction

    def add_segment(self) -> None:
        """Add one body segment.

        Sets the initial position of the new segment at the same
        position as the final segment, or the same position as the
        head if this is the first segment. The position will be corrected
        on the next move() call.
        """
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("circle")
        new_segment.color(self.sprite_config.segment.color)
        new_segment.penup()

        if self.segments:
            # Add new segment at same position as final tail segment.
            new_segment.goto(self.segments[-1].xcor(),
                             self.segments[-1].ycor())
        else:
            # Add new segment at head position.
            new_segment.goto(self.head.xcor(), self.head.ycor())

        self.segments.append(new_segment)

    def move(self) -> None:
        """Update snake position."""
        if self.head_direction is not Direction.STOP:
            delta_x, delta_y = Snake._move_delta_map[self.head_direction]
            previous_head_position = self.head.xcor(), self.head.ycor()
            new_x = self.head.xcor() + delta_x
            new_y = self.head.ycor() + delta_y
            self.head.goto(new_x, new_y)

            self.update_tail(previous_head_position)

    def update_tail(self, prev_head_position: tuple[float, float]) -> None:
        """Update positions of tail segments."""
        prev_head_x, prev_head_y = prev_head_position
        # Update tail segments in reverse order.
        for current, previous in pairwise(reversed(self.segments)):
            current.goto(previous.xcor(), previous.ycor())

        # Update first segment to old head position.
        if self.segments:
            self.segments[0].goto(prev_head_x, prev_head_y)


class Food(turtle.Turtle):
    """Sprites to be collected."""
    def __init__(self, config: Config, sprite_config: SpriteConfig) -> None:
        super().__init__()
        self.config = config
        self.sprite_config = sprite_config
        self.sprite_size = sprite_config.sprite_size
        attributes = choice(sprite_config.food_attributes)
        self.set_attributes(attributes)
        self.place_food()

    def set_attributes(self, food_attributes: SpriteAttributes) -> None:
        """Set food turtle attributes."""
        self.color(food_attributes.color)
        self.shape(food_attributes.shape)
        self.penup()

    def place_food(self) -> None:
        """Add food item at random position"""
        padding = self.sprite_size
        x_max = self.config.display_width // 2 - padding
        half_height = self.config.display_height // 2
        y_max = half_height - self.config.scoreboard_height - padding
        y_min = padding - half_height
        position = randint(-x_max, x_max), randint(y_min, y_max)
        self.goto(position)

    def replace_food(self):
        """Re-initialise 'eaten' food as new food item."""
        self.hideturtle()
        attributes = choice(self.sprite_config.food_attributes)
        self.set_attributes(attributes)
        self.place_food()
        self.showturtle()


if __name__ == '__main__':
    game = SnakeGame(Config(), SpriteConfig())
    turtle.Screen().mainloop()
