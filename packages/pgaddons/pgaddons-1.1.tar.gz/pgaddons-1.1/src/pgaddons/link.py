from .errors import *

try:
    import pygame as pg
except ImportError:
    raise PygameNotInstalled()


class Link:
    def __init__(self, pos: list[int, int] | tuple[int, int], text: str, url: str,
                 font: str | type[pg.font.Font] | type[pg.font.SysFont] = "freesansbold",
                 font_size=30, font_colour: str | tuple[int, int, int] | pg.Color = pg.Color("white"), underline=True):

        self.x = pos[0]
        self.y = pos[1]
        self.font_colour = font_colour
        self.underline = underline
        self.text = text
        self.url = url

        if isinstance(font, str):
            self.font = font.lower()
            if self.font.removesuffix(".ttf") not in pg.font.get_fonts() and self.font != "freesansbold":
                raise InvalidFont(self.font)

            else:
                self.font = pg.font.SysFont(font, font_size)

        else:
            self.font = font

    def draw(self, screen):
        text = self.font.render(self.text, True, self.font_colour)
        self.font.set_underline(self.underline)
        screen.blit(text, (self.x, self.y))

    def handle_mousedown(self, event):
        if self.x < event.pos[0] < self.x + self.font.size(self.text)[0] and self.y < event.pos[1] < self.y + \
                self.font.size(self.text)[1]:
            self.on_click()

    def on_click(self):
        import webbrowser
        webbrowser.open(self.url)
