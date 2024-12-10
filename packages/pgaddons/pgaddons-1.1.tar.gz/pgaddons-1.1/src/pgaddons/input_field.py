from .base_class import BaseClass
from .errors import *

try:
    import pygame as pg

except ImportError:
    raise PygameNotInstalled()


class InputField(BaseClass):
    def __init__(self, pos: list[int, int] | tuple[int, int], size: list[int, int] | tuple[int, int], colour, active_colour, background_text: str | list = "",
                 font_colour: str | tuple[int, int, int] | pg.Color = pg.Color("white"),
                 font: str | type[pg.font.Font] | type[pg.font.SysFont] = "freesansbold",
                 font_size=30, max_length=10):

        super().__init__(pos, size, colour)
        self.active_colour = active_colour
        self.font_colour = font_colour
        self.font_size = font_size
        self.text = ""
        self.bg_text = background_text
        self.active = False
        self.locked = False
        self.max_length = max_length
        if isinstance(font, str):
            self.font = font.lower()
            if self.font.removesuffix(".ttf") not in pg.font.get_fonts() and self.font != "freesansbold":
                raise InvalidFont(self.font)

            else:
                self.font = pg.font.SysFont(font, font_size)

        else:
            self.font = font

    def draw(self, screen):
        pg.draw.rect(screen, self.colour if not self.active else self.active_colour,
                     (self.x, self.y, self.width, self.height))
        if not self.text:
            if isinstance(self.bg_text, str):
                text = self.font.render(self.bg_text, True, self.font_colour)
                screen.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

            else:
                for line in self.bg_text:
                    text = self.font.render(line, True, self.font_colour)
                    screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                                       self.y + (self.height / 2 - text.get_height() / 2) + (
                                                   self.bg_text.index(line) * text.get_height())))
        else:
            text = self.font.render(self.text, True, self.font_colour)
            screen.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def on_key_press(self, key):
        if self.active:
            if key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < self.max_length:
                self.text += pg.key.name(key)
