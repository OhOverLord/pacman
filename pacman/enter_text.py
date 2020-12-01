import pygame as pg
from constants import LIGHT_ORANGE, DARK_ORANGE, LIGHT_BLUE


class InputBox:

    def __init__(self, x, y, w, h, n, text=''):
        self.font = pg.font.Font(None, 32)
        self.rect = pg.Rect(x, y, w, h)
        self.color = DARK_ORANGE
        self.text = text
        self.n = n
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        self.color_active = DARK_ORANGE
        self.color_inactive = LIGHT_ORANGE

    def check_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
                f = open('players.txt', 'r')
                data = f.read().split(sep=',')
                f.close()
                f = open('players.txt', 'w')
                if self.n == 0:
                    f.write('{},{}'.format(self.text, data[1]))
                else:
                    f.write('{},{}'.format(data[0], self.text))
                f.close()
            self.color = self.color_active if self.active else self.color_inactive
            if len(self.text) == 0:
                self.text = 'Vacuum'
                self.txt_surface = self.font.render(self.text, True, self.color_active)
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    f = open('players.txt', 'r')
                    data = f.read().split(sep=',')
                    f.close()
                    f = open('players.txt', 'w')
                    if len(self.text) == 0:
                        self.text = 'Vacuum'
                    if self.n == 0:
                        f.write('{},{}'.format(self.text, data[1]))
                    else:
                        f.write('{},{}'.format(data[0], self.text))
                    f.close()
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif self.txt_surface.get_width() < self.rect.width - 30:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        pg.draw.rect(screen, LIGHT_BLUE, self.rect, 0)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pg.draw.rect(screen, self.color, self.rect, 5 if self.active else 2)
