import pygame
import constants


class Cell:

    def __init__(self, x, y, width, height, type, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.type = type
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Floor(Cell):

    def __init__(self, x, y, width, height, type, color):
        super().__init__(x, y, width, height, type, color)

    def draw(self, screen):
        pass
        #pygame.draw.rect(screen, constants.LIGHT_ORANGE, self.rect)


class Wall(Cell):

    def __init__(self, x, y, width, height, type, color):
        super().__init__(x, y, width, height, type, color)

    def draw(self, screen):
        pass
        #pygame.draw.rect(screen, constants.BROWN, self.rect)



class Grain(Cell):

    def __init__(self, x, y, width, height, type, color):
        super().__init__(x, y, width, height, type, color)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color,
                           (self.rect.centerx, self.rect.centery), (self.rect.width + self.rect.height) // 10)


class SuperGrain(Grain):
    def __init__(self, x, y, width, height, type, color):
        super().__init__(x, y, width, height, type, color)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color,
                           (self.rect.centerx, self.rect.centery), (self.rect.height + self.rect.width) // 5)


class Teleport(Cell):
    def __init__(self, x, y, width, height, type, color):
        super().__init__(x, y, width, height, type, color)
