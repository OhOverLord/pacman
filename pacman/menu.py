import pygame
import os
from gif import GIFImage
from scene import Scene
from enter_text import InputBox
from button import Button
from facts import Facts
from constants import LIGHT_ORANGE, BUTTON_STYLE, WIDTH, proceed_levels, proceed_close_app, proceed_game_double, \
    proceed_game_single, proceed_table_records, proceed_control, BUTTON_HEIGHT, MENU_BUTTON_SPACING, BUTTON_WIDTH


class Menu(Scene):
    def __init__(self, origin_y=100, height=BUTTON_HEIGHT, width=BUTTON_WIDTH, spacing=MENU_BUTTON_SPACING):
        self.objects = []
        self.buttons_height = height
        self.width = width
        self.buttons_spacing = spacing
        self.y = origin_y
        self.gif = GIFImage('anim.gif')
        self.inputbox_id = 0
        cursor_path = os.path.join('cursors', 'cursor_pacman_text.xbm')
        self.text_cursor = pygame.cursors.load_xbm(cursor_path, cursor_path)
        self.prepare_scene()
        self.facts = Facts()

    def prepare_scene(self):
        button_labels = ['Single', 'Double', 'Levels', 'Table records', 'How to play', 'Exit']
        button_functions = [self.proceed_game_single, self.proceed_game_double, self.proceed_levels,
                            self.proceed_table_records, self.proceed_control, self.proceed_close_app]

        for i in range(len(button_labels)):
            self.objects.append(Button((WIDTH / 2 - self.width / 2,
                self.y + i * (self.buttons_height + self.buttons_spacing), BUTTON_WIDTH, self.buttons_height),
                LIGHT_ORANGE, button_functions[i], text=button_labels[i], font=pygame.font.SysFont('Comic Sans MS', 42),
                **BUTTON_STYLE))
        f = open('players.txt', 'r')
        players = f.read().split(sep=',')
        f.close()

        self.inputbox_id = len(self.objects)
        self.objects.append(InputBox(0, 0, 200, 40, 0, players[0]))
        self.objects.append(InputBox(WIDTH-200, 0, 200, 40, 1, players[1]))

    def process_events(self, event):
        if self.objects[self.inputbox_id].active or self.objects[self.inputbox_id+1].active:
            pygame.mouse.set_cursor(*self.text_cursor)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
        for object in self.objects:
            object.check_event(event)

    def proceed_game_single(self):
        self.next_scene = proceed_game_single + '1'

    def proceed_game_double(self):
        self.next_scene = proceed_game_double + '1'

    def proceed_levels(self):
        self.next_scene = proceed_levels

    def proceed_table_records(self):
        self.next_scene = proceed_table_records

    def proceed_control(self):
        self.next_scene = proceed_control

    def proceed_close_app(self):
        self.next_scene = proceed_close_app

    def draw(self, screen):
        self.gif.render(screen, (0, 0))
        for object in self.objects:
            object.draw(screen)
        self.facts.draw(screen)
