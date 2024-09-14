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
        self.x = x_position
        self.y = y_position
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
    

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
