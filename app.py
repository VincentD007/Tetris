import pygame as pg
from tetromino_class import *
import random
pg.init()

WIDTH = 700
HEIGHT = 700
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
CLOCK = pg.time.Clock()
PIECE_MOVEDOWN = pg.event.Event(pg.USEREVENT + 1)
DEL_COLUMN = pg.event.Event(pg.USEREVENT + 2)


class TetrisMap:
    def __init__(self, screen):  
        self.rows = [[] for _ in range(20)]
        self.out_of_bounds = []
        self.screen = screen


    def add(self, tetris_piece):
        for cube in tetris_piece.get_cubes():
            if cube.rect.y < 0:
                self.out_of_bounds.append(cube)
            else:
                row = cube.rect.y // 25
                self.rows[row].append(cube)
        for unsorted_row in self.rows:
            unsorted_row.sort(key=lambda cube: cube.rect.x)
            print([xvalue.rect.x for xvalue in unsorted_row])


    def draw(self):
        spacing = 25
        for _ in range(20):
            if _ == 19:
                pg.draw.rect(self.screen, (0, 0, 0), pg.rect.Rect(225, spacing - 1, 250, 8))
            else:
                pg.draw.rect(self.screen, (0, 0, 0), pg.rect.Rect(225, spacing - 1, 250, 2))
            spacing += 25
        spacing = 25
        for _ in range(11):
            if _ == 0:
                pg.draw.rect(self.screen, (0, 0, 0), pg.rect.Rect(193 + spacing, 0, 8, 507))
            elif _ == 10:
                pg.draw.rect(self.screen, (0, 0, 0), pg.rect.Rect(199 + spacing, 0, 8, 507))
            else:
                pg.draw.rect(self.screen, (0, 0, 0), pg.rect.Rect(199 + spacing, 0, 2, 507))
            spacing += 25
            
        for row in self.rows:
            for cube in row:
                cube.draw(self.screen)

    @property
    def completed_rows(self):
        completed_rows = []
        for row in self.rows:
            if len(row) >= 10:
                completed_rows.append(self.rows.index(row))
        return completed_rows
    

    def delete_completed_rows(self):
        score = 0
        if len(self.completed_rows) == 0:
            return score
        pg.event.post(DEL_COLUMN)
        len_rows = 0
        while len_rows >= 0: 
            break
            for event in pg.event.get():
                if event == DEL_COLUMN:
                    for row in self.completed_rows:
                        del_index = (len(self.rows[row]) // 2) - 1
                        del self.rows[row][del_index]
                        del self.rows[row][del_index]
                        len_rows = len(self.rows[row])
                    pg.time.set_timer(DEL_COLUMN, 300)
            self.screen.fill((70, 70, 70))
            self.draw()
        for row in self.completed_rows:
            del self.rows[row]
            self.rows.insert(0, [])
            score += 2000
        return score
    def __getitem__(self, i):
        return self.rows[i]


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
