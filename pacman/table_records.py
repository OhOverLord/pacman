import pygame as pg
from scene import Scene
from button import Button
from table import Table
from constants import (WIDTH, HEIGHT, LIGHT_ORANGE, LIGHT_LIGHT_ORANGE, BUTTON_STYLE, BUTTON_HEIGHT, BUTTON_WIDTH, proceed_menu)


class TableRecords(Scene):
    def __init__(self):
        self.count_records = 10
        self.records = [0] * 10
        self.texts = ['Rank:', 'Score:', 'Name:']
        self.font = pg.font.SysFont('Comic Sans MS', 50)
        self.button_back = Button((10, HEIGHT-BUTTON_HEIGHT-10 , BUTTON_WIDTH, BUTTON_HEIGHT), LIGHT_ORANGE,
                                  self.proceed_menu, text='Back to menu', font=pg.font.SysFont('Comic Sans MS', 42),
                                  **BUTTON_STYLE)
        self.table = Table()

    def proceed_menu(self):
        self.next_scene = proceed_menu

    def process_events(self, event):
        self.button_back.check_event(event)

    def draw(self, screen):
        self.button_back.update(screen)
        font_l = pg.font.SysFont('Comic Sans MS', 80)
        label = font_l.render('Table of records', 1, LIGHT_LIGHT_ORANGE)
        screen.blit(label, ((WIDTH - label.get_rect().width) // 2, 5))
        for i in range(len(self.texts)):
            text = self.font.render(self.texts[i], 1, LIGHT_LIGHT_ORANGE)
            cur_x = 100 + ((200 - text.get_rect().width) // 2) + 200 * i
            screen.blit(text, (cur_x, label.get_rect().height + 10))
        self.table.draw(screen, label.get_rect().height + text.get_rect().height + 20,
                        self.font, self.count_records)
