"""Python / Turtle implementation of classic Snake game."""

import turtle
from random import choice, randint
from dataclasses import dataclass
from enum import Enum, auto
from collections import namedtuple


Sprite = namedtuple('Sprite', ['color', 'shape'])
Text = namedtuple('Text', ['color', 'bg_color', 'font', 'v_pos'])


class Direction(Enum):
    """Snake direction flags."""
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    STOP = auto()


@dataclass
class Config:
    """Configure game defaults."""
    # Game initial default settings.
    initial_update_delay = 25  # milliseconds
    initial_score = 0
    initial_high_score = 0
    move_delta = 5  # Distance to move in x,y directions per step.

    # Scoreboard.
    scoreboard_height: int = 50
    text: Text = Text(color='white',
                      bg_color='black',
                      font=("sans", 20, "normal"),
                      v_pos=50)

    # Sprites.
    head: Sprite = Sprite(color='white', shape='square')
    segment: Sprite = Sprite(color='orange', shape='circle')
    head_size: int = 20  # px size of head.
    # noinspection SpellCheckingInspection
    food: tuple[Sprite, ...] = (Sprite(color='red', shape='circle'),
                                Sprite(color='yellow', shape='circle'),
                                Sprite(color='limegreen', shape='circle'))

    # Map direction of movement to x,y delta.
    move_delta_map = {
        Direction.UP: (0, move_delta),
        Direction.DOWN: (0, -move_delta),
        Direction.LEFT: (-move_delta, 0),
        Direction.RIGHT: (move_delta, 0)
    }

    key_bindings = {
        "Up": Direction.UP,
        "Down": Direction.DOWN,
        "Left": Direction.LEFT,
        "Right": Direction.RIGHT,
        "space": Direction.STOP
    }

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


class SnakeGame:
    """Snake game."""

    def __init__(self, config):
        turtle.tracer(0)
        self.config = config
        # Default settings.
        width = config.display_width
        height = config.display_height

        # Initialise speed (delay) and scores.
        self.delay = config.initial_update_delay
        self.score = config.initial_score
        self.high_score = config.initial_high_score

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

        self.snake = Snake()
        self.setup_listeners()

        # Add food
        # food = Food()
        # print(food.xcor(), food.ycor())
        self.update_score()
        self.update()

    def draw_scoreboard(self):
        """Draw the score area at the top of the screen."""
        height = self.config.scoreboard_height
        width = self.config.display_width
        top = self.config.display_height // 2

        scoreboard_turtle = turtle.Turtle()
        scoreboard_turtle.hideturtle()
        scoreboard_turtle.penup()
        # Start at top left corner.
        scoreboard_turtle.goto(-width // 2, top)
        scoreboard_turtle.pendown()
        scoreboard_turtle.color(self.config.text.bg_color)

        scoreboard_turtle.begin_fill()
        for distance in (width, height, width, height):
            scoreboard_turtle.forward(distance)
            scoreboard_turtle.right(90)
        scoreboard_turtle.end_fill()

    def draw_game_area(self):
        """Draw the area that we play in."""
        scoreboard_height = self.config.scoreboard_height
        width = self.config.display_width
        top = self.config.display_height // 2 - scoreboard_height
        height = self.config.display_height - scoreboard_height

        board_turtle = turtle.Turtle()
        board_turtle.hideturtle()
        board_turtle.penup()
        # Start at top left corner.
        board_turtle.goto(-width // 2, top)
        board_turtle.pendown()
        board_turtle.color(self.config.board_color)

        board_turtle.begin_fill()
        for distance in (width, height, width, height):
            board_turtle.forward(distance)
            board_turtle.right(90)
        board_turtle.end_fill()

    def setup_listeners(self):
        """Configure listeners."""
        self.screen.listen()
        for key, direction in self.config.key_bindings.items():
            self.screen.onkeypress(
                lambda d=direction: self.snake.set_direction(d), key)

    def update_score(self):
        """Write current score to screen."""
        self.pen.clear()
        self.pen.write(f"Score : {self.score}  "
                       f"High Score : {self.high_score}", align="center",
                       font=self.config.text.font)

    def update(self):
        """Main game loop to keep updating the game state."""
        self.snake.move()
        self.check_collision()
        turtle.update()
        self.screen.ontimer(self.update, int(self.delay))

    def check_collision(self):
        """Return True if snake collides with edge of board or its tail."""
        x_coord = self.snake.head.xcor()
        y_coord = self.snake.head.ycor()
        half_head_size = self.config.head_size // 2
        half_width = self.config.display_width // 2

        x_max = half_width - half_head_size
        x_min = -half_width + half_head_size
        y_max = half_width - self.config.scoreboard_height - half_head_size
        y_min = -half_width + half_head_size

        out_of_bounds = not (x_min <= x_coord <= x_max and y_min <= y_coord <= y_max)
        if out_of_bounds:
            print(x_coord, y_coord)  # crash


class Snake:
    """Snake character as compound turtle."""
    config = Config()

    # Attribute to check for backtracking.
    _backtrack = {
        Direction.UP: Direction.DOWN,
        Direction.DOWN: Direction.UP,
        Direction.LEFT: Direction.RIGHT,
        Direction.RIGHT: Direction.LEFT
    }

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

        Snake cannot double back on itself.
        """
        if self.head_direction is not Snake._backtrack.get(direction):
            self.head_direction = direction

    def add_segment(self):
        """Add one body segment."""
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color(Snake.config.segment.color)
        new_segment.penup()
        self.segments.append(new_segment)

    def move(self):
        """Update snake position."""
        if self.head_direction is not Direction.STOP:
            delta_x, delta_y = self.config.move_delta_map[self.head_direction]
            new_x = self.head.xcor() + delta_x
            new_y = self.head.ycor() + delta_y
            self.head.goto(new_x, new_y)


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
        x_max = Config.display_width // 2 - padding
        x_min = - x_max
        y_max = Config.display_height // 2 - padding
        y_min = - y_max
        position = randint(x_min, x_max), randint(y_min, y_max)
        self.goto(position)


if __name__ == '__main__':
    # Init game instance.
    game = SnakeGame(Config())

    turtle.Screen().mainloop()
