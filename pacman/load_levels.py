import pygame
from button import Button
from scene import Scene
from constants import (HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT, LIGHT_ORANGE, BUTTON_STYLE, WIDTH, proceed_game_single, proceed_menu)


class LoadLevels(Scene):
    def __init__(self):
        self.number_press_button = 0
        spacing_ratio = 80
        buttons_in_col = 5
        origin_y = 70
        self.buttons_left = [Button((int(i > buttons_in_col)*3*(WIDTH-BUTTON_WIDTH)/4 +
                                     int(i <= buttons_in_col)*(WIDTH-BUTTON_WIDTH)/4,
                                     origin_y+((i-1) % buttons_in_col)*spacing_ratio, BUTTON_WIDTH, BUTTON_HEIGHT),
                                    LIGHT_ORANGE, self.proceed_game_single, text="Уровень {}".format(i),
                                    **BUTTON_STYLE)
                             for i in range(1, 11)]
        self.button_back = Button((10, HEIGHT-BUTTON_HEIGHT-10 , BUTTON_WIDTH, BUTTON_HEIGHT), LIGHT_ORANGE,
                                  self.proceed_menu, text='Back to menu', font=pygame.font.SysFont('Comic Sans MS', 42),
                                  **BUTTON_STYLE)

    def proceed_game_single(self):
        self.next_scene = proceed_game_single + str(self.number_press_button)

    def proceed_menu(self):
        self.next_scene = proceed_menu

    def process_events(self, event):
        self.button_back.check_event(event)
        for i in range(len(self.buttons_left)):
            self.number_press_button = i + 1
            self.buttons_left[i].check_event(event)

    def draw(self, screen):
        self.button_back.update(screen)
        for button in self.buttons_left:
            button.update(screen)
