import os
import pygame
from moving_objects import MovingObject
from constants import ANIMATION_TICK

# TODO Добавить вызов метода `eat()` в функцию `collision_hero_and_grains()`
# TODO Разобраться с задержкой перед запуском звука

class Pacman(MovingObject):

    image0 = pygame.image.load('image/pacman/body.png')
    image1 = pygame.image.load('image/pacman/body_eating.png')

    sound_eat = None

    def __init__(self, x, y, width, height, speed, color, score=0, hp=3):
        # Перед загрузкой звуков нужно инициализироваит pygame
        if Pacman.sound_eat == None:
            Pacman.sound_eat = pygame.mixer.Sound(os.path.join('sound', 'pacman', 'eat.wav'))

        super().__init__(x, y, width, height, speed, color)

        self.score = score
        self.hp = hp
        self.tick = None   #Для анимации

        self.image_base0 = pygame.transform.scale(Pacman.image0,
            (self.rect.width, self.rect.height))
        self.image_base1 = pygame.transform.scale(Pacman.image1,
            (self.rect.width, self.rect.height))
        
        self.image = self.current_base_img = self.image_base0
    
    def check_events(self, event, number_pacman):
        if event.type == pygame.KEYDOWN:
            if number_pacman == 1:
                if event.key == pygame.K_w:
                    self.potential_action = 1
                elif event.key == pygame.K_a:
                    self.potential_action = 2
                elif event.key == pygame.K_s:
                    self.potential_action = 3
                elif event.key == pygame.K_d:
                    self.potential_action = 4
            elif number_pacman == 2:
                if event.key == pygame.K_UP:
                    self.potential_action = 1
                elif event.key == pygame.K_LEFT:
                    self.potential_action = 2
                elif event.key == pygame.K_DOWN:
                    self.potential_action = 3
                elif event.key == pygame.K_RIGHT:
                    self.potential_action = 4
    
    def set_way(self):
        super().set_way()

        if self.tick != None:
            self.tick += 1
            if self.tick == ANIMATION_TICK:
                self.current_base_img = self.image_base0
                self.tick = None

        self.image = pygame.transform.rotate(self.current_base_img, self.directions.get(self.current_action)[2])
        
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def is_alive(self):
        return self.hp > 0

    def eat(self):
        Pacman.sound_eat.play()
        self.current_base_img = self.image_base1
        self.tick = 0
