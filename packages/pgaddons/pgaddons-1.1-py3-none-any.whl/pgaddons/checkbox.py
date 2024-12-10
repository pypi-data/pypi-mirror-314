from .errors import *
from .base_class import *

try:
    import pygame as pg
except ImportError:
    raise PygameNotInstalled()


class CheckBox(BaseClass):
    """
    A class that generates at checkbox at the given pos.
    """

    def __init__(self, pos: list[int, int] | tuple[int, int], size: list[int, int] | tuple[int, int],
                 inactive_colour: str | tuple[int, int, int] | pg.Color,
                 active_colour: str | tuple[int, int, int] | pg.Color, active: True | False = False):

        super().__init__(pos, size, inactive_colour)

        self.active_colour = active_colour
        self.inactive_colour = inactive_colour
        self.active = active

    def draw(self, screen):
        colour = self.active_colour if self.active else self.inactive_colour
        pg.draw.rect(screen, colour, (self.x, self.y, self.width, self.height))

    def on_click(self):
        self.active = not self.active
