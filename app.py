import pygame as pg
from tetris_objects import *
pg.init()

WIDTH = 700
HEIGHT = 700
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
CLOCK = pg.time.Clock()

def draw_grid(screen):
    spacing = 25
    for _ in range(20):
        if _ == 19:
            pg.draw.rect(screen, (0, 0, 0), pg.rect.Rect(225, spacing - 1, 250, 8))
        else:
            pg.draw.rect(screen, (0, 0, 0), pg.rect.Rect(225, spacing - 1, 250, 2))
        spacing += 25
    spacing = 25
    for _ in range(11):
        if _ == 0:
            pg.draw.rect(screen, (0, 0, 0), pg.rect.Rect(193 + spacing, 0, 8, 507))
        elif _ == 10:
            pg.draw.rect(screen, (0, 0, 0), pg.rect.Rect(199 + spacing, 0, 8, 507))
        else:
            pg.draw.rect(screen, (0, 0, 0), pg.rect.Rect(199 + spacing, 0, 2, 507))
        spacing += 25


vincent = Cube("green", 250, 50)

def main():
    playgame = True
    while playgame:
        CLOCK.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                playgame = False
        SCREEN.fill((50, 50, 50))
        draw_grid(SCREEN)
        vincent.draw(SCREEN)
        pg.display.update()
    pg.quit()

if __name__ == "__main__":
    main()
