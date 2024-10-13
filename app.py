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
STOP_ADDPIECE_DELAY = pg.event.Event(pg.USEREVENT + 3)

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
        completed_rows = self.completed_rows
        if len(completed_rows) == 0:
            return score
        pg.event.post(DEL_COLUMN)
        len_rows = 10
        while len_rows > 0: 
            for event in pg.event.get():
                if event == DEL_COLUMN:
                    for row in completed_rows:
                        del_index = len_rows // 2 - 1
                        del self.rows[row][del_index]
                        del self.rows[row][del_index]
                    len_rows -= 2
                    pg.time.set_timer(DEL_COLUMN, 30)
            self.screen.fill((100, 100, 100))
            self.draw()
            pg.display.update()
        for row in completed_rows:
            del self.rows[row]
            self.rows.insert(0, [])
            score += 2000
        return score
    

    def __getitem__(self, i):
        return self.rows[i]


def main():
    player_score = 0
    game_loose = False
    pause_game = False
    addpiece_delay = True
    first_collision_happened = False
    fall_speed = 350
    playgame = True
    tetrismap = TetrisMap(SCREEN)

    piece = random.choice([Tpiece("purple", tetrismap), Ipiece("light_blue", tetrismap), Jpiece("blue", tetrismap), 
                           Lpiece("orange", tetrismap), Opiece("yellow", tetrismap), Spiece("green", tetrismap), Zpiece("red", tetrismap)
                           ])
    pg.time.set_timer(PIECE_MOVEDOWN, fall_speed)
    while playgame:
        CLOCK.tick(60)
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                playgame = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pause_game = not pause_game

        SCREEN.fill((100, 100, 100))

        if not game_loose and not pause_game:
            for event in events:
                pressed_keys = pg.key.get_pressed()
                if pressed_keys[pg.K_DOWN]:
                    pg.event.post(PIECE_MOVEDOWN)

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE: 
                        piece.rotate()
                    elif event.key == pg.K_LEFT:
                        piece.move(tetrismap, "left")
                    elif event.key == pg.K_RIGHT:
                        piece.move(tetrismap, "right")

                elif event == STOP_ADDPIECE_DELAY:
                    addpiece_delay = False

                elif event == PIECE_MOVEDOWN:
                    moved_down = piece.move(tetrismap, "down")
                    if not moved_down:
                        if not first_collision_happened:
                            first_collision_happened = True
                            pg.time.set_timer(STOP_ADDPIECE_DELAY, 500, 1)
                        if not addpiece_delay:
                            tetrismap.add(piece)
                            player_score += tetrismap.delete_completed_rows()
                            if len(tetrismap.out_of_bounds) > 0:
                                game_loose = True
                            else:
                                addpiece_delay = True
                                first_collision_happened = False
                                piece = random.choice([Tpiece("purple", tetrismap), Ipiece("light_blue", tetrismap), Jpiece("blue", tetrismap), 
                                                    Lpiece("orange", tetrismap), Opiece("yellow", tetrismap), Spiece("green", tetrismap), Zpiece("red", tetrismap)
                                                    ])
                                pg.time.set_timer(PIECE_MOVEDOWN, fall_speed)



        for row_index in range(0, 20):
            for cube in tetrismap[row_index]:
                if cube.rect.y // 25 != row_index:
                    cube.rect.y += 5

        piece.draw(SCREEN)
        tetrismap.draw()
        pg.display.update()
    pg.quit()

if __name__ == "__main__":
    main() 
