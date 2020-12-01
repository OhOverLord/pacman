import pygame

class MovingObject():
    def __init__(self, x, y, width, height, speed, color):
        self.color = color
        self.speed = speed
        self.rect = pygame.Rect(x, y, width, height)
        self.shift_x = self.shift_y = 0
        self.current_action = self.potential_action = 0
        self.directions = {0: [0, 0, 0], 1: [0, -1, 90], 2: [-1, 0, 180], 3: [0, 1, 270], 4: [1, 0, 360]}
    def set_way(self):
        self.shift_x = self.directions[self.current_action][0] * self.speed
        self.shift_y = self.directions[self.current_action][1] * self.speed
    def move(self):
        self.rect.x += self.shift_x
        self.rect.y += self.shift_y
    def draw(self,screen):
        pygame.draw.rect(screen, self.color, self.rect)
