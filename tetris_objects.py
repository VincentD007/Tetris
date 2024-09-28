import pygame as pg
pg.init()

purple_block = pg.transform.scale(pg.image.load("purple_block.png"), (25, 25))
blue_block = pg.transform.scale(pg.image.load("blue_block.png"), (25, 25))
gold_block = pg.transform.scale(pg.image.load("gold_block.png"), (25, 25))
green_block = pg.transform.scale(pg.image.load("green_block.png"), (25, 25))
light_blue_block = pg.transform.scale(pg.image.load("light_blue_block.png"), (25, 25))
red_block = pg.transform.scale(pg.image.load("red_block.png"), (25, 25))
yellow_block = pg.transform.scale(pg.image.load("yellow_block.png"), (25, 25))


class Map:
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


class Tpiece:
    def __init__(self):
        self.reference_cube = pg.rect.Rect(350, 0, 25, 25)
        self.position = 1
        self.cubes = [
            Cube("purple", self.reference_cube.x, self.reference_cube.y),
            Cube("purple", self.reference_cube.x, self.reference_cube.y - 25), 
            Cube("purple", self.reference_cube.x + 25, self.reference_cube.y),
            Cube("purple", self.reference_cube.x - 25, self.reference_cube.y)]


    def move(self, map, direction):
        if direction == "down":
            self.reference_cube.y += 25
            for cube in self.cubes:
                cube.move("down")

        elif direction == "left":
            for cube in self.cubes:
                if cube.rect.x - 25 < 225:
                    return
                else:
                    for mapped_cube in map[cube.rect.y // 25]:
                        if mapped_cube.rect.x == cube.rect.x - 25:
                            return
            self.reference_cube.x -= 25
            for cube in self.cubes:
                cube.move("left")

        elif direction == "right":
            for cube in self.cubes:
                if cube.rect.x + 25 > 450:
                    return
                else:
                    for mapped_cube in map[cube.rect.y // 25]:
                        if mapped_cube.rect.x == cube.rect.x + 25:
                            return
            self.reference_cube.x += 25
            for cube in self.cubes:
                cube.move("right")
 

    def draw(self, screen):
        for cube in self.cubes:
            cube.draw(screen)


    def rotate(self, map):
        if self.position == 4:
            next_position = 1
        else:
            next_position = self.position + 1
        positions = {
        1: [Cube("purple", self.reference_cube.x, self.reference_cube.y),
            Cube("purple", self.reference_cube.x, self.reference_cube.y - 25), 
            Cube("purple", self.reference_cube.x + 25, self.reference_cube.y),
            Cube("purple", self.reference_cube.x - 25, self.reference_cube.y)],

        2: [Cube("purple", self.reference_cube.x, self.reference_cube.y),
            Cube("purple", self.reference_cube.x, self.reference_cube.y - 25), 
            Cube("purple", self.reference_cube.x, self.reference_cube.y + 25), 
            Cube("purple", self.reference_cube.x + 25, self.reference_cube.y)],

        3: [Cube("purple", self.reference_cube.x, self.reference_cube.y),
            Cube("purple", self.reference_cube.x, self.reference_cube.y + 25), 
            Cube("purple", self.reference_cube.x + 25, self.reference_cube.y), 
            Cube("purple", self.reference_cube.x - 25, self.reference_cube.y)],

        4: [Cube("purple", self.reference_cube.x, self.reference_cube.y),
            Cube("purple", self.reference_cube.x, self.reference_cube.y - 25), 
            Cube("purple", self.reference_cube.x, self.reference_cube.y + 25), 
            Cube("purple", self.reference_cube.x - 25, self.reference_cube.y)]
        }


        collision = False
        collided_x = 0
        for cube in positions[next_position]:
            if cube.rect.y > 475:
                return
            if pg.Rect.collidelist(cube.rect, [cube.rect for cube in map[cube.rect.y // 25]]) != -1:
                collision = True
                collided_x = cube.rect.x
                break
            elif cube.rect.x < 225:
                collided_x = 200
                collision = True
                break
            elif cube.rect.x > 450:
                collided_x = 475
                collision = True
                break
      
        if collision:
            offset = 0
            cubestoleft = []
            cubestoright = []
            for cube in positions[next_position]:
                if cube.rect.x > collided_x:
                    cubestoright.append(cube)
                elif cube.rect.x < collided_x:
                    cubestoleft.append(cube)
                    
            l = len(cubestoleft)
            r = len(cubestoright)
            if l > r:
                offset = -25
                for cube in positions[next_position]:
                    cube.rect.x += offset
                    if pg.Rect.collidelist(cube.rect, [cube.rect for cube in map[cube.rect.y // 25]]) != -1:
                        return
                    elif cube.rect.x < 225:
                        return
                self.reference_cube.x += offset
            elif r > l:
                offset = 25
                for cube in positions[next_position]:
                    cube.rect.x += offset
                    if pg.Rect.collidelist(cube.rect, [cube.rect for cube in map[cube.rect.y // 25]]) != -1:
                        return
                    elif cube.rect.x > 450:
                        return
                self.reference_cube.x += offset

        self.position = next_position
        self.cubes.clear()
        for cube in positions[next_position]:
            self.cubes.append(cube)

    # Returns a list of cubes that make up the piece
    def get_cubes(self):
        aggregated_cubes = [cube for cube in self.cubes]
        return aggregated_cubes


class Ipiece:
    def __init__(self):
        self.reference_cube = pg.rect.Rect(325, 0, 50, 50)
        self.position = 1
        self.cubes = [
            Cube("light_blue", self.reference_cube.x -25, self.reference_cube.y),
            Cube("light_blue", self.reference_cube.x, self.reference_cube.y), 
            Cube("light_blue", self.reference_cube.x + 25, self.reference_cube.y),
            Cube("light_blue", self.reference_cube.x + 50, self.reference_cube.y)]

    def move(self, map, direction):
        if direction == "down":
            self.reference_cube.y += 25
            for cube in self.cubes:
                cube.move("down")
        elif direction == "left":
            for cube in self.cubes:
                if cube.rect.x - 25 < 225:
                    return
                else:
                    for mapped_cube in map[cube.rect.y // 25]:
                        if mapped_cube.rect.x == cube.rect.x - 25:
                            return
            self.reference_cube.x -= 25
            for cube in self.cubes:
                cube.move("left")
        elif direction == "right":
            for cube in self.cubes:
                if cube.rect.x + 25 > 450:
                    return
                else:
                    for mapped_cube in map[cube.rect.y // 25]:
                        if mapped_cube.rect.x == cube.rect.x + 25:
                            return
            self.reference_cube.x += 25
            for cube in self.cubes:
                cube.move("right")


    def draw(self, screen):
        for cube in self.cubes:
            cube.draw(screen)


    def get_cubes(self):
        return [cube for cube in self.cubes]
    

    def rotate(self, map):
        if self.position == 4:
            next_position = 1
        else:
            next_position = self.position + 1
        positions = {
        1: [Cube("light_blue", self.reference_cube.x -25, self.reference_cube.y),
            Cube("light_blue", self.reference_cube.x, self.reference_cube.y), 
            Cube("light_blue", self.reference_cube.x + 25, self.reference_cube.y),
            Cube("light_blue", self.reference_cube.x + 50, self.reference_cube.y)],

        2: [Cube("light_blue", self.reference_cube.x + 25, self.reference_cube.y - 25),
            Cube("light_blue", self.reference_cube.x + 25, self.reference_cube.y), 
            Cube("light_blue", self.reference_cube.x + 25, self.reference_cube.y + 25), 
            Cube("light_blue", self.reference_cube.x + 25, self.reference_cube.y + 50)],

        3: [Cube("light_blue", self.reference_cube.x - 25, self.reference_cube.y + 25),
            Cube("light_blue", self.reference_cube.x, self.reference_cube.y + 25), 
            Cube("light_blue", self.reference_cube.x + 25, self.reference_cube.y + 25), 
            Cube("light_blue", self.reference_cube.x + 50, self.reference_cube.y + 25)],

        4: [Cube("light_blue", self.reference_cube.x, self.reference_cube.y -25),
            Cube("light_blue", self.reference_cube.x, self.reference_cube.y), 
            Cube("light_blue", self.reference_cube.x, self.reference_cube.y + 25), 
            Cube("light_blue", self.reference_cube.x, self.reference_cube.y + 50)]
        }

        map_cubes_collided = []
        cube_collision = False
        boarder_collision = False
        for cube in positions[next_position]:
            if cube.rect.y > 475:
                return
            if cube.rect.x > 450 or cube.rect.x < 225:
                    boarder_collision = True
            for mapped_cube in map[cube.rect.y // 25]:
                if pg.Rect.colliderect(cube.rect, mapped_cube.rect):
                    cube_collision = True
                    map_cubes_collided.append(mapped_cube)
        cubes_to_left = []
        cubes_to_right = []
        if cube_collision and boarder_collision:
            return
        elif cube_collision:
            # Checks of Ipiece is vertical because there is no bump upwards.
            if next_position == 2 or next_position == 4:
                return
            elif len(map_cubes_collided) == 1:
                for cube in positions[next_position]:
                    if cube.rect.x < map_cubes_collided[0].rect.x:
                        cubes_to_left.append(cube)
                    elif cube.rect.x > map_cubes_collided[0].rect.x:
                        cubes_to_right.append(cube)
                if len(cubes_to_right) > len(cubes_to_left):
                    offset = (25 * len(cubes_to_left)) + 25
                    for cube in positions[next_position]:
                        cube.rect.x += offset
                        if pg.Rect.collidelist(cube.rect, [map_cube.rect for map_cube in map[cube.rect.y // 25]]) != -1:
                            return
                        elif cube.rect.x < 225 or cube.rect.x > 450:
                            return
                    self.reference_cube.x += offset
                elif len(cubes_to_right) < len(cubes_to_left):
                    offset = (-25 * len(cubes_to_right)) - 25
                    for cube in positions[next_position]:
                        cube.rect.x += offset
                        if pg.Rect.collidelist(cube.rect, [map_cube.rect for map_cube in map[cube.rect.y // 25]]) != -1:
                            return
                        elif cube.rect.x < 225 or cube.rect.x > 450:
                            return
                    self.reference_cube.x += offset
            else:
                # Converts the listed cubes collided with on the map into their x-values as integers
                for i in map_cubes_collided:
                    map_cubes_collided[map_cubes_collided.index(i)] = i.rect.x
                for i in range(0, len(map_cubes_collided) - 1):
                    if map_cubes_collided[i + 1] - map_cubes_collided[i] > 25:
                        return
                # Code to offset next_position
                if positions[next_position][0].rect.x < map_cubes_collided[0]:
                    for cube in positions[next_position]:
                        cube.rect.x -= 50
                        if pg.Rect.collidelist(cube.rect, [map_cube.rect for map_cube in map[cube.rect.y // 25]]) != -1:
                                return
                        elif cube.rect.x < 225:
                            return
                    self.reference_cube.x -= 50
                else:
                    for cube in positions[next_position]:
                        cube.rect.x += 50
                        if pg.Rect.collidelist(cube.rect, [map_cube.rect for map_cube in map[cube.rect.y // 25]]) != -1:
                                return
                        elif cube.rect.x > 450:
                            return
                    self.reference_cube.x += 50
        elif boarder_collision:
            offset = 0     
            # Code to offset based on boarder overlap
            if positions[next_position][0].rect.x < 225:
                offset =  225 - positions[next_position][0].rect.x
            elif positions[next_position][3].rect.x > 450:
                offset = 450 - positions[next_position][3].rect.x
            for cube in positions[next_position]:
                cube.rect.x += offset
                if pg.Rect.collidelist(cube.rect, [map_cube.rect for map_cube in map[cube.rect.y // 25]]) != -1:
                    return
            self.reference_cube.x += offset

        self.cubes.clear()
        for cube in positions[next_position]:
            self.cubes.append(cube)
        self.position = next_position

