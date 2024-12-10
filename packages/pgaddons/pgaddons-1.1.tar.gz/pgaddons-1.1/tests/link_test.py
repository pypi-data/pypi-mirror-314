import pygame as p
from pgaddons import Link


def main():
    p.init()
    screen = p.display.set_mode((500, 500))
    p.display.set_caption("Link Test")
    link = Link((100, 100), "GitHub", "https://www.github.com/iamdeedz/pygame-addons")
    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

            if event.type == p.MOUSEBUTTONDOWN:
                link.handle_mousedown(event)

        screen.fill((0, 0, 0))
        link.draw(screen)
        p.display.update()


if __name__ == '__main__':
    main()
