import pygame as pg
import os
pg.init()


class Button:
    def __init__(self, width: float, height: float, coords: tuple, color: tuple, caption: str):
        self.pressed = False
        font_size = int(height / (5/3))
        self.color = color
        font = pg.font.Font(os.path.join("assets", "gomarice_no_continue.ttf"), font_size)
        self.caption = font.render(caption, True, (0, 0, 0))
        while self.caption.get_width() > width:
            font_size -= int(font_size//10)
            font = pg.font.Font(os.path.join("assets", "gomarice_no_continue.ttf"), font_size)
            self.caption = font.render(caption, True, (0, 0, 0))
        pressed_font = pg.font.Font(os.path.join("assets", "gomarice_no_continue.ttf"), int(font_size * .80))
        self.pressed_caption = pressed_font.render(caption, True, (0, 0, 0))
        self.rect = pg.rect.Rect(coords[0], coords[1], width, height)
        pressed_width = width * .80
        pressed_height = height * .80
        pressed_x = coords[0] + ((width - pressed_width)/2)
        pressed_y = coords[1] + ((height - pressed_height)/2)
        self.pressed_rect = pg.rect.Rect(pressed_x, pressed_y, pressed_width, pressed_height)

    
    def draw(self, screen):
        if not self.pressed:
            pg.draw.rect(screen, self.color, self.rect)
            caption_x = (self.rect.width - self.caption.get_width())/2 + self.rect.x
            caption_y = (self.rect.height - self.caption.get_height())/2 + self.rect.y
            screen.blit(self.caption, (caption_x, caption_y))
        else:
            pg.draw.rect(screen, (150, 150, 150), self.pressed_rect)
            pressed_caption_x = (self.pressed_rect.width - self.pressed_caption.get_width())/2 + self.pressed_rect.x
            pressed_caption_y = (self.pressed_rect.height - self.pressed_caption.get_height())/2 + self.pressed_rect.y
            screen.blit(self.pressed_caption, (pressed_caption_x, pressed_caption_y))


def main():
    width = 500
    height = 500
    SCREEN = pg.display.set_mode((width, height))
    playgame = True
    clock = pg.time.Clock()
    test_button = Button(150, 50, (width/2 - 75, height/2 - 25), (255, 255, 255), "HI")
    test_button2 = Button(150, 50, (width/2 - 75, height/3 - 25), (255, 255, 255), "Main Menu")

    while playgame:
        clock.tick(30)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                playgame = False
        SCREEN.fill((0, 0, 0))
        test_button.draw(SCREEN)
        test_button2.draw(SCREEN)
        pg.display.update()
    pg.quit()

if __name__ == "__main__":
    main()
