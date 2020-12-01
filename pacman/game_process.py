import os
from random import randint
from sys import exit
from cell import *
from constants import *
from pacman import Pacman
from scene import Scene
from ghost import Ghost
from button import Button
from system_score import SystemScore
from status_bar import StatusBar
from text import Text


class GameProcess(Scene):
    def __init__(self, count_pacmans, level):
        self.count_pacmans = count_pacmans
        self.level = level
        self.game_over = False
        self.fear = False
        self.pause = True
        self.walls = []
        self.floor = []
        self.grains = []
        self.ghosts = []
        self.pacmans = []
        self.status_bars = []
        self.teleports = []
        self.initial_coordinates = dict()
        self.buttons = []
        self.system_score = SystemScore()
        self.prepare_scene()

        self.victory_sound = pygame.mixer.Sound(os.path.join('sound', 'victory.wav'))

    def prepare_scene(self):
        self.initial_coordinates = {'pacmans': [], 'ghosts': []}
        scores = []
        hp = []
        for i in range(self.count_pacmans):
            scores.append(0)
            hp.append(3)
        self.load_playing_field(scores, hp)

        btn_origin_y = 390
        btn_origin_x = WIDTH - 20 - BUTTON_WIDTH
        spacing = 30 + BUTTON_HEIGHT

        self.buttons.append(Button((btn_origin_x, btn_origin_y, BUTTON_WIDTH, BUTTON_HEIGHT), LIGHT_ORANGE, self.menu,
                                   text='Back to menu', **BUTTON_STYLE))
        self.buttons.append(Button((btn_origin_x, btn_origin_y - spacing, BUTTON_WIDTH, BUTTON_HEIGHT), LIGHT_ORANGE,
                                   self.restart, text='Restart', **BUTTON_STYLE))
        self.buttons.append(Button((btn_origin_x, btn_origin_y - 2 * spacing, BUTTON_WIDTH, BUTTON_HEIGHT),
                                   LIGHT_ORANGE, self.write_data, text='Save score', **BUTTON_STYLE))

    def menu(self):
        self.next_scene = proceed_menu

    def restart(self):
        if self.count_pacmans == 1:
            self.next_scene = proceed_game_single + str(self.level)
        else:
            self.next_scene = proceed_game_double + str(self.level)

    def write_data(self):
        f = open('high_scores.txt', 'a')
        f2 = open('players.txt', 'r')
        players = f2.read().split(sep=',')
        f2.close()
        for k in range(len(self.pacmans)):
            f.write(players[k] + ' ' + str(self.pacmans[k].score) + '\n')
        f.close()

    def process_events(self, event):

        for i in self.buttons:
            i.check_event(event)
        for i in range(len(self.pacmans)):
            self.pacmans[i].check_events(event, i + 1)
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.pause = not self.pause
            elif event.key == pygame.K_r:
                self.restart()

    def process_logic(self):
        if self.pause:
            return 0
        if self.game_over:
            return 0
        self.collision_hero_and_grains()
        self.collision_hero_and_ghosts()
        self.teleport()
        for i in range(len(self.pacmans)):
            if not self.collision_object_and_walls(self.pacmans[i].potential_action, self.pacmans[i], self.walls):
                self.pacmans[i].current_action = self.pacmans[i].potential_action
            if not self.collision_object_and_walls(self.pacmans[i].current_action, self.pacmans[i], self.walls):
                self.pacmans[i].set_way()
                self.pacmans[i].move()

        for i in self.ghosts:
            new_way = randint(1, 4)
            if not self.collision_object_and_walls(new_way, i, self.walls + self.teleports) \
                    and (new_way + 2) % 2 != (i.current_action + 2) % 2:
                i.current_action = new_way
            if not self.collision_object_and_walls(i.current_action, i, self.walls + self.teleports):
                i.set_way()
                i.move()

    def draw(self, screen):
        screen.fill(DEEP_BLUE)

        try:
            self.level_background = pygame.image.load(os.path.join('image', 'level_maps', 'levels_for_{}'.format(self.count_pacmans), 'level_map_{}.png'.format(self.level)))
            self.level_background = pygame.transform.scale(self.level_background, (self.field_width, self.field_height))
            self.bg_rect = self.level_background.get_rect()
            self.bg_rect.x = INDENT_X
            self.bg_rect.y = INDENT_Y
            screen.blit(self.level_background, self.bg_rect)
        except:
            print('Error: Couldn\'t open {}'.format(os.path.join('image', 'level_maps', 'levels_for_{}'.format(self.count_pacmans), 'level_map_{}.png'.format(self.level))))

        for i in self.floor + self.walls + self.grains:
            i.draw(screen)
        for i in self.pacmans:
            i.draw(screen)
        for i in self.ghosts:
            i.draw(screen)
        for i in self.buttons:
            i.update(screen)
        for i in range(len(self.status_bars)):
            self.status_bars[i].draw(screen,
                                     '{}'.format(constants.players[i])+"'s"+' score: {}, life: {}'.format(self.pacmans[i].score, self.pacmans[i].hp))

        if self.game_over:
            self.message_game_over(screen)

    def load_playing_field(self, score, hp):
        f = open('game_process_for_{}/level{}.txt'.format(self.count_pacmans, self.level), 'r')
        data = list(f.read().split(sep='\n'))
        for i in range(len(data)):
            data[i] = list(data[i])
        f.close()
        field = []
        k = 0
        for x in range(len(data[k])):
            h = []
            for y in range(len(data)):
                h.append(data[y][x])
            k += 1
            field.append(h)
        width = WIDTH_CELL
        height = HEIGHT_CELL

        self.field_width = len(field) * WIDTH_CELL
        self.field_height = len(field[0]) * HEIGHT_CELL

        for i in range(len(field)):
            for k in range(len(field[i])):
                x = INDENT_X + i * width
                y = INDENT_Y + k * height
                if field[i][k] != '1':
                    self.floor.append(Floor(x, y, width, height, 0, constants.BLACK))
                if field[i][k] == '1':
                    self.walls.append(Wall(x, y, width, height, 1, constants.BROWN))
                if field[i][k] == '2':
                    self.grains.append(Grain(x, y, width, height, 2, constants.LIGHT_ORANGE))
                if field[i][k] == '3':
                    self.grains.append(SuperGrain(x, y, width, height, 3, constants.LIGHT_ORANGE))
                if field[i][k] == '5' and self.count_pacmans != len(self.pacmans):
                    self.pacmans.append(Pacman(x + 1, y + 1, width + LESS_OBJECT, height + LESS_OBJECT, 3,
                                        None, score[len(self.pacmans)], hp[len(self.pacmans)]))
                    self.initial_coordinates['pacmans'].append((x + 1, y + 1))
                    self.status_bars.append(StatusBar(INDENT_X, self.walls[0].rect.y - (len(self.status_bars) + 1) * 22))
                if field[i][k] == '6':
                    self.ghosts.append(Ghost(x + 1, y + 1, width + LESS_OBJECT, height + LESS_OBJECT, 3, WHITE))
                    self.initial_coordinates['ghosts'].append((x + 1, y + 1))
                if field[i][k] == '4':
                    self.teleports.append(Teleport(x, y, width, height, 4, constants.BLACK))

    def teleport(self):
        for i in range(len(self.pacmans)):
            if self.teleports[0].rect.collidepoint(self.pacmans[i].rect.centerx, self.pacmans[i].rect.centery):
                self.pacmans[i].rect.x = self.teleports[1].rect.x - WIDTH_CELL
                self.pacmans[i].rect.y = self.teleports[1].rect.y
                self.pacmans[i].score += self.system_score.get_pay_for_teleport()
            if self.teleports[1].rect.collidepoint(self.pacmans[i].rect.centerx, self.pacmans[i].rect.centery):
                self.pacmans[i].rect.x = self.teleports[0].rect.x + WIDTH_CELL
                self.pacmans[i].rect.y = self.teleports[0].rect.y
                self.pacmans[i].score += self.system_score.get_pay_for_teleport()

    def collision_hero_and_grains(self):
        for k in range(len(self.pacmans)):
            for i in range(len(self.grains)):
                if self.grains[i].rect.collidepoint(self.pacmans[k].rect.centerx, self.pacmans[k].rect.centery):
                    self.pacmans[k].eat() # Moved here to make victory sound possible (it has to be played after eat()
                    if self.grains[i].type == 3:
                        for g in range(len(self.ghosts)):
                            if self.ghosts[g].death == False:
                                self.ghosts[g].fear = True
                                self.ghosts[g].new_time_fear()
                        self.pacmans[k].score += self.system_score.get_score_for_super_grain()
                    else:
                        self.pacmans[k].score += self.system_score.get_score_for_grain()
                    self.grains.pop(i)
                    if len(self.grains) == 0:
                        self.level = (self.level + 1) % 10
                        self.pause = True
                        self.walls = []
                        self.floor = []
                        self.grains = []
                        self.ghosts = []
                        self.status_bars = []
                        self.teleports = []
                        self.initial_coordinates = {'pacmans': [], 'ghosts': []}
                        scores = []
                        hp = []
                        for p in range(self.count_pacmans):
                            scores.append(self.pacmans[p].score)
                            hp.append(self.pacmans[p].hp)
                        self.pacmans = []
                        self.load_playing_field(scores, hp)
                        pygame.time.wait(500) # Delay to hear the victory sound and let our player know next lvl begins
                        self.victory_sound.play()
                    break

    def collision_object_and_walls(self, action, moving_object, walls):
        x = moving_object.rect.x + moving_object.directions[action][0] * moving_object.speed
        y = moving_object.rect.y + moving_object.directions[action][1] * moving_object.speed
        width = moving_object.rect.width
        height = moving_object.rect.height
        rect = pygame.Rect(x, y, width, height)
        for i in walls:
            if rect.colliderect(i.rect):
                return True
        else:
            return False

    def collision_hero_and_ghosts(self):
        for g in range(len(self.ghosts)):
            for p in self.pacmans:
                if p.rect.colliderect(self.ghosts[g]):
                    if self.ghosts[g].fear:
                        p.score += self.system_score.get_score_for_ghost()
                        p.eat()
                        self.ghosts[g].fear = False
                        self.ghosts[g].death = True
                        self.ghosts[g].new_time_death()
                        self.ghosts[g].rect.x = self.initial_coordinates['ghosts'][g][0]
                        self.ghosts[g].rect.y = self.initial_coordinates['ghosts'][g][1]
                    elif self.ghosts[g].death == False:
                        p.score += self.system_score.get_pay_for_ghost()
                        self.ghosts[g].kill()
                        if not p.is_alive():
                            self.game_over = True
                            self.write_data()
                        else:
                            p.hp -= 1
                            for k in range(len(self.pacmans)):
                                self.pacmans[k].rect.x = self.initial_coordinates['pacmans'][k][0]
                                self.pacmans[k].rect.y = self.initial_coordinates['pacmans'][k][1]
                            for k in range(len(self.ghosts)):
                                self.ghosts[k].rect.x = self.initial_coordinates['ghosts'][k][0]
                                self.ghosts[k].rect.y = self.initial_coordinates['ghosts'][k][1]
                            self.pause = not self.pause
                        break

    def message_game_over(self, screen):
        Text(110, 150, 'Game over', color=GOLD, size=100).draw(screen)
