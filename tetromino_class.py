import pygame as pg
import os
pg.init()


purple_block = pg.transform.scale(pg.image.load(os.path.join("assets", "purple_block.png")), (25, 25))
blue_block = pg.transform.scale(pg.image.load(os.path.join("assets", "blue_block.png")), (25, 25))
orange_block = pg.transform.scale(pg.image.load(os.path.join("assets", "orange_block.png")), (25, 25))
green_block = pg.transform.scale(pg.image.load(os.path.join("assets", "green_block.png")), (25, 25))
light_blue_block = pg.transform.scale(pg.image.load(os.path.join("assets", "light_blue_block.png")), (25, 25))
red_block = pg.transform.scale(pg.image.load(os.path.join("assets", "red_block.png")), (25, 25))
yellow_block = pg.transform.scale(pg.image.load(os.path.join("assets", "yellow_block.png")), (25, 25))
black_block = pg.transform.scale(pg.image.load(os.path.join("assets", "black_block.png")), (25, 25))


class Cube:
    def __init__(self, color, x_position, y_position):
        if color == "purple":
            self.image = purple_block
        elif color == "blue":
            self.image = blue_block
        elif color == "orange":
            self.image = orange_block
        elif color == "green":
            self.image = green_block
        elif color == "light_blue":
            self.image = light_blue_block
        elif color == "red":
            self.image = red_block
        elif color == "yellow":
            self.image = yellow_block
        elif color == "black":
            self.image = black_block
        else:
            raise ValueError
            
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


# Base Class for all tetriminoes
class Piece:
    def __init__(self, cube_color, game_map):
        self.position = 1
        self.starting_coords = (350, -25)
        self.color = cube_color.lower()
        self.cubes = []
        self.map = game_map

    def move(self, direction):
        cubes_copy = [Cube(self.color, cpycube.rect.x, cpycube.rect.y) for cpycube in self.cubes]
        if direction == "down":
            for cube in cubes_copy:
                cube.move("down")
            if check_piece_collision(cubes_copy, self.map):
                return False
        elif direction == "left":
            for cube in cubes_copy:
                cube.move("left")
            if check_piece_collision(cubes_copy, self.map):
                return False
        elif direction == "right":
            for cube in cubes_copy:
                cube.move("right")
            if check_piece_collision(cubes_copy, self.map):
                return False
        self.cubes.clear()
        self.cubes.extend(cubes_copy)
        return True
 

    def draw(self, screen):
        shadow_cubes = [Cube("black", cube.rect.x, cube.rect.y) for cube in self.cubes]
        while not check_piece_collision(shadow_cubes, self.map):
            for cube in shadow_cubes:
                cube.move("down")
        for cube in shadow_cubes:
            cube.rect.y -= 25
            cube.draw(screen)
        for cube in self.cubes:
            cube.draw(screen)

    
    def get_cubes(self):
        return [cube for cube in self.cubes]


    
class Tpiece(Piece):
    def __init__(self, color, map):
        super().__init__(color, map)
        self.cubes = [
            Cube(self.color, self.starting_coords[0] - 25 , self.starting_coords[1]),
            Cube(self.color, self.starting_coords[0], self.starting_coords[1] - 25), 
            Cube(self.color, self.starting_coords[0] + 25, self.starting_coords[1]),
            Cube(self.color, self.starting_coords[0], self.starting_coords[1])]


    def rotate(self):
        cubes_copy = [Cube(self.color, cpycube.rect.x, cpycube.rect.y) for cpycube in self.cubes]
        if self.position == 4:
            next_position = 1
        else:
            next_position = self.position + 1
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


        collided = check_piece_collision(cubes_copy, self.map)
        if collided:
            if not bump_piece(cubes_copy, self.map):
                return
            elif collided == "Too far down":
                return
        self.cubes.clear()
        self.cubes.extend(cubes_copy)
        self.position = next_position



class Ipiece(Piece):
    def __init__(self, color, map):
        super().__init__(color, map)
        self.cubes = [
            Cube(self.color, self.starting_coords[0] - 50 , self.starting_coords[1]),
            Cube(self.color, self.starting_coords[0] - 25, self.starting_coords[1]), 
            Cube(self.color, self.starting_coords[0], self.starting_coords[1]),
            Cube(self.color, self.starting_coords[0] + 25, self.starting_coords[1])]


    def rotate(self):
        cubes_copy = [Cube(self.color, cpycube.rect.x, cpycube.rect.y) for cpycube in self.cubes]
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

        collided = check_piece_collision(cubes_copy, self.map)
        if collided:
            if not bump_piece(cubes_copy, self.map):
                return
        elif collided == "Too far down":
            return
        self.cubes.clear()
        self.cubes.extend(cubes_copy)
        self.position = next_position



class Jpiece(Piece):
    def __init__(self, color, map):
        super().__init__(color, map)
        self.cubes = [
            Cube(self.color, self.starting_coords[0] - 25 , self.starting_coords[1] - 25),
            Cube(self.color, self.starting_coords[0] - 25, self.starting_coords[1]), 
            Cube(self.color, self.starting_coords[0], self.starting_coords[1]),
            Cube(self.color, self.starting_coords[0] + 25, self.starting_coords[1])]

  
    def rotate(self):
        cubes_copy = [Cube(self.color, cpycube.rect.x, cpycube.rect.y) for cpycube in self.cubes]
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

        collided = check_piece_collision(cubes_copy, self.map)
        if collided:
            if not bump_piece(cubes_copy, self.map):
                return
        elif collided == "Too far down":
            return
        self.position = next_position
        self.cubes.clear()
        self.cubes.extend(cubes_copy)



class Lpiece(Piece):
    def __init__(self, color, map):
        super().__init__(color, map)
        self.cubes = [
            Cube(self.color, self.starting_coords[0] - 25 , self.starting_coords[1]),
            Cube(self.color, self.starting_coords[0], self.starting_coords[1]), 
            Cube(self.color, self.starting_coords[0] + 25, self.starting_coords[1]),
            Cube(self.color, self.starting_coords[0] + 25, self.starting_coords[1] - 25)]

  
    def rotate(self):
        cubes_copy = [Cube(self.color, cpycube.rect.x, cpycube.rect.y) for cpycube in self.cubes]
        if self.position == 4:
            next_position = 1
        else:
            next_position = self.position + 1
        
        if next_position == 2:
            cubes_copy[0].rect.x += 25
            cubes_copy[0].rect.y -= 25
            cubes_copy[2].rect.x -= 25
            cubes_copy[2].rect.y += 25
            cubes_copy[3].rect.y += 50
        elif next_position == 3:
            cubes_copy[0].rect.x += 25
            cubes_copy[0].rect.y += 25
            cubes_copy[2].rect.x -= 25
            cubes_copy[2].rect.y -= 25
            cubes_copy[3].rect.x -= 50
        elif next_position == 4:
            cubes_copy[0].rect.x -= 25
            cubes_copy[0].rect.y += 25
            cubes_copy[2].rect.x += 25
            cubes_copy[2].rect.y -= 25
            cubes_copy[3].rect.y -= 50
        elif next_position == 1:
            cubes_copy[0].rect.x -= 25
            cubes_copy[0].rect.y -= 25
            cubes_copy[2].rect.x += 25
            cubes_copy[2].rect.y += 25
            cubes_copy[3].rect.x += 50

        collided = check_piece_collision(cubes_copy, self.map)
        if collided:
            if not bump_piece(cubes_copy, self.map):
                return
        elif collided == "Too far down":
            return
        self.position = next_position
        self.cubes.clear()
        self.cubes.extend(cubes_copy)



class Opiece(Piece):
    def __init__(self, color, map):
        super().__init__(color, map)
        self.cubes = [
            Cube(self.color, self.starting_coords[0], self.starting_coords[1]),
            Cube(self.color, self.starting_coords[0] - 25, self.starting_coords[1]), 
            Cube(self.color, self.starting_coords[0] - 25, self.starting_coords[1] - 25),
            Cube(self.color, self.starting_coords[0], self.starting_coords[1] - 25)]

  
    def rotate(self):
        pass



class Spiece(Piece):
    def __init__(self, color, map):
        super().__init__(color, map)
        self.cubes = [
            Cube(self.color, self.starting_coords[0] - 25, self.starting_coords[1]),
            Cube(self.color, self.starting_coords[0], self.starting_coords[1]), 
            Cube(self.color, self.starting_coords[0], self.starting_coords[1] - 25),
            Cube(self.color, self.starting_coords[0] + 25, self.starting_coords[1] - 25)]


    def rotate(self):
        cubes_copy = [Cube(self.color, cpycube.rect.x, cpycube.rect.y) for cpycube in self.cubes]
        if self.position == 4:
            next_position = 1
        else:
            next_position = self.position + 1
        
        if next_position == 2:
            cubes_copy[0].rect.x += 25
            cubes_copy[0].rect.y -= 50
            cubes_copy[1].rect.y -= 25
            cubes_copy[2].rect.x += 25
            cubes_copy[3].rect.y += 25
        elif next_position == 3:
            cubes_copy[0].rect.x += 50
            cubes_copy[0].rect.y += 25
            cubes_copy[1].rect.x += 25
            cubes_copy[2].rect.y += 25
            cubes_copy[3].rect.x -= 25
        elif next_position == 4:
            cubes_copy[0].rect.x -= 25
            cubes_copy[0].rect.y += 50
            cubes_copy[1].rect.y += 25
            cubes_copy[2].rect.x -= 25
            cubes_copy[3].rect.y -= 25
        elif next_position == 1:
            cubes_copy[0].rect.x -= 50
            cubes_copy[0].rect.y -= 25
            cubes_copy[1].rect.x -= 25
            cubes_copy[2].rect.y -= 25
            cubes_copy[3].rect.x += 25

        collided = check_piece_collision(cubes_copy, self.map)
        if collided:
            if not bump_piece(cubes_copy, self.map):
                return
        elif collided == "Too far down":
            return
        self.position = next_position
        self.cubes.clear()
        self.cubes.extend(cubes_copy)



class Zpiece(Piece):
    def __init__(self, color, map):
        super().__init__(color, map)
        self.cubes = [
            Cube(self.color, self.starting_coords[0] - 25, self.starting_coords[1] - 25),
            Cube(self.color, self.starting_coords[0], self.starting_coords[1] - 25), 
            Cube(self.color, self.starting_coords[0], self.starting_coords[1]),
            Cube(self.color, self.starting_coords[0] + 25, self.starting_coords[1])]


    def rotate(self):
        cubes_copy = [Cube(self.color, cpycube.rect.x, cpycube.rect.y) for cpycube in self.cubes]
        if self.position == 4:
            next_position = 1
        else:
            next_position = self.position + 1
        
        if next_position == 2:
            cubes_copy[0].rect.x += 50
            cubes_copy[0].rect.y -= 25
            cubes_copy[1].rect.x += 25
            cubes_copy[2].rect.y -= 25
            cubes_copy[3].rect.x -= 25
        elif next_position == 3:
            cubes_copy[0].rect.x += 25
            cubes_copy[0].rect.y += 50
            cubes_copy[1].rect.y += 25
            cubes_copy[2].rect.x += 25
            cubes_copy[3].rect.y -= 25
        elif next_position == 4:
            cubes_copy[0].rect.x -= 50
            cubes_copy[0].rect.y += 25
            cubes_copy[1].rect.x -= 25
            cubes_copy[2].rect.y += 25
            cubes_copy[3].rect.x += 25
        elif next_position == 1:
            cubes_copy[0].rect.x -= 25
            cubes_copy[0].rect.y -= 50
            cubes_copy[1].rect.y -= 25
            cubes_copy[2].rect.x -= 25
            cubes_copy[3].rect.y += 25

        collided = check_piece_collision(cubes_copy, self.map)
        if collided:
            if not bump_piece(cubes_copy, self.map):
                return
        elif collided == "Too far down":
            return
        self.position = next_position
        self.cubes.clear()
        self.cubes.extend(cubes_copy)
 