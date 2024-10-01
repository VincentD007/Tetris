import pygame as pg
pg.init()

purple_block = pg.transform.scale(pg.image.load("purple_block.png"), (25, 25))
blue_block = pg.transform.scale(pg.image.load("blue_block.png"), (25, 25))
gold_block = pg.transform.scale(pg.image.load("gold_block.png"), (25, 25))
green_block = pg.transform.scale(pg.image.load("green_block.png"), (25, 25))
light_blue_block = pg.transform.scale(pg.image.load("light_blue_block.png"), (25, 25))
red_block = pg.transform.scale(pg.image.load("red_block.png"), (25, 25))
yellow_block = pg.transform.scale(pg.image.load("yellow_block.png"), (25, 25))


class TetrisMap:
    def __init__(self):  
        self.rows = [[] for _ in range(20)]

    def add(self, tetris_piece):
        for cube in tetris_piece.get_cubes():
            location = cube.rect.y // 25
            self.rows[location].append(cube)

    def drawcubes(self, screen):
        for row in self.rows:
            for cube in row:
                cube.draw(screen)

    def __getitem__(self, i):
        return self.rows[i]
    

class Cube:
    def __init__(self, color, x_position, y_position):
        if color == "purple":
            self.image = purple_block
        elif color == "blue":
            self.image = blue_block
        elif color == "gold":
            self.image = gold_block
        elif color == "green":
            self.image = green_block
        elif color == "light_blue":
            self.image = light_blue_block
        elif color == "red":
            self.image = red_block
        elif color == "yellow":
            self.image = yellow_block
        self.rect = self.image.get_rect(topleft = (x_position, y_position))

 
    def move(self, direction):
        if direction == "down":
            self.rect.y += 25
        elif direction == "left":
            self.rect.x -= 25
        elif direction == "right":
            self.rect.x += 25
    

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


def check_piece_collision(cubes, active_map):
    for cube in cubes:
        if cube.rect.y > 475:
            return "Too far down"
        if pg.Rect.collidelist(cube.rect, [mapcube.rect for mapcube in active_map[cube.rect.y // 25]]) != -1:
            return True
        elif cube.rect.x < 225 or cube.rect.x > 450:
            return True
    return False


def bump_piece(piece_cubes, game_map):
    bump_offset = 25
    while True:
        for cube in piece_cubes:
            cube.rect.x += bump_offset
        if not check_piece_collision(piece_cubes, game_map):
            return True
        else:
            if bump_offset == 25:
                bump_offset -= 75
            elif bump_offset == -50:
                bump_offset += 125
            elif bump_offset == 75:
                bump_offset -= 175
            else:
                break
    return False
                

class Tpiece:
    def __init__(self):
        self.reference_cube = pg.rect.Rect(350, 0, 25, 25)
        starting_x, starting_y = 350, 0
        self.position = 1
        self.cubes = [
            Cube("purple", starting_x - 25 , starting_y),
            Cube("purple", starting_x, starting_y - 25), 
            Cube("purple", starting_x + 25, starting_y),
            Cube("purple", starting_x, starting_y)]


    def move(self, game_map, direction):
        cubes_copy = [Cube("purple", cpycube.rect.x, cpycube.rect.y) for cpycube in self.cubes]
        if direction == "down":
            for cube in cubes_copy:
                cube.move("down")
        elif direction == "left":
            for cube in cubes_copy:
                cube.move("left")
            if check_piece_collision(cubes_copy, game_map):
                return
        elif direction == "right":
            for cube in cubes_copy:
                cube.move("right")
            if check_piece_collision(cubes_copy, game_map):
                return
        self.cubes.clear()
        self.cubes.extend(cubes_copy)
 

    def draw(self, screen):
        for cube in self.cubes:
            cube.draw(screen)


    def rotate(self, game_map):
        cubes_copy = [Cube("purple", cpycube.rect.x, cpycube.rect.y) for cpycube in self.cubes]
        if self.position == 4:
            next_position = 1
        else:
            next_position = self.position + 1
        # Adjust rotations to Tpiece
        if next_position == 2:
            cubes_copy[0].rect.x += 25
            cubes_copy[0].rect.y -= 25
            cubes_copy[1].rect.x += 25
            cubes_copy[1].rect.y += 25
            cubes_copy[2].rect.x -= 25
            cubes_copy[2].rect.y += 25
        elif next_position == 3:
            cubes_copy[0].rect.x += 25
            cubes_copy[0].rect.y += 25
            cubes_copy[1].rect.x -= 25
            cubes_copy[1].rect.y += 25
            cubes_copy[2].rect.x -= 25
            cubes_copy[2].rect.y -= 25

        elif next_position == 4:
            cubes_copy[0].rect.x -= 25
            cubes_copy[0].rect.y += 25
            cubes_copy[1].rect.x -= 25
            cubes_copy[1].rect.y -= 25
            cubes_copy[2].rect.x += 25
            cubes_copy[2].rect.y -= 25

        elif next_position == 1:
            cubes_copy[0].rect.x -= 25
            cubes_copy[0].rect.y -= 25
            cubes_copy[1].rect.x += 25
            cubes_copy[1].rect.y -= 25
            cubes_copy[2].rect.x += 25
            cubes_copy[2].rect.y += 25


        collided = check_piece_collision(cubes_copy, game_map)
        if collided:
            if not bump_piece(cubes_copy, game_map):
                return
            elif collided == "Too far down":
                return
        self.cubes.clear()
        self.cubes.extend(cubes_copy)
        self.position = next_position
    
    def get_cubes(self):
        aggregated_cubes = [cube for cube in self.cubes]
        return aggregated_cubes


class Ipiece:
    def __init__(self):
        self.reference_cube = pg.rect.Rect(350, 0, 25, 25)
        starting_x, starting_y = 350, 0
        self.position = 1
        self.cubes = [
            Cube("light_blue", starting_x - 25 , starting_y),
            Cube("light_blue", starting_x, starting_y), 
            Cube("light_blue", starting_x + 25, starting_y),
            Cube("light_blue", starting_x + 50, starting_y)]


    def move(self, game_map, direction):
        cubes_copy = [Cube("light_blue", cpycube.rect.x, cpycube.rect.y) for cpycube in self.cubes]
        if direction == "down":
            for cube in cubes_copy:
                cube.move("down")
        elif direction == "left":
            for cube in cubes_copy:
                cube.move("left")
            if check_piece_collision(cubes_copy, game_map):
                return
        elif direction == "right":
            for cube in cubes_copy:
                cube.move("right")
            if check_piece_collision(cubes_copy, game_map):
                return
        self.cubes.clear()
        self.cubes.extend(cubes_copy)


    def draw(self, screen):
        for cube in self.cubes:
            cube.draw(screen)


    def get_cubes(self):
        return [cube for cube in self.cubes]
    

    def rotate(self, game_map):
        cubes_copy = [Cube("light_blue", cpycube.rect.x, cpycube.rect.y) for cpycube in self.cubes]
        if self.position == 4:
            next_position = 1
        else:
            next_position = self.position + 1
        
        if next_position == 2:
            cubes_copy[0].rect.x += 50
            cubes_copy[0].rect.y -= 25
            cubes_copy[1].rect.x += 25
            cubes_copy[2].rect.y += 25
            cubes_copy[3].rect.x -= 25
            cubes_copy[3].rect.y += 50
        elif next_position == 3:
            cubes_copy[0].rect.y += 50
            cubes_copy[0].rect.x += 25
            cubes_copy[1].rect.y += 25
            cubes_copy[2].rect.x -= 25
            cubes_copy[3].rect.y -= 25
            cubes_copy[3].rect.x -= 50
        elif next_position == 4:
            cubes_copy[0].rect.x -= 50
            cubes_copy[0].rect.y += 25
            cubes_copy[1].rect.x -= 25
            cubes_copy[2].rect.y -= 25
            cubes_copy[3].rect.x += 25
            cubes_copy[3].rect.y -= 50
        elif next_position == 1:
            cubes_copy[0].rect.y -= 50
            cubes_copy[0].rect.x -= 25
            cubes_copy[1].rect.y -= 25
            cubes_copy[2].rect.x += 25
            cubes_copy[3].rect.y += 25
            cubes_copy[3].rect.x += 50

        collided = check_piece_collision(cubes_copy, game_map)
        if collided:
            if not bump_piece(cubes_copy, game_map):
                return
        elif collided == "Too far down":
            return
        self.cubes.clear()
        self.cubes.extend(cubes_copy)
        self.position = next_position


class Jpiece:
    def __init__(self):
        self.reference_cube = pg.rect.Rect(350, 0, 25, 25)
        starting_x, starting_y = 350, 0
        self.position = 1
        self.cubes = [
            Cube("blue", starting_x - 25 , starting_y - 25),
            Cube("blue", starting_x - 25, starting_y), 
            Cube("blue", starting_x, starting_y),
            Cube("blue", starting_x + 25, starting_y)]


    def move(self, game_map, direction):
        cubes_copy = [Cube("blue", cpycube.rect.x, cpycube.rect.y) for cpycube in self.cubes]
        if direction == "down":
            for cube in cubes_copy:
                cube.move("down")
        elif direction == "left":
            for cube in cubes_copy:
                cube.move("left")
            if check_piece_collision(cubes_copy, game_map):
                return
        elif direction == "right":
            for cube in cubes_copy:
                cube.move("right")
            if check_piece_collision(cubes_copy, game_map):
                return
        self.cubes.clear()
        self.cubes.extend(cubes_copy)


    def draw(self, screen):
        for cube in self.cubes:
            cube.draw(screen)


    def get_cubes(self):
        return self.cubes

    
    def rotate(self, game_map):
        cubes_copy = [Cube("blue", cpycube.rect.x, cpycube.rect.y) for cpycube in self.cubes]
        if self.position == 4:
            next_position = 1
        else:
            next_position = self.position + 1
        
        if next_position == 2:
            cubes_copy[0].rect.x += 50
            cubes_copy[1].rect.y -= 25
            cubes_copy[1].rect.x += 25
            cubes_copy[3].rect.y += 25
            cubes_copy[3].rect.x -= 25
        elif next_position == 3:
            cubes_copy[0].rect.y += 50
            cubes_copy[1].rect.x += 25
            cubes_copy[1].rect.y += 25
            cubes_copy[3].rect.x -= 25
            cubes_copy[3].rect.y -= 25
        elif next_position == 4:
            cubes_copy[0].rect.x -= 50 
            cubes_copy[1].rect.x -= 25
            cubes_copy[1].rect.y += 25
            cubes_copy[3].rect.x += 25
            cubes_copy[3].rect.y -= 25
        elif next_position == 1:
            cubes_copy[0].rect.y -= 50
            cubes_copy[1].rect.x -= 25
            cubes_copy[1].rect.y -= 25
            cubes_copy[3].rect.x += 25
            cubes_copy[3].rect.y += 25

        collided = check_piece_collision(cubes_copy, game_map)
        if collided:
            if not bump_piece(cubes_copy, game_map):
                return
        elif collided == "Too far down":
            return
        self.position = next_position
        self.cubes.clear()
        self.cubes.extend(cubes_copy)
