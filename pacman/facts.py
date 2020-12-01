import pygame as pg
import constants
import random
import time


class Facts:

    def __init__(self):
        self.data = []
        f = open('tips_and_facts.txt', 'r')
        self.data = f.read().split('.\n')
        f.close()
        self.font = pg.font.SysFont('Comic Sans MS', 30)
        self.rand = random.randint(0, 17)
        self.t = time.time()

    def draw(self, screen):
        back = pg.Surface((800, 30))
        if abs(self.t - time.time()) > 5:
            self.rand = random.randint(0, len(self.data) - 1)
            self.t = time.time()
        text = self.font.render(self.data[self.rand], 1, (0, 0, 0))
        back.fill(constants.GOLD)
        back.blit(text, (0, 0))
        screen.blit(back, (0, 50))




