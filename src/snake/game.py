"""Python / Turtle implementation of classic Snake game."""

import turtle
# from time import sleep
from random import choice, randint
from dataclasses import dataclass
from enum import Enum, auto


@dataclass
class ColorConfig:
    """Configure default game colours."""
    text: str = 'white'
    background: str = 'navyblue'
    head: str = 'white'
    segment: str = 'orange'
    food: tuple[str] = ('red', 'yellow', 'limegreen')

    @property
    def bg(self) -> str:
        """Alias for bacground."""
        return self.background


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


class SnakeGame:
    """Snake game."""

    def __init__(self):
        turtle.tracer(0)
        # Default settings.
        color = ColorConfig()
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

        # Draw snake
        self.snake = Snake()

        # Add food
        food = Food()
        # print(food.xcor(), food.ycor())

        turtle.update()


class Snake:
    """Snake character as compound turtle."""

    def __init__(self):
        color = ColorConfig()
        # head of the snake
        self.head = turtle.Turtle()
        self.head.shape("square")
        self.head.color(color.head)
        self.head.penup()
        self.head.goto(0, 0)
        self.head.direction = Direction.STOP


class Food(turtle.Turtle):
    """Sprites to be collected."""
    colors = ColorConfig().food

    def __init__(self):
        super().__init__()
        self.color(choice(Food.colors))
        self.shape('circle')
        self.penup()

        # Set position
        padding = 20
        xmax = ConfigWindow.screen_width // 2 - padding
        xmin = - xmax
        ymax = ConfigWindow.screen_height // 2 - padding
        ymin = - ymax
        position = randint(xmin, xmax), randint(ymin, ymax)
        self.goto(position)


if __name__ == '__main__':
    delay = 0.1
    score = 0
    high_score = 0

    # Init game instance.
    game = SnakeGame()

    turtle.Screen().mainloop()
