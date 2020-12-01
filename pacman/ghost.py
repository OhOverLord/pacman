import os
import pygame
from moving_objects import MovingObject
from random import randint
import time
import math

class Ghost(MovingObject):
    imageGhost = pygame.image.load('image/ghost/Ghost.png')
    imageGhostWhite = pygame.image.load('image/ghost/GhostWhite.png')
    imageGhostFear = pygame.image.load('image/ghost/GhostFear.png')
    imageGhostRun = pygame.image.load('image/ghost/GhostRun.png')
    imageGhostWhiteRun = pygame.image.load('image/ghost/GhostWhiteRun.png')
    imageGhostFearRun = pygame.image.load('image/ghost/GhostFearRun.png')

    def __init__(self, x, y, width, height, speed, color,fear = False,death = False):
        super().__init__(x, y, width, height, speed, color)
        self.image0 = pygame.transform.scale(Ghost.imageGhost,(self.rect.width, self.rect.height))
        self.image0Run = pygame.transform.scale(Ghost.imageGhostRun, (self.rect.width, self.rect.height))
        self.image1 = pygame.transform.scale(Ghost.imageGhostFear, (self.rect.width, self.rect.height))
        self.image1Run = pygame.transform.scale(Ghost.imageGhostFearRun, (self.rect.width, self.rect.height))
        self.image2 = pygame.transform.scale(Ghost.imageGhostWhite, (self.rect.width, self.rect.height))
        self.image2Run = pygame.transform.scale(Ghost.imageGhostWhiteRun, (self.rect.width, self.rect.height))
        self.modes = {'standart': [self.image0,self.image0Run], 'fear':  [self.image1,self.image1Run], 'invisibility':  [self.image2,self.image2Run]}
        self.current_mode = self.later_mode = 'standart'
        self.current_action = randint(1, 4)
        self.fear = fear
        self.t = time.time()
        self.t2 = time.time()
        self.death = death


    def kill(self):
        sound = pygame.mixer.Sound(os.path.join('sound', 'pacman_death.wav'))
        sound.play()

    def new_time_fear(self):
        self.t = time.time()

    def new_time_death(self):
        self.t2 = time.time()

    def run(self,screen,mode = 'standart'):
        screen.blit(self.modes[mode][0], self.rect)
        if math.floor(time.time() * 10) % 2 == 0:
            screen.blit(self.modes[mode][1], self.rect)

    def draw(self, screen):
        if self.fear:
            if abs(self.t - time.time()) > 5 and math.floor(time.time()) % 2 == 0:
                self.run(screen,'invisibility')
            else:
                self.run(screen,'fear')
            if abs(self.t - time.time()) > 10:
                self.fear = False
                self.t = time.time()
        elif self.death:
            self.run(screen,'invisibility')
            if abs(self.t2 - time.time()) > 3:
                self.death = False
                self.t2 = time.time()
        else:
            self.run(screen)
