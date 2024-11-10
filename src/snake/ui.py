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
        self.text_pen = turtle.Turtle()
        self.graphics_pen = turtle.Turtle()

        self.setup_screen()

    def setup_screen(self):
        """Setup screen properties and initialise the board."""
        turtle.tracer(0)  # pylint: disable=no-member
        width = self.config.display_width
        height = self.config.display_height

        # Setup screen area with border space.
        self.screen.setup(width + self.config.border * 2,
                          height + self.config.border * 2)
        self.screen.title("Snake")
        self.screen.bgcolor(self.config.bg)

        self.draw_scoreboard()
        self.draw_game_area()

        # Screen text
        self.text_pen.color(self.config.text.color)
        self.text_pen.hideturtle()
        self.text_pen.penup()
        self.text_pen.goto(0, height // 2 - self.config.text.v_pos)

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

    def _draw_board_region(self, width: int,
                           height: int,
                           top: int,
                           color: str) -> None:
        """Draw rectangular area the width of the board."""
        self.graphics_pen.hideturtle()
        self.graphics_pen.penup()
        # Start at top left corner.
        self.graphics_pen.goto(-width // 2, top)
        self.graphics_pen.pendown()
        self.graphics_pen.color(color)

        self.graphics_pen.begin_fill()
        for distance in (width, height, width, height):
            self.graphics_pen.forward(distance)
            self.graphics_pen.right(90)
        self.graphics_pen.end_fill()

    def update_score(self, game_state: GameState) -> None:
        """Write current score to screen."""
        self.text_pen.clear()
        self.text_pen.write(
            f"Score : {game_state.current_score}  "
            f"High Score : {game_state.best_score}", align="center",
            font=self.config.text.font
        )
