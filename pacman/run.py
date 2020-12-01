#!/usr/bin/env python

import pygame
import os

from game import Game

def main():
    pygame.mixer.pre_init(22050, -16, 1, 32)
    pygame.init()
    pygame.mixer.music.load(os.path.join('sound', "pacman_beginning.wav"))

    pygame.font.init()
    pygame.display.set_caption('Pacman')
    pygame.display.set_icon(pygame.image.load('image/pacman/body.png'))
    g = Game()
    g.main_loop()


if __name__ == "__main__":
    main()
