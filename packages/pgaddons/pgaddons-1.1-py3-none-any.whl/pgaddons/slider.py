from .base_class import BaseClass
from .errors import *
from math import ceil

try:
    import pygame as pg

except ImportError:
    raise PygameNotInstalled()


class Slider(BaseClass):

    def __init__(self, pos: list[int, int] | tuple[int, int], size: list[int, int] | tuple[int, int], colour: tuple[int, int, int] | pg.Color, border_colour: tuple[int, int, int] | pg.Color,
                 min_value: int, max_value: int, start_value: int,
                 border_size: int = 3,
                 background_text: str = "",
                 font: str | type[pg.font.Font] | type[pg.font.SysFont] = "freesansbold",
                 font_size=25, font_colour: str | tuple[int, int, int] | pg.Color = pg.Color("white")):

        super().__init__(pos, size, colour)

        # Border Variables
        self.border_colour = border_colour
        self.border_size = border_size

        # Value Variables
        self.min_value = min_value
        self.max_value = max_value
        self.start_value = start_value
        if self.start_value > self.max_value:
            self.start_value = self.max_value
        self.amount_of_values = self.max_value - self.min_value
        self.distance_between_values = self.width / self.amount_of_values

        # Circle Variables
        self.circle_radius = round(self.height / 2) - self.border_size * 2
        # Clamp the circle to the slider
        self.circle_x = max(min((self.x + self.width) - self.circle_radius, round(self.width * (self.start_value / self.max_value))), self.x + self.circle_radius)
        self.circle_y = self.y + round(self.height / 2)

        # Interaction Variables
        self.is_being_dragged = False
        self.can_be_dragged = True

        # Font Variables
        self.bg_text = background_text
        self.font_colour = font_colour
        if isinstance(font, str):
            self.font = font.lower()
            if self.font.removesuffix(".ttf") not in pg.font.get_fonts() and self.font != "freesansbold":
                raise InvalidFont(self.font)
            
            else:
                self.font = pg.font.SysFont(font, font_size)

        else:
            self.font = font

    def draw(self, screen):
        pg.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height), round(self.height / 2), ceil(self.height / 2))
        pg.draw.rect(screen, self.border_colour, (self.x, self.y, self.width, self.height), self.border_size, ceil(self.height / 2))
        text = self.font.render(self.bg_text, True, self.font_colour)
        screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))
        pg.draw.circle(screen, self.border_colour, (self.circle_x, self.circle_y), round(self.height / 2) - self.border_size * 2)
        text = self.font.render(str(self.start_value), True, self.font_colour)
        screen.blit(text, (self.circle_x - text.get_width() / 2, self.circle_y - text.get_height() / 2))

    def handle_mousedown(self, mouse_pos: tuple[int, int]):
        if self.can_be_dragged:
            mouse_x, mouse_y = mouse_pos

            # distance = (center_x - mouse_x, center_y - mouse_y)
            # use pythagoras to check if the mouse is inside the circle

            circle_center = (self.circle_x, self.circle_y)
            distance = (circle_center[0] - mouse_x, circle_center[1] - mouse_y)
            if distance[0]**2 + distance[1]**2 > self.circle_radius**2:
                return
            else:
                self.is_being_dragged = True

    def handle_mousemotion(self, mouse_pos: tuple[int, int]):
        if self.is_being_dragged:
            mouse_x, mouse_y = mouse_pos
            # Clamp the circle to the slider
            self.circle_x = max(min((self.x + self.width) - self.circle_radius, mouse_x), self.x + self.circle_radius)

            self.start_value = round((self.circle_x - self.x - self.circle_radius) / (self.width - 2 * self.circle_radius) * self.amount_of_values + self.min_value)
