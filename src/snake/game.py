"""Python / Turtle implementation of classic Snake game."""

import turtle
from random import choice, randint
from dataclasses import dataclass
from enum import Enum, auto


@dataclass
class ConfigColor:
    """Configure default game colours."""
    text: str = 'white'
    # noinspection SpellCheckingInspection
    background: str = 'navyblue'
    head: str = 'white'
    segment: str = 'orange'
    # noinspection SpellCheckingInspection
    food: tuple[str] = ('red', 'yellow', 'limegreen')

    @property
    def bg(self) -> str:
        """Alias for background."""
        return self.background


@dataclass
class ConfigShapes:
    """Configure default Turtle shapes."""
    head: str = 'square'
    segment: str = 'circle'


@dataclass
class ConfigWindow:
    """Configure default app window."""
    screen_width: int = 600
    screen_height: int = 600


class Direction(Enum):
    """Snake direction flags."""
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    STOP = auto()

    @staticmethod
    def is_backtrack(dir_1, dir_2):
        opposites = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        return opposites.get(dir_1) is dir_2


class SnakeGame:
    """Snake game."""

    def __init__(self):
        turtle.tracer(0)
        # Default settings.
        color = ConfigColor()
        width = ConfigWindow.screen_width
        height = ConfigWindow.screen_height
        text_height = 50
        font = "sans", 20, "normal"

        # Score:
        self.current_score = 0
        self.high_score = 0

        # Initialise screen.
        self.screen = turtle.Screen()
        self.screen.setup(width, height)
        self.screen.title("Snake")
        self.screen.bgcolor(color.bg)

        # Screen text
        pen = turtle.Turtle()
        pen.color(color.text)
        pen.penup()
        pen.hideturtle()
        pen.goto(0, height // 2 - text_height)
        pen.write(f"Score : {self.current_score}  "
                  f"High Score : {self.high_score}", align="center",
                  font=font)

        self.snake = Snake()
        self.setup_listeners()

        # Add food
        # food = Food()
        # print(food.xcor(), food.ycor())

        turtle.update()

    def setup_listeners(self):
        """Configure listeners."""
        self.screen.listen()
        self.screen.onkeypress(lambda: self.snake.set_direction(Direction.UP), "Up")
        self.screen.onkeypress(lambda: self.snake.set_direction(Direction.DOWN), "Down")
        self.screen.onkeypress(lambda: self.snake.set_direction(Direction.LEFT), "Left")
        self.screen.onkeypress(lambda: self.snake.set_direction(Direction.RIGHT), "Right")


class Snake:
    """Snake character as compound turtle."""
    color = ConfigColor()
    shape = ConfigShapes()

    def __init__(self):
        # head of the snake
        self.head = turtle.Turtle()
        self.head.shape(Snake.shape.head)
        self.head.color(Snake.color.head)
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
        new_segment.color(Snake.color.segment)
        new_segment.penup()
        self.segments.append(new_segment)


class Food(turtle.Turtle):
    """Sprites to be collected."""
    colors = ConfigColor().food

    def __init__(self):
        super().__init__()
        self.color(choice(Food.colors))
        self.shape('circle')
        self.penup()

        # Set position
        padding = 20
        x_max = ConfigWindow.screen_width // 2 - padding
        x_min = - x_max
        y_max = ConfigWindow.screen_height // 2 - padding
        y_min = - y_max
        position = randint(x_min, x_max), randint(y_min, y_max)
        self.goto(position)


if __name__ == '__main__':
    delay = 0.1
    score = 0
    high_score = 0

    # Init game instance.
    game = SnakeGame()

    turtle.Screen().mainloop()
