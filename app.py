import pygame as pg
from tetromino_class import *
import random, os

pg.init()
game_state = 0 # 0 = main_menu; 1 = game_running; 2 = QUIT
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

TEXT_FONT = pg.font.Font(os.path.join("assets", "gomarice_no_continue.ttf"), 50)
SCORE_FONT = pg.font.Font(os.path.join("assets", "gomarice_no_continue.ttf"), 30)
PAUSE_TEXT = TEXT_FONT.render("PAUSED", 1, (255, 255, 255))


tetrominos = {
    Tpiece : pg.image.load(os.path.join("assets", "Tpiece.png")),
    Ipiece : pg.image.load(os.path.join("assets", "Ipiece.png")),
    Jpiece : pg.image.load(os.path.join("assets", "Jpiece.png")),
    Lpiece : pg.image.load(os.path.join("assets", "Lpiece.png")),
    Opiece : pg.image.load(os.path.join("assets", "Opiece.png")),
    Spiece : pg.image.load(os.path.join("assets", "Spiece.png")),
    Zpiece : pg.image.load(os.path.join("assets", "Zpiece.png")),
}


def display_score(screen, current_score):
    text = TEXT_FONT.render("Score", 1, (0, 255, 220))
    score = SCORE_FONT.render(str(current_score), 1, (255, 255, 255))
    screen.blit(text, ((225 - text.get_width())/2, 25))
    screen.blit(score, ((225 - score.get_width())/2, 85))


def display_next_pieces(screen, pieces: list) -> None:
    text = TEXT_FONT.render("Up Next", 1, (255, 255, 255))
    screen.blit(text, (475 + ((WIDTH-475) - (text.get_width()))/2, 25))
    y_cord = 25 + text.get_height() + 40
    for piece in pieces:
        screen.blit(tetrominos[type(piece)], (475 + ((WIDTH-475) - (tetrominos[type(piece)].get_width()))/2, y_cord))
        y_cord += 80


def random_piece(lvl: int, map) -> Piece: 
    if lvl == 1:
        return random.choice([
        Tpiece("purple", map), Ipiece("light_blue", map), 
        Jpiece("blue", map), Lpiece("orange", map), 
        Opiece("yellow", map), Spiece("green", map), Zpiece("red", map)
        ])
    

class TetrisMap:
    def __init__(self):  
        self.rows = [[] for _ in range(20)]
        self.out_of_bounds = []
        self.level = 1
        self.next_pieces = [random_piece(self.level, self), random_piece(self.level, self), random_piece(self.level, self)]



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
                pg.draw.rect(SCREEN, (0, 0, 0), pg.rect.Rect(225, spacing - 1, 250, 8))
            else:
                pg.draw.rect(SCREEN, (0, 0, 0), pg.rect.Rect(225, spacing - 1, 250, 2))
            spacing += 25
        spacing = 25
        for _ in range(11):
            if _ == 0:
                pg.draw.rect(SCREEN, (0, 0, 0), pg.rect.Rect(193 + spacing, 0, 8, 507))
            elif _ == 10:
                pg.draw.rect(SCREEN, (0, 0, 0), pg.rect.Rect(199 + spacing, 0, 8, 507))
            else:
                pg.draw.rect(SCREEN, (0, 0, 0), pg.rect.Rect(199 + spacing, 0, 2, 507))
            spacing += 25
            
        for row in self.rows:
            for cube in row:
                cube.draw(SCREEN)

    @property
    def completed_rows(self):
        completed_rows = []
        for row in self.rows:
            if len(row) >= 10:
                completed_rows.append(self.rows.index(row))
        return completed_rows
    

    def delete_completed_rows(self, score):
        global game_state # 0 = main_menu; 1 = game_running; 2 = QUIT
        current_score = score
        points_earned = 0
        completed_rows = self.completed_rows
        if len(completed_rows) == 0:
            return points_earned
        pg.event.post(DEL_COLUMN)
        len_rows = 10
        while len_rows > 0:
            if game_state == 2:
                return
            for event in pg.event.get():
                if event == DEL_COLUMN:
                    for row in completed_rows:
                        del_index = len_rows // 2 - 1
                        del self.rows[row][del_index]
                        del self.rows[row][del_index]
                    len_rows -= 2
                    pg.time.set_timer(DEL_COLUMN, 60, 1)
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    pause_game(self, current_score)
                    pg.event.post(DEL_COLUMN)
                elif event.type == pg.QUIT:
                    game_state = 2
            SCREEN.fill((100, 100, 100))
            self.draw()
            display_score(SCREEN, current_score + points_earned)
            display_next_pieces(SCREEN, self.next_pieces)
            pg.display.update()
        for row in completed_rows:
            del self.rows[row]
            self.rows.insert(0, [])
            points_earned += 100

        rows_falling = True
        while rows_falling:
            if game_state == 2:
                return
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    game_state = 2
            CLOCK.tick(120)
            unsettled_cubes = 0
            for row_index in range(0, 20):
                for cube in self[row_index]:
                    if cube.rect.y // 25 != row_index:
                        cube.rect.y += 1
                        unsettled_cubes += 1
            if unsettled_cubes == 0:
                rows_falling = False
            SCREEN.fill((100, 100, 100))
            self.draw()
            display_score(SCREEN, current_score + points_earned)
            display_next_pieces(SCREEN, self.next_pieces)
            pg.display.update()

        return points_earned
    

    def __getitem__(self, i):
        return self.rows[i]


    def new_piece(self, lvl: int) -> Piece:
        new_piece = None
        if lvl == self.level:
            new_piece = self.next_pieces[0]
            del self.next_pieces[0]
            self.next_pieces.append(random_piece(lvl, self))
        else:
            self.level = lvl
            self.next_pieces.clear()
            self.next_pieces.extend([random_piece(lvl, self), random_piece(lvl, self), random_piece(lvl, self)])
            new_piece = self.next_pieces[0]
            del self.next_pieces[0]
            self.next_pieces.append(random_piece(lvl, self))
        return new_piece
    

    def reset(self):
        self.rows = [[] for _ in range(20)]
        self.out_of_bounds = []
        self.level = 1
        self.next_pieces = [random_piece(self.level, self), random_piece(self.level, self), random_piece(self.level, self)]


def new_game():
    global game_state # 0 = main_menu; 1 = game_running; 2 = QUIT
    tetrismap = TetrisMap()
    player_score = 0
    game_loose = False
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

    piece = tetrismap.new_piece(level)
    pg.time.set_timer(PIECE_MOVEDOWN, fall_delay)
    while game_state == 1:
        CLOCK.tick(60)
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                game_state = 2
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pause_game(tetrismap, player_score, piece)
                if first_collision_happened:
                    addpiece_delayed = False
        
        SCREEN.fill((100, 100, 100))
        if not game_loose:
            if (pg.key.get_pressed()[pg.K_LEFT] or pg.key.get_pressed()[pg.K_RIGHT]) and not movement_delayed:
                if pg.key.get_pressed()[pg.K_LEFT] and not pg.key.get_pressed()[pg.K_RIGHT]:
                    piece.move("left")
                    pg.time.set_timer(STOP_MOVEMENTDELAY, movement_delay_duration, 1)
                    movement_delayed = True
                elif pg.key.get_pressed()[pg.K_RIGHT] and not pg.key.get_pressed()[pg.K_LEFT]:
                    piece.move("right")
                    pg.time.set_timer(STOP_MOVEMENTDELAY, movement_delay_duration, 1)
                    movement_delayed = True

            if pg.key.get_pressed()[pg.K_DOWN] and not rotate_delayed:
                piece.rotate()
                rotate_delayed = True
                pg.time.set_timer(STOP_ROTATIONDELAY, rotate_delay_duration, 1)


            if pg.key.get_pressed()[pg.K_SPACE]:
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
                        if len(tetrismap.out_of_bounds) > 0: #Ends the game if the Pieces go past the ceiling
                            game_loose = True
                        else: #Renders a new piece if the player has not lost the game
                            piece = tetrismap.new_piece(level)
                            pg.time.set_timer(PIECE_MOVEDOWN, fall_delay)
                            
                    elif not first_collision_happened:
                        row_number = 0
                        for row in tetrismap.rows:
                            piececubes_in_row = 0
                            for cube in piece.get_cubes():
                                if cube.rect.y // 25 == row_number:
                                    piececubes_in_row += 1
                            #Stops PIECE_MOVEDOWN timer and adds tetromino to the map and then deletes the completed rows
                            if len(row) + piececubes_in_row == 10:
                                pg.time.set_timer(PIECE_MOVEDOWN, 0)
                                tetrismap.add(piece)
                                movement_delayed = False
                                rotate_delayed = False

                                try:
                                    player_score += tetrismap.delete_completed_rows(player_score)
                                except TypeError:
                                    return

                                if len(tetrismap.out_of_bounds) > 0:
                                    game_loose = True
                                else:
                                    piece = tetrismap.new_piece(level)
                                    pg.time.set_timer(PIECE_MOVEDOWN, fall_delay)
                                break
                            elif row_number == 19:
                                pg.time.set_timer(STOP_ADDPIECE_DELAY, addpiece_delay_duration, 1)
                                first_collision_happened = True
                            row_number += 1
        tetrismap.draw()
        piece.draw(SCREEN)
        display_score(SCREEN, player_score)
        display_next_pieces(SCREEN, tetrismap.next_pieces)
        pg.display.update()


def pause_game(active_map:TetrisMap, current_score:int, piece:Piece=None):
    global game_state # 0 = main_menu; 1 = game_running; 2 = QUIT
    paused = True
    while paused:
        events = pg.event.get()
        for event in events:
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                paused = False
            elif event.type == pg.QUIT:
                game_state = 2
                paused = False
        SCREEN.fill((50, 50, 50))
        active_map.draw()
        if piece is not None:
            piece.draw(SCREEN)
        display_score(SCREEN, current_score)
        display_next_pieces(SCREEN, active_map.next_pieces)
        SCREEN.blit(PAUSE_TEXT, (WIDTH/2 - (PAUSE_TEXT.get_width()/2), HEIGHT - (HEIGHT/4)))
        display_next_pieces(SCREEN, active_map.next_pieces)
        pg.display.update()


def main_menu():
    global game_state # 0 = main_menu; 1 = game_running; 2 = QUIT
    menu_font = pg.font.Font(os.path.join("assets", "gomarice_no_continue.ttf"), 100)
    title = menu_font.render("TETRIS", True, (255, 255, 255))
    while game_state != 2:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_state = 2
            elif event.type == pg.KEYDOWN and event.key == pg.K_p:
                game_state = 1
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(title, ((SCREEN.get_width()/2)-(title.get_width()/2), SCREEN.get_height()/6))
        pg.display.update()
        if game_state == 1:
            new_game()


if __name__ == "__main__":
    main_menu()
 