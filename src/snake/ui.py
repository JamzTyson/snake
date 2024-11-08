"""User interface.

 Draws and manages screen elements in the Snake game.
 Handles the setup of the game screen, drawing the game area,
scoreboard, and updating the score display.
"""

import turtle

from snake.config import Config, SpriteConfig
from snake.game_state import GameState


class ScreenManager:
    """Draw and manage screen areas."""
    def __init__(self, config: Config, sprite_config: SpriteConfig):
        self.config = config
        self.sprite_config = sprite_config
        self.screen = turtle.Screen()
        self.pen = turtle.Turtle()

        self.setup_screen()

    def setup_screen(self):
        """Setup screen properties and initialise the board."""
        turtle.tracer(0)  # pylint: disable=no-member
        width = self.config.display_width
        height = self.config.display_height

        self.screen = turtle.Screen()
        # Setup screen area with border space.
        self.screen.setup(width + self.config.border * 2,
                          height + self.config.border * 2)
        self.screen.title("Snake")
        self.screen.bgcolor(self.config.bg)

        self.draw_scoreboard()
        self.draw_game_area()

        # Screen text
        self.pen.color(self.config.text.color)
        self.pen.hideturtle()
        self.pen.goto(0, height // 2 - self.config.text.v_pos)

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
    def _draw_board_region(width: int,
                           height: int,
                           top: int,
                           color: str) -> None:
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

    def update_score(self, game_state: GameState) -> None:
        """Write current score to screen."""
        self.pen.clear()
        self.pen.write(f"Score : {game_state.scores.current}  "
                       f"High Score : {game_state.scores.best}", align="center",
                       font=self.config.text.font)
