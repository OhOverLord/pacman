import pygame
from scene import Scene
from button import Button
from text import Text
from cell import Grain
from pacman import Pacman
from constants import BLACK, LIGHT_ORANGE, DARK_ORANGE, HEIGHT, BUTTON_STYLE, BUTTON_HEIGHT, BUTTON_WIDTH, LIGHT_BLUE, proceed_menu


class Control(Scene):
    def __init__(self):
        texts_color = LIGHT_BLUE
        origin_y = 20
        self.objects = []
        self.objects.append(Button((10, HEIGHT-BUTTON_HEIGHT-10 , BUTTON_WIDTH, BUTTON_HEIGHT), LIGHT_ORANGE,
                                  self.back_to_menu, text='Back to menu', font=pygame.font.SysFont('Comic Sans MS', 42),
                                  **BUTTON_STYLE))
        self.objects.append(Text(20, origin_y +  0, 'Player #1: WASD', color=texts_color))
        self.objects.append(Text(20, origin_y + 30, 'Player #2: arrow keys', color=texts_color))
        self.objects.append(Text(20, origin_y + 60, 'Press P to pause/continue', color=texts_color))
        self.objects.append(Text(20, origin_y + 90, 'Press R to restart level (lose pts and refresh hp)', color=texts_color))

        self.objects.append(Text(20, origin_y + 300, 'You get points by eating grains and ghosts (Fear mode)', color=texts_color))
        self.objects.append(Text(20, origin_y + 330, 'Try to avoid the ghosts while not in Fear mod', color=texts_color))
        self.objects.append(Text(20, origin_y + 360, 'To activate Fear mode eat a big grain', color=texts_color))
        self.objects.append(Text(20, origin_y + 390, 'Teleportation costs 10 pts', color=texts_color))

        self.objects.append(Text(15+BUTTON_WIDTH, HEIGHT-BUTTON_HEIGHT/2-20, 'Good luck!', color=LIGHT_ORANGE))

        self.objects.append(Grain(120, 175, 100, 100, 0, LIGHT_ORANGE))
        self.objects.append(Grain(220, 175, 100, 100, 0, LIGHT_ORANGE))
        self.objects.append(Grain(320, 175, 100, 100, 0, LIGHT_ORANGE))
        self.objects.append(Pacman(10, 165, 120, 120, 1, None, 1))

    def process_events(self, event):
        self.objects[0].check_event(event)

    def draw(self, screen):
        for object in self.objects:
            object.draw(screen)

    def back_to_menu(self):
        self.next_scene = proceed_menu
