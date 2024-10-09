import pygame as pg
from tetris_objects import *
import random
pg.init()

WIDTH = 700
HEIGHT = 700
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
CLOCK = pg.time.Clock()
PIECE_MOVEDOWN = pg.event.Event(pg.USEREVENT + 1)


def main():
    player_score = 0
    game_loose = False
    playgame = True
    tetrismap = TetrisMap(SCREEN)

    piece = random.choice([Tpiece("purple"), Ipiece("light_blue"), Jpiece("blue")])
    pg.time.set_timer(PIECE_MOVEDOWN, 120)
    while playgame:
        CLOCK.tick(60)
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                playgame = False

        SCREEN.fill((70, 70, 70))
        tetrismap.draw()

        if not game_loose:
            for event in events:
                if event == PIECE_MOVEDOWN:
                    has_moved = piece.move(tetrismap, "down")
                    if has_moved:
                        pg.time.set_timer(PIECE_MOVEDOWN, 120)
                    elif len(tetrismap.out_of_bounds) > 0:
                        game_loose = True
                    else:
                        tetrismap.add(piece)
                        player_score += tetrismap.delete_completed_rows()
                        piece = random.choice([Tpiece("purple"), Ipiece("light_blue"), Jpiece("blue")])
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE: 
                        piece.rotate(tetrismap)
                    elif event.key == pg.K_LEFT:
                        piece.move(tetrismap, "left")
                    elif event.key == pg.K_RIGHT:
                        piece.move(tetrismap, "right")

        for row_index in range(0, 20):
            for cube in tetrismap[row_index]:
                if cube.rect.y // 25 != row_index:
                    cube.rect.y += 5

        piece.draw(SCREEN)
        pg.display.update()
    pg.quit()

if __name__ == "__main__":
    main() 
