import pygame as pg
from tetromino_class import *
import random

pg.init()
WIDTH = 700
HEIGHT = 700
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("TETRIS")
CLOCK = pg.time.Clock()
PIECE_MOVEDOWN = pg.event.Event(pg.USEREVENT + 1)
DEL_COLUMN = pg.event.Event(pg.USEREVENT + 2)
STOP_ADDPIECE_DELAY = pg.event.Event(pg.USEREVENT + 3)
STOP_MOVEMENTDELAY = pg.event.Event(pg.USEREVENT + 4)
STOP_ROTATIONDELAY = pg.event.Event(pg.USEREVENT + 5)
scoretext_font = pg.font.Font("assets\gomarice_no_continue.ttf", 50)
score_font = pg.font.Font("assets\gomarice_no_continue.ttf", 30)

def display_score(screen, current_score):
    text = scoretext_font.render("Score", 1, (0, 255, 220))
    score = score_font.render(str(current_score), 1, (255, 255, 255))
    screen.blit(text, (25, 25))
    screen.blit(score, (88 - (score.get_width()/2), 85))


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
    

    def delete_completed_rows(self, score):
        current_score = score
        points_earned = 0
        completed_rows = self.completed_rows
        if len(completed_rows) == 0:
            return points_earned
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
            display_score(self.screen, current_score + points_earned)
            pg.display.update()
        for row in completed_rows:
            del self.rows[row]
            self.rows.insert(0, [])
            points_earned += 100

        rows_falling = True
        while rows_falling:
            CLOCK.tick(120)
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
            display_score(self.screen, current_score + points_earned)
            pg.display.update()

        return points_earned
    

    def __getitem__(self, i):
        return self.rows[i]


    def new_piece(self, lvl):
        if lvl == 1:
            return random.choice([
            Tpiece("purple", self), Ipiece("light_blue", self), 
            Jpiece("blue", self), Lpiece("orange", self), 
            Opiece("yellow", self), Spiece("green", self), Zpiece("red", self)
            ])



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
    level = 1

    next_piece2 = tetrismap.new_piece(level)
    next_piece = tetrismap.new_piece(level)
    piece = tetrismap.new_piece(level)
    while type(piece) == (type(next_piece) and type(next_piece2)):
        next_piece2 = tetrismap.new_piece(level)

    pg.time.set_timer(PIECE_MOVEDOWN, fall_delay)
    while playgame:
        CLOCK.tick(60)
        events = pg.event.get()

        for event in events:
            if event.type == pg.QUIT:
                playgame = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pause_game = not pause_game
        if not pause_game:
            SCREEN.fill((100, 100, 100))
        else:
            SCREEN.fill((50, 50, 50))
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
                        movement_delayed = False
                        rotate_delayed = False
                        if len(tetrismap.out_of_bounds) > 0:
                            game_loose = True
                        else:
                            piece = next_piece
                            next_piece = next_piece2
                            next_piece2 = tetrismap.new_piece(level)
                            while type(piece) == (type(next_piece) and type(next_piece2)):
                                next_piece2 = tetrismap.new_piece(level)

                            pg.time.set_timer(PIECE_MOVEDOWN, fall_delay)
                            
                    elif not first_collision_happened:
                        for row in tetrismap.rows:
                            if len(row) < 6:
                                continue
                            else:
                                piececubes_in_row = 0
                                for cube in piece.get_cubes():
                                    if cube.rect.y // 25 == tetrismap.rows.index(row):
                                        piececubes_in_row += 1
                                    else:
                                        continue
                                if len(row) + piececubes_in_row == 10:
                                    pg.time.set_timer(PIECE_MOVEDOWN, 0)
                                    tetrismap.add(piece)
                                    movement_delayed = False
                                    rotate_delayed = False
                                    player_score += tetrismap.delete_completed_rows(player_score)
                                    if len(tetrismap.out_of_bounds) > 0:
                                        game_loose = True
                                    else:
                                        piece = next_piece
                                        next_piece = next_piece2
                                        next_piece2 = tetrismap.new_piece(level)
                                        while type(piece) == (type(next_piece) and type(next_piece2)):
                                            next_piece2 = tetrismap.new_piece(level)

                                        pg.time.set_timer(PIECE_MOVEDOWN, fall_delay)
                                    break
                        if addpiece_delayed:
                            pg.time.set_timer(STOP_ADDPIECE_DELAY, addpiece_delay_duration, 1)
                            first_collision_happened = True
        tetrismap.draw()
        piece.draw(SCREEN)
        display_score(SCREEN, player_score)
        pg.display.update()
    pg.quit()

if __name__ == "__main__":
    main() 
