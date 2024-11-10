"""Custom Turtle game sprites."""

import turtle
from itertools import pairwise
from random import choice, randint
from typing import Any

from snake.config import Config, SpriteConfig
from snake.constants import Direction, SpriteAttributes


class SnakeHead(turtle.Turtle):
    """Compound shape turtle for snake head."""
    def __init__(self):
        super().__init__()
        self.shape_name = 'head'
        self.register_head_shape()
        self.shape(self.shape_name)
        self.setheading(90)  # Up
        self.penup()

    def register_head_shape(self):
        """Register compound shape for head of the snake."""
        s: turtle.Shape = turtle.Shape("compound")

        # Temporary turtle for shape creation, to keep it hidden.
        temp = turtle.Turtle()
        temp.hideturtle()
        temp.penup()

        # noinspection SpellCheckingInspection
        components = {
            'face': self.circle_component(temp, (0, -10), 10, 'limegreen'),
            'left_eye': self.circle_component(temp, (-6, 0), 6, 'white'),
            'right_eye': self.circle_component(temp, (6, 0), 6, 'white'),
            'left_pupil': self.circle_component(temp, (-7, 3), 4, 'black'),
            'right_pupil': self.circle_component(temp, (7, 3), 4, 'black')
        }

        for component in components.values():
            try:
                shape, fill = component  # Attempt to unpack
                s.addcomponent(shape, fill)
            except ValueError:
                print(f"Expected tuple (shape, fill), but got {component}")

        turtle.register_shape(self.shape_name, s)  # pylint: disable=no-member
        temp.clear()

    @staticmethod
    def circle_component(t: turtle.Turtle,
                         position: tuple[int, int],
                         size: int,
                         color: str) -> tuple[Any, str]:
        """Return filled circular polygon and fill color."""
        t.color(color)
        t.goto(position)
        t.begin_fill()
        t.begin_poly()
        t.circle(size)
        t.end_poly()
        t.end_fill()
        return t.get_poly(), color

    def spin_head(self) -> None:
        """Spin the head in its current position."""
        turtle.tracer(1)  # pylint: disable=no-member
        for i in range(90, -280, -10):
            self.setheading(i)
        turtle.tracer(0)  # pylint: disable=no-member


class Snake:
    """Snake character as compound turtle."""
    _move_delta_map: dict[Direction, tuple[float, float]] = {}
    _angle_map: dict[Direction, float] = {}

    def __init__(self, config: Config, sprite_config: SpriteConfig) -> None:
        self.config = config
        self.sprite_config = sprite_config

        # Map direction of movement to x,y delta.
        if not Snake._move_delta_map:
            Snake.set_move_delta_map(config.move_delta)
        # Map direction of movement to orientation in degrees
        if not Snake._angle_map:
            Snake.set_angle_map()

        self.head: SnakeHead = SnakeHead()
        self.head.penup()
        self.head_direction = Direction.STOP
        self.segments: list[turtle.Turtle] = []
        self.reset_snake()

    def reset_snake(self):
        """Reset snake and tail to initial state."""
        self.head.goto(0, 0)
        self.head_direction = Direction.STOP
        for segment in self.segments:
            segment.hideturtle()
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

    @classmethod
    def set_angle_map(cls):
        """Initialise angle map."""
        cls._angle_map = {
            Direction.RIGHT: 0,
            Direction.UP: 90,
            Direction.LEFT: 180,
            Direction.DOWN: 270
        }

    def set_direction(self, direction: Direction) -> None:
        """Set snake head direction.

        Snake cannot double back on itself.
        """
        if not direction.is_opposite(self.head_direction):
            self.head_direction = direction
            if direction in Snake._angle_map:
                self.head.setheading(Snake._angle_map[direction])

    def spin_head(self) -> None:
        """Spin the head in its current position."""
        self.head.spin_head()

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
        if len(self.segments) % 2 == 0:
            new_segment.color(self.sprite_config.segment.color)
        else:
            new_segment.color(self.sprite_config.segment_alternate_color)
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
