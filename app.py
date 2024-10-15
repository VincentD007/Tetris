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
STOP_MOVEMENTDELAY = pg.event.Event(pg.USEREVENT + 4)
STOP_ROTATIONDELAY = pg.event.Event(pg.USEREVENT + 5)


def display_score(screen, score):
    pass


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
                    pg.time.set_timer(DEL_COLUMN, 60, 9)
            self.screen.fill((100, 100, 100))
            self.draw()
            pg.display.update()
        for row in completed_rows:
            del self.rows[row]
            self.rows.insert(0, [])
            score += 2000

        rows_falling = True
        while rows_falling:
            CLOCK.tick(100)
            unsettled_cubes = 0
            for row_index in range(0, 20):
                for cube in self[row_index]:
                    if cube.rect.y // 25 != row_index:
                        cube.rect.y += 1
                        unsettled_cubes += 1
            if unsettled_cubes == 0:
                rows_falling = False
            self.screen.fill((100, 100, 100))
            self.draw()
            pg.display.update()
        return score
    

    def __getitem__(self, i):
        return self.rows[i]



def main():
    tetrismap = TetrisMap(SCREEN)
    player_score = 0
    game_loose = False
    pause_game = False
    addpiece_delayed = True
    movement_delayed = False
    rotate_delayed = False
    addpiece_delay_duration = 800
    movement_delay_duration = 100
    rotate_delay_duration = 120
    first_collision_happened = False
    playgame = True
    fall_delay = 200

    next_piece = random.choice([
        Tpiece("purple", tetrismap), Ipiece("light_blue", tetrismap), 
        Jpiece("blue", tetrismap), Lpiece("orange", tetrismap), 
        Opiece("yellow", tetrismap), Spiece("green", tetrismap), Zpiece("red", tetrismap)
        ])
    piece = random.choice([
        Tpiece("purple", tetrismap), Ipiece("light_blue", tetrismap), 
        Jpiece("blue", tetrismap), Lpiece("orange", tetrismap), 
        Opiece("yellow", tetrismap), Spiece("green", tetrismap), Zpiece("red", tetrismap)
        ])
    
    pg.time.set_timer(PIECE_MOVEDOWN, fall_delay)
    while playgame:
        CLOCK.tick(60)
        events = pg.event.get()

        for event in events:
            if event.type == pg.QUIT:
                playgame = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pause_game = not pause_game

        SCREEN.fill((100, 100, 100))

        if not game_loose and not pause_game:
            if (pg.key.get_pressed()[pg.K_LEFT] or pg.key.get_pressed()[pg.K_RIGHT]) and not movement_delayed:
                if pg.key.get_pressed()[pg.K_LEFT] and not pg.key.get_pressed()[pg.K_RIGHT]:
                    piece.move("left")
                    pg.time.set_timer(STOP_MOVEMENTDELAY, movement_delay_duration, 1)
                    movement_delayed = True
                elif pg.key.get_pressed()[pg.K_RIGHT] and not pg.key.get_pressed()[pg.K_LEFT]:
                    piece.move("right")
                    pg.time.set_timer(STOP_MOVEMENTDELAY, movement_delay_duration, 1)
                    movement_delayed = True

            if pg.key.get_pressed()[pg.K_SPACE] and not rotate_delayed:
                piece.rotate()
                rotate_delayed = True
                pg.time.set_timer(STOP_ROTATIONDELAY, rotate_delay_duration, 1)


            if pg.key.get_pressed()[pg.K_DOWN]:
                pg.event.post(PIECE_MOVEDOWN)

            for event in events:
                if event == STOP_ADDPIECE_DELAY:
                    addpiece_delayed = False

                elif event == STOP_MOVEMENTDELAY:
                    movement_delayed = False

                elif event == STOP_ROTATIONDELAY:
                    rotate_delayed = False

                elif event == PIECE_MOVEDOWN:
                    moved_down = piece.move("down")
                    if moved_down:
                        pg.time.set_timer(STOP_ADDPIECE_DELAY, 0)
                        addpiece_delayed = True
                        first_collision_happened = False
                    elif not addpiece_delayed:
                        pg.time.set_timer(PIECE_MOVEDOWN, 0)
                        tetrismap.add(piece)
                        player_score += tetrismap.delete_completed_rows()
                        if len(tetrismap.out_of_bounds) > 0:
                            game_loose = True
                        else:
                            piece = next_piece
                            next_piece = random.choice([
                            Tpiece("purple", tetrismap), Ipiece("light_blue", tetrismap), 
                            Jpiece("blue", tetrismap), Lpiece("orange", tetrismap), 
                            Opiece("yellow", tetrismap), Spiece("green", tetrismap), Zpiece("red", tetrismap)
                            ])
                            pg.time.set_timer(PIECE_MOVEDOWN, fall_delay)
                    elif not moved_down and not first_collision_happened:
                        pg.time.set_timer(STOP_ADDPIECE_DELAY, addpiece_delay_duration, 1)
                        first_collision_happened = True
        piece.draw(SCREEN)
        tetrismap.draw()
        display_score(SCREEN, player_score)
        pg.display.update()
    pg.quit()

if __name__ == "__main__":
    main() 
