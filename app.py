import pygame as pg
from tetris_objects import *
pg.init()

WIDTH = 1000
HEIGHT = 1000
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))


def draw_grid(screen):
    spacing = 25
    for _ in range(35):
        if _ == 34:
            pg.draw.rect(screen, (0, 0, 0), pg.rect.Rect(250, spacing, 500, 8))
        else:
            pg.draw.rect(screen, (0, 0, 0), pg.rect.Rect(250, spacing, 500, 2))
        spacing += 25
    spacing = 25
    for _ in range(21):
        if _ == 0:
            pg.draw.rect(screen, (0, 0, 0), pg.rect.Rect(217 + spacing, 0, 8, 883))
        elif _ == 20:
            pg.draw.rect(screen, (0, 0, 0), pg.rect.Rect(225 + spacing, 0, 8, 883))
        else:
            pg.draw.rect(screen, (0, 0, 0), pg.rect.Rect(225 + spacing, 0, 2, 883))
        spacing += 25


vincent = Cube("green", 250, 50)

def main():
    playgame = True
    while playgame:
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
