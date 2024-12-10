import pygame as pg
from pgaddons import InputField

width = height = 500
fps = 30


def main():
    pg.init()
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption("Input Field Test")
    input_field = InputField((175, 212.5), (150, 75), pg.Color("grey 33"), pg.Color("grey 50"),
                             background_text="Type Here", font_colour=pg.Color("grey 66"), font="verdana", font_size=25)
    clock = pg.time.Clock()

    running = True
    while running:

        screen.fill(pg.Color("white"))

        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False

            elif e.type == pg.MOUSEBUTTONDOWN:
                if input_field.x < pg.mouse.get_pos()[0] < input_field.x + input_field.width and input_field.y < pg.mouse.get_pos()[1] < input_field.y + input_field.height:
                    input_field.active = True

                else:
                    input_field.active = False

            elif e.type == pg.KEYDOWN:
                input_field.on_key_press(e.key)

        clock.tick(fps)
        input_field.draw(screen)
        pg.display.update()


if __name__ == "__main__":
    main()
