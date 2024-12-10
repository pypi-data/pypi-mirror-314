from pgaddons import Slider
import pygame as p


p.init()
screen = p.display.set_mode((500, 500))
p.display.set_caption("Slider Test")
clock = p.time.Clock()
slider = Slider((0, 0), (300, 50), p.Color("lightgrey"), p.Color("grey25"), 50, 100, 100, font_size=20)

running = True
while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False

        elif event.type == p.MOUSEBUTTONDOWN:
            slider.handle_mousedown(p.mouse.get_pos())

        elif event.type == p.MOUSEBUTTONUP:
            slider.is_being_dragged = False

        elif event.type == p.MOUSEMOTION:
            slider.handle_mousemotion(p.mouse.get_pos())

    screen.fill((0, 0, 0))
    slider.draw(screen)
    font = p.font.SysFont("freesansbold", 30)
    text = font.render(str(slider.value), True, p.Color("white"))
    screen.blit(text, (0, 250))
    p.display.update()
    clock.tick(60)
