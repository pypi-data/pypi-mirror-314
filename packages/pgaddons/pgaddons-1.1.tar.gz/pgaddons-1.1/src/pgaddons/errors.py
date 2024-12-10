class InvalidFont(Exception):
    def __init__(self, font):
        self.font = font
        super().__init__(f"Invalid font: {self.font}. Please use a font from pygame.font.get_fonts()")


class PygameNotInstalled(Exception):
    def __init__(self):
        super().__init__("Pygame is not installed. This package requires pygame to be installed.")
