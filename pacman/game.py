import pygame
import os
from sys import exit
from constants import *
from menu import Menu
from game_process import GameProcess
from table_records import TableRecords
from scene import Scene
from load_levels import LoadLevels
from control import Control


class Game:
    def __init__(self):
        pygame.mixer.music.play(-1)
        self.screen = pygame.display.set_mode(SIZE)
        self.close_app = False
        self.scene = Menu()
        self.scenes = {proceed_game_single: GameProcess, proceed_game_double: GameProcess,
                       proceed_table_records: TableRecords, proceed_close_app: Exit, proceed_menu: Menu,
                       proceed_levels: LoadLevels, proceed_control: Control}

    def main_loop(self):
        while not self.close_app:
            self.process_events()
            self.process_logic()
            self.process_drawing()
            pygame.time.wait(FPS)

    def process_events(self):
        for event in pygame.event.get():
            self.scene.process_events(event)
            if event.type == pygame.QUIT:
                self.close_app = True

    def process_logic(self):
        if self.scene.next_scene is not None:
            if proceed_game_single in self.scene.next_scene:
                self.scene = self.scenes[proceed_game_single](1, int(self.scene.next_scene[-1]))
            elif proceed_game_double in self.scene.next_scene:
                self.scene = self.scenes[proceed_game_single](2, int(self.scene.next_scene[-1]))
            else:
                self.scene = self.scenes[self.scene.next_scene]()
        self.scene.process_logic()

    def process_drawing(self):
        self.screen.fill((62, 58, 97))
        self.scene.draw(self.screen)
        pygame.display.flip()


class Exit(Scene):

    def process_logic(self):
        exit()
