import pygame as pg
from tetris_objects import *
import random
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


def main():
    game_loose = False
    piece_move_down = True
    playgame = True
    tetrismap = TetrisMap()

    piece = random.choice([Tpiece("purple"), Ipiece("light_blue"), Jpiece("blue")])
    while playgame:
        CLOCK.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                playgame = False
            elif not game_loose:
                if event == PIECE_MOVE:
                    piece_move_down = True
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE: 
                        piece.rotate(tetrismap)
                    elif event.key == pg.K_LEFT:
                        piece.move(tetrismap, "left")
                    elif event.key == pg.K_RIGHT:
                        piece.move(tetrismap, "right")

        SCREEN.fill((70, 70, 70))
        draw_grid(SCREEN)
        tetrismap.drawcubes(SCREEN)

        if piece_move_down:
            piece_move_down = False 
            moved = piece.move(tetrismap, "down")
            if not moved:
                tetrismap.add(piece)
                if len(tetrismap.out_of_bounds) > 0:
                    game_loose = True
                else:
                    piece = random.choice([Tpiece("purple"), Ipiece("light_blue"), Jpiece("blue")])
            if not game_loose:
                pg.time.set_timer(PIECE_MOVE, 120)

        complete_rows = tetrismap.complete_rows()
        for row in complete_rows:
            del tetrismap.rows[row]
            tetrismap.rows.insert(0, [])
        for row_index in range(0, 20):
            for cube in tetrismap[row_index]:
                if cube.rect.y // 25 != row_index:
                    cube.rect.y += 1

        piece.draw(SCREEN)
        pg.display.update()
    pg.quit()

if __name__ == "__main__":
    main() 
