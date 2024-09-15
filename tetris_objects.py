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
        self.x, self.y = x_position, y_position
        self.rect = self.image.get_rect(topleft = (self.x, self.y))

 
    def move(self):
        self.y += 25
    

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Tpiece:
    def __init__(self) -> None:
        self.reference_cube = Cube("purple", 350, 100)
        self.position = 1


    def move(self, direction):
        if direction == "down":
            self.reference_cube.y += 25
        elif direction == "left":
            if self.position != 2:
                if self.reference_cube.x > 250:
                    self.reference_cube.x -= 25
            else:
                if self.reference_cube.x > 225:
                    self.reference_cube.x -= 25
        elif direction == "right":
            if self.position != 4:
                if self.reference_cube.x < 425:
                    self.reference_cube.x += 25
            else:
                if self.reference_cube.x < 450:
                    self.reference_cube.x += 25

    def draw(self, screen):
        positions = {
        1: [Cube("purple", self.reference_cube.x, self.reference_cube.y - 25), 
            Cube("purple", self.reference_cube.x + 25, self.reference_cube.y),
            Cube("purple", self.reference_cube.x - 25, self.reference_cube.y)],

        2: [Cube("purple", self.reference_cube.x, self.reference_cube.y - 25), 
            Cube("purple", self.reference_cube.x, self.reference_cube.y + 25), 
            Cube("purple", self.reference_cube.x + 25, self.reference_cube.y)],

        3: [Cube("purple", self.reference_cube.x, self.reference_cube.y + 25), 
            Cube("purple", self.reference_cube.x + 25, self.reference_cube.y), 
            Cube("purple", self.reference_cube.x - 25, self.reference_cube.y)],

        4: [Cube("purple", self.reference_cube.x, self.reference_cube.y - 25), 
            Cube("purple", self.reference_cube.x, self.reference_cube.y + 25), 
            Cube("purple", self.reference_cube.x - 25, self.reference_cube.y)]
        }

        self.reference_cube.draw(screen)
        for cube in positions[self.position]:
            cube.draw(screen)


    def rotate(self):
        if self.reference_cube.x == 225:
            self.reference_cube.x += 25
        elif self.reference_cube.x == 450:
            self.reference_cube.x -= 25
        if self.position != 4:
            self.position += 1
        else:
            self.position = 1


class Map:
    def __init__(self) -> None:  
        self.map = [[], [], [], [], [], [], [], [], [], []]
