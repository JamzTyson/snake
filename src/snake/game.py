"""Python / Turtle implementation of classic Snake game."""

from collections import namedtuple
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum, auto
from itertools import pairwise
from random import choice, randint

import turtle


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


class KeyBindings:
    """Static key bindings for direction controls."""
    bindings = {
        Direction.UP: "Up",
        Direction.DOWN: "Down",
        Direction.LEFT: "Left",
        Direction.RIGHT: "Right",
        Direction.STOP: "space"
    }


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
    head_size: int = 20  # px size of head.
    # noinspection SpellCheckingInspection
    food: tuple[SpriteAttributes, ...] = (
        SpriteAttributes(color='red', shape='circle'),
        SpriteAttributes(color='yellow', shape='circle'),
        SpriteAttributes(color='limegreen', shape='circle')
    )


class SnakeGame:
    """Snake game."""

    def __init__(self, config: Config, sprite_config: SpriteConfig) -> None:
        """Initialise SnakeGame.

        Args:
            config: Default configuration settings.
            sprite_config: Sprite attributes.
        """
        turtle.tracer(0)
        self.config = config
        self.sprite_config = sprite_config
        # Default settings.
        width = config.display_width
        height = config.display_height

        # Initialise speed (delay) and scores.
        self.delay = config.initial_update_delay
        self.score = 0
        self.high_score = 0

        # Initialise screen.
        self.screen = turtle.Screen()
        # Setup screen area with border space.
        self.screen.setup(width + config.border * 2,
                          height + config.border * 2)
        self.screen.title("Snake")
        self.screen.bgcolor(config.bg)
        self.draw_scoreboard()
        self.draw_game_area()

        # Screen text
        self.pen = turtle.Turtle()
        self.pen.color(config.text.color)
        self.pen.hideturtle()
        self.pen.goto(0, height // 2 - config.text.v_pos)

        self.snake = Snake(self.config, self.sprite_config)
        self.setup_listeners()

        # Add food
        # food = Food()
        # print(food.xcor(), food.ycor())
        self.update_score()
        self.update()

    def draw_scoreboard(self) -> None:
        """Draw the score area at the top of the screen."""
        height = self.config.scoreboard_height
        width = self.config.display_width
        top = self.config.display_height // 2
        color = self.config.text.bg_color
        self._draw_board_region(width, height, top, color)

    def draw_game_area(self) -> None:
        """Draw the area that we play in."""
        scoreboard_height = self.config.scoreboard_height
        width = self.config.display_width
        height = self.config.display_height - scoreboard_height
        top = self.config.display_height // 2 - scoreboard_height
        color = self.config.board_color
        self._draw_board_region(width, height, top, color)

    @staticmethod
    def _draw_board_region(width: int, height: int, top: int, color: str) -> None:
        """Draw rectangular area the width of the board."""
        board_turtle = turtle.Turtle()
        board_turtle.hideturtle()
        board_turtle.penup()
        # Start at top left corner.
        board_turtle.goto(-width // 2, top)
        board_turtle.pendown()
        board_turtle.color(color)

        board_turtle.begin_fill()
        for distance in (width, height, width, height):
            board_turtle.forward(distance)
            board_turtle.right(90)
        board_turtle.end_fill()

    def setup_listeners(self) -> None:
        """Configure listeners."""
        self.screen.listen()
        for direction, char in KeyBindings.bindings.items():
            fun: Callable = lambda d=direction: self.snake.set_direction(d)
            self.screen.onkeypress(fun, char)

    def update_score(self) -> None:
        """Write current score to screen."""
        self.pen.clear()
        self.pen.write(f"Score : {self.score}  "
                       f"High Score : {self.high_score}", align="center",
                       font=self.config.text.font)

    def update(self) -> None:
        """Main game loop to keep updating the game state."""
        self.snake.move()
        self.check_collision()
        turtle.update()
        self.screen.ontimer(self.update, self.delay)

    def check_collision(self) -> None:
        """Return True if snake collides with edge of board or its tail."""
        x_coord = self.snake.head.xcor()
        y_coord = self.snake.head.ycor()
        half_head_size = self.sprite_config.head_size // 2
        half_width = self.config.display_width // 2

        x_max = half_width - half_head_size
        x_min = -half_width + half_head_size
        y_max = half_width - self.config.scoreboard_height - half_head_size
        y_min = -half_width + half_head_size

        out_of_bounds = not (x_min <= x_coord <= x_max and
                             y_min <= y_coord <= y_max)
        if out_of_bounds:
            print(x_coord, y_coord)  # crash


class Snake:
    """Snake character as compound turtle."""
    # Attribute to check for backtracking.
    _backtrack = {
        Direction.UP: Direction.DOWN,
        Direction.DOWN: Direction.UP,
        Direction.LEFT: Direction.RIGHT,
        Direction.RIGHT: Direction.LEFT
    }

    _move_delta_map: dict[Direction, tuple[float, float]] = {}

    def __init__(self, config: Config, sprite_config: SpriteConfig) -> None:
        self.config = config
        self.sprite_config = sprite_config

        # Map direction of movement to x,y delta.
        if not Snake._move_delta_map:
            Snake.set_move_delta_map(config.move_delta)

        # head of the snake
        self.head = turtle.Turtle()
        self.head.shape(sprite_config.head.shape)
        self.head.color(sprite_config.head.color)
        self.head.penup()
        self.head.goto(0, 0)
        self.head_direction = Direction.STOP
        self.segments: list[turtle.Turtle] = []

    @classmethod
    def set_move_delta_map(cls, delta: float) -> None:
        """Initialize the class-level movement delta map.

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
        if self.head_direction is not Snake._backtrack.get(direction):
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
    sprites = SpriteConfig.food

    def __init__(self) -> None:
        super().__init__()
        self.color(choice(Food.sprites).color)
        self.shape('circle')
        self.penup()

        # Set position
        padding = 20
        x_max = Config.display_width // 2 - padding
        x_min = - x_max
        y_max = Config.display_height // 2 - padding
        y_min = - y_max
        position = randint(x_min, x_max), randint(y_min, y_max)
        self.goto(position)


if __name__ == '__main__':
    game = SnakeGame(Config(), SpriteConfig())
    turtle.Screen().mainloop()
