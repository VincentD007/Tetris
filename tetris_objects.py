import pygame as pg
pg.init()

purple_block = pg.transform.scale(pg.image.load("purple_block.png"), (25, 25))
blue_block = pg.transform.scale(pg.image.load("blue_block.png"), (25, 25))
gold_block = pg.transform.scale(pg.image.load("gold_block.png"), (25, 25))
green_block = pg.transform.scale(pg.image.load("green_block.png"), (25, 25))
light_blue_block = pg.transform.scale(pg.image.load("light_blue_block.png"), (25, 25))
red_block = pg.transform.scale(pg.image.load("red_block.png"), (25, 25))
yellow_block = pg.transform.scale(pg.image.load("yellow_block.png"), (25, 25))

class Cube:
    def __init__(self, color, x_position, y_position) -> None:
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
    def __init__(self) -> None:
        self.reference_cube = Cube("purple", 350, 0)
        self.position = 1
        self.follower_cubes = [
            Cube("purple", self.reference_cube.rect.x, self.reference_cube.rect.y - 25), 
            Cube("purple", self.reference_cube.rect.x + 25, self.reference_cube.rect.y),
            Cube("purple", self.reference_cube.rect.x - 25, self.reference_cube.rect.y)]


    def move(self, map, direction):
        if direction == "down":
            self.reference_cube.rect.y += 25
            for cube in self.follower_cubes:
                cube.move("down")
        elif direction == "left":
            if self.position != 2:
                if self.reference_cube.rect.x > 250:
                    self.reference_cube.move("left")
                    for cube in self.follower_cubes:
                        cube.move("left")
            else:
                if self.reference_cube.rect.x > 225:
                    self.reference_cube.move("left")
                    for cube in self.follower_cubes:
                        cube.move("left")
        elif direction == "right":
            if self.position != 4:
                if self.reference_cube.rect.x < 425:
                    self.reference_cube.move("right")
                    for cube in self.follower_cubes:
                        cube.move("right")
            else:
                if self.reference_cube.rect.x < 450:
                    self.reference_cube.move("right")
                    for cube in self.follower_cubes:
                        cube.move("right")
 

    def draw(self, screen):
        self.reference_cube.draw(screen)
        for cube in self.follower_cubes:
            cube.draw(screen)


    def rotate(self, map):
        positions = {
        1: [Cube("purple", self.reference_cube.rect.x, self.reference_cube.rect.y - 25), 
            Cube("purple", self.reference_cube.rect.x + 25, self.reference_cube.rect.y),
            Cube("purple", self.reference_cube.rect.x - 25, self.reference_cube.rect.y)],

        2: [Cube("purple", self.reference_cube.rect.x, self.reference_cube.rect.y - 25), 
            Cube("purple", self.reference_cube.rect.x, self.reference_cube.rect.y + 25), 
            Cube("purple", self.reference_cube.rect.x + 25, self.reference_cube.rect.y)],

        3: [Cube("purple", self.reference_cube.rect.x, self.reference_cube.rect.y + 25), 
            Cube("purple", self.reference_cube.rect.x + 25, self.reference_cube.rect.y), 
            Cube("purple", self.reference_cube.rect.x - 25, self.reference_cube.rect.y)],

        4: [Cube("purple", self.reference_cube.rect.x, self.reference_cube.rect.y - 25), 
            Cube("purple", self.reference_cube.rect.x, self.reference_cube.rect.y + 25), 
            Cube("purple", self.reference_cube.rect.x - 25, self.reference_cube.rect.y)]
        }

        if self.reference_cube.rect.x != 225 and self.reference_cube.rect.x != 450:
            if self.position == 4:
                for cube in positions[1]:
                    for mapcube in map[cube.rect.y // 25]:
                        if mapcube.rect.x == cube.rect.x:
                            return
                self.position = 1
            else:
                for cube in positions[self.position + 1]:
                    for mapcube in map[cube.rect.y // 25]:
                        if mapcube.rect.x == cube.rect.x:
                            return
                self.position += 1
        else:
            if self.reference_cube.rect.x == 225:
                for cube in positions[3]:
                    for mapcube in map[cube.rect.y // 25]:
                        if cube.rect.x + 25 == mapcube.rect.x:
                            return
                self.position = 3
                self.reference_cube.move("right")
                for cube in positions[3]:
                    cube.move("right")
            else:
                for cube in positions[1]:
                    for mapcube in map[cube.rect.y // 25]:
                        if cube.rect.x - 25 == mapcube.rect.x:
                            return
                self.position = 1
                self.reference_cube.move("left")
                for cube in positions[1]:
                    cube.move("left")
        self.follower_cubes.clear()
        for cube in positions[self.position]:
            self.follower_cubes.append(cube)


    def get_cubes(self):
        aggregated_cubes = [cube for cube in self.follower_cubes]
        aggregated_cubes.append(self.reference_cube)
        return aggregated_cubes



class Map:
    def __init__(self) -> None:  
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
