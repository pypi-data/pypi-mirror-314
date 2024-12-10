from pgaddons import Button
import pygame as pg

width = height = 500
pg.init()
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Button Test")
button = Button((150, 250), (175, 112.5), pg.Color("grey 33"), text="Hello World", font_colour=pg.Color("grey 66"),
                font="verdana", font_size=25)
clock = pg.time.Clock()
x = 0


def on_click():
    global x
    x += 1


button.on_click = on_click

running = True
while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.MOUSEBUTTONDOWN:
            if button.x < pg.mouse.get_pos()[0] < button.x + button.width and button.y < pg.mouse.get_pos()[1] < button.y + button.height:
                button.on_click()

    screen.fill(pg.Color("white"))

    text = pg.font.SysFont("verdana", 25).render(f"The button was clicked {x} times.", True, pg.Color("grey 33"))
    text_rect = text.get_rect()
    text_rect.center = (width / 2, 133)
    screen.blit(text, text_rect)

    clock.tick(60)
    button.draw(screen)
    pg.display.update()
