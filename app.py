import pygame as pg
from tetris_objects import *
pg.init()

WIDTH = 700
HEIGHT = 700
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
CLOCK = pg.time.Clock()
PIECE_MOVE = pg.event.Event(pg.USEREVENT + 1)

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


vincent = Tpiece()

def main():
    piece_move = True
    playgame = True
    while playgame:
        CLOCK.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                playgame = False
            elif event == PIECE_MOVE:
                piece_move = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    vincent.rotate()
                elif event.key == pg.K_LEFT:
                    vincent.move("left")
                elif event.key == pg.K_RIGHT:
                    vincent.move("right")
        SCREEN.fill((50, 50, 50))

        draw_grid(SCREEN)
        if piece_move:
            vincent.move("down")
            piece_move = False
            pg.time.set_timer(PIECE_MOVE, 1000)
        vincent.draw(SCREEN)

        pg.display.update()
    pg.quit()

if __name__ == "__main__":
    main()
