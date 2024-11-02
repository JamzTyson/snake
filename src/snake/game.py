"""Python / Turtle implementation of classic Snake game."""

import turtle
from random import choice, randint
from dataclasses import dataclass
from enum import Enum, auto
from collections import namedtuple


Sprite = namedtuple('Sprite', ['color', 'shape'])
Text = namedtuple('Text', ['color', 'font', 'v_pos'])


@dataclass
class Config:
    """Configure game defaults."""
    # Game initial default settings.
    initial_delay = 0.1
    initial_score = 0
    initial_high_score = 0

    # Scoreboard text.
    text: Text = Text(color='white',
                      font=("sans", 20, "normal"),
                      v_pos=50)

    # Sprites.
    head: Sprite = Sprite(color='white', shape='square')
    segment: Sprite = Sprite(color='orange', shape='circle')
    # noinspection SpellCheckingInspection
    food: tuple[Sprite, ...] = (Sprite(color='red', shape='circle'),
                                Sprite(color='yellow', shape='circle'),
                                Sprite(color='limegreen', shape='circle'))

    # App window properties.
    screen_width: int = 600
    screen_height: int = 600
    # noinspection SpellCheckingInspection
    background_color: str = 'navyblue'

    @property
    def bg(self) -> str:
        """Alias for background."""
        return self.background_color


class Direction(Enum):
    """Snake direction flags."""
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    STOP = auto()

    @staticmethod
    def is_backtrack(dir_1, dir_2):
        """Return True if directions are opposite."""
        opposites = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        return opposites.get(dir_1) is dir_2


class SnakeGame:
    """Snake game."""

    def __init__(self, config):
        turtle.tracer(0)
        self.config = config
        # Default settings.
        width = config.screen_width
        height = config.screen_height

        # Initialise speed (delay) and scores.
        self.delay = config.initial_delay
        self.score = config.initial_score
        self.high_score = config.initial_high_score

        # Initialise screen.
        self.screen = turtle.Screen()
        self.screen.setup(width, height)
        self.screen.title("Snake")
        self.screen.bgcolor(config.bg)

        # Screen text
        self.pen = turtle.Turtle()
        self.pen.color(config.text.color)
        self.pen.hideturtle()
        self.pen.goto(0, height // 2 - config.text.v_pos)

        self.snake = Snake()
        self.setup_listeners()

        # Add food
        # food = Food()
        # print(food.xcor(), food.ycor())
        self.update_score()
        turtle.update()

    def setup_listeners(self):
        """Configure listeners."""
        self.screen.listen()
        self.screen.onkeypress(
            lambda: self.snake.set_direction(Direction.UP), "Up")
        self.screen.onkeypress(
            lambda: self.snake.set_direction(Direction.DOWN), "Down")
        self.screen.onkeypress(
            lambda: self.snake.set_direction(Direction.LEFT), "Left")
        self.screen.onkeypress(
            lambda: self.snake.set_direction(Direction.RIGHT), "Right")

    def update_score(self):
        """Write current score to screen."""
        self.pen.clear()
        self.pen.write(f"Score : {self.score}  "
                       f"High Score : {self.high_score}", align="center",
                       font=self.config.text.font)


class Snake:
    """Snake character as compound turtle."""
    config = Config()

    def __init__(self):
        # head of the snake
        self.head = turtle.Turtle()
        self.head.shape(Snake.config.head.shape)
        self.head.color(Snake.config.head.color)
        self.head.penup()
        self.head.goto(0, 0)
        self.head_direction = Direction.STOP
        self.segments = []

    def set_direction(self, direction: Direction):
        """Set snake head direction.

        Snake cannot double back on itself."""
        if not Direction.is_backtrack(direction, self.head_direction):
            self.head_direction = direction
        print(self.head_direction)

    def add_segment(self):
        """Add one body segment."""
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color(Snake.config.segment.color)
        new_segment.penup()
        self.segments.append(new_segment)


class Food(turtle.Turtle):
    """Sprites to be collected."""
    sprites = Config().food

    def __init__(self):
        super().__init__()
        self.color(choice(Food.sprites).color)
        self.shape('circle')
        self.penup()

        # Set position
        padding = 20
        x_max = Config.screen_width // 2 - padding
        x_min = - x_max
        y_max = Config.screen_height // 2 - padding
        y_min = - y_max
        position = randint(x_min, x_max), randint(y_min, y_max)
        self.goto(position)


if __name__ == '__main__':
    # Init game instance.
    game = SnakeGame(Config())

    turtle.Screen().mainloop()
