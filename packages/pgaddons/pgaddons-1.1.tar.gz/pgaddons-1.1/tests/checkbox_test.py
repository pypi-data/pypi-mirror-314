from pgaddons import CheckBox, is_clicked
import pygame as pg

width = height = 500
pg.init()
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Button Test")
checkbox = CheckBox((225, 225), (50, 50), "grey 75", "grey 25")
clock = pg.time.Clock()

running = True
while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.MOUSEBUTTONDOWN:
            if is_clicked(checkbox):
                checkbox.on_click()

    screen.fill(pg.Color("white"))

    text = pg.font.SysFont("verdana", 25).render(f"The checkbox is currently set to {checkbox.active}.", True, pg.Color("grey 33"))
    text_rect = text.get_rect()
    text_rect.center = (width / 2, 133)
    screen.blit(text, text_rect)

    clock.tick(60)
    checkbox.draw(screen)
    pg.display.update()
