"""User interface.

 Draws and manages screen elements in the Snake game.
 Handles the setup of the game screen, drawing the game area,
scoreboard, and updating the score display.
"""

import turtle

from snake.config import Config, SpriteConfig
from snake.constants import TextAttributes
from snake.game_state import GameState


# Typehint alias
Pen = turtle.Turtle


class ScreenManager:
    """Draw and manage screen areas."""
    def __init__(self, config: Config, sprite_config: SpriteConfig):
        """Initialise ScreenManager.

        Args:
            config (Config): Main configuration settings.
            sprite_config (SpriteConfig): Cofig settings for sprite Turtles.
        """
        self.config = config
        self.sprite_config = sprite_config
        self.screen = turtle.Screen()

        # Create Turtles for drawing and writing.
        self.scoreboard_pen = turtle.Turtle()  # Writes scores at top.
        # Writes eaten food score value. As this is never cleared, this
        # pen only needs to have its attributes set once.
        self.splash_pen = turtle.Turtle()
        self.set_pen_attributes(self.splash_pen, self.config.splash_text)

        self.graphics_pen = turtle.Turtle()  # Draws board regions.

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

    @staticmethod
    def set_pen_attributes(pen: Pen, attributes: TextAttributes) -> None:
        """Clear pen and set or reset pen attributes."""
        pen.clear()
        pen.hideturtle()
        pen.penup()
        pen.color(attributes.color)

    def draw_scoreboard(self) -> None:
        """Draw the score area at the top of the screen."""
        height = self.config.scoreboard_height
        width = self.config.display_width
        top = self.config.display_height // 2
        color = self.config.scoreboard_text.bg_color
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
        self.set_pen_attributes(self.scoreboard_pen,
                                self.config.scoreboard_text)

        vpos = ((self.config.display_height // 2)
                - self.config.scoreboard_height)
        self.scoreboard_pen.goto(0, vpos)

        self.scoreboard_pen.write(
            f"Score : {game_state.current_score}  "
            f"High Score : {game_state.best_score}", align="center",
            font=self.config.scoreboard_text.font
        )

    def score_splash(self, value: int) -> None:
        """Display last score for a few seconds.

        Note:
            As we do not call clear() on this turtle, it is not
            necessary to re-initialise attributes.
        """
        self.splash_pen.home()
        self.splash_pen.write(f"{value:+}", font=self.config.scoreboard_text.font)
        self.screen.ontimer(self.splash_pen.undo, 500)
