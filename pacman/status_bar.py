import pygame
import constants


class StatusBar:
    def __init__(self, x, y):
        self.red = 15
        self.green = 255
        self.blue = 245
        self.pos = (x, y)
        self.font = pygame.font.SysFont('Comic Sans MS', constants.HEIGHT_CELL)

    def draw(self, screen, text):
        surface = self.font.render(text, 1, (self.red, self.green, self.blue))
        screen.blit(surface, self.pos)
        self.color_change()

    def color_change(self):
        speed = 5
        if self.blue >= 255:
            self.green += speed
            self.red -= speed

        if self.green >= 255:
            self.red += speed
            self.blue -= speed

        if self.red >= 255:
            self.green -= speed
            self.blue += speed