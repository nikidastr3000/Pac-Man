import pygame
import random
import globals
from constants import *
from utils import Coord

class Cell():
    size = None
    skin = None

    def __init__(self):
        pass

class Point(Cell):
    def __init__(self, pos):
        self.pos = pos
        self.coord = Coord(globals.game.topleft_x + self.pos.x * Cell.size, globals.game.topleft_y + self.pos.y * Cell.size)
        
        circle = pygame.Surface((Cell.size, Cell.size), pygame.SRCALPHA)
        pygame.draw.circle(circle, YELLOW, (Cell.size / 2, Cell.size / 2), Cell.size / 10)
        self.skin = circle
        
    def update(self):       
        globals.game.screen.blit(self.skin, (self.coord.x, self.coord.y))

class Wall(Cell):
    def __init__(self):
        rect = pygame.Surface((Cell.size, Cell.size))
        rect.fill(BLUE)
        self.skin = rect

class Ghost(Cell):
    def __init__(self, skins, pos, speed = None, direction = None):
        self.skins = skins
        self.skin = skins['down']
        self.pos = pos
        self.coord = Coord(globals.game.topleft_x + self.pos.x * Cell.size, globals.game.topleft_y + self.pos.y * Cell.size)
        self.speed = speed
        self.direction = direction
        
    def update(self): 
        self.clear()
        self.move()
        globals.game.screen.blit(self.skin, (self.coord.x, self.coord.y))
        self.check_collision()
        if self.direction != None and self.skin != self.skins[self.direction]:
            self.skin = self.skins[self.direction]

    def move(self):
        # если привидение не находится в центре клетки
        if ((self.coord.x - globals.game.topleft_x) % Cell.size != 0) or ((self.coord.y - globals.game.topleft_y) % Cell.size != 0):
            if self.direction == 'up':
                next_cell_center = globals.game.topleft_y + (self.coord.y - globals.game.topleft_y) // Cell.size * Cell.size
                next_pos = self.coord.y - (self.speed / (globals.game.fps / 70))
                self.coord.y = next_cell_center if next_cell_center > next_pos  else next_pos
                
            elif self.direction == 'left':
                next_cell_center = globals.game.topleft_x + (self.coord.x - globals.game.topleft_x) // Cell.size * Cell.size
                next_pos = self.coord.x - (self.speed / (globals.game.fps / 70))
                self.coord.x = next_cell_center if next_cell_center > next_pos  else next_pos
                
            elif self.direction == 'right':
                next_cell_center = globals.game.topleft_x + ((self.coord.x - globals.game.topleft_x) // Cell.size + 1) * Cell.size
                next_pos = self.coord.x + (self.speed / (globals.game.fps / 70))
                self.coord.x = next_cell_center if next_cell_center < next_pos  else next_pos
                               
            elif self.direction == 'down':
                next_cell_center = globals.game.topleft_y + ((self.coord.y - globals.game.topleft_y) // Cell.size + 1) * Cell.size
                next_pos = self.coord.y + (self.speed / (globals.game.fps / 70))
                self.coord.y = next_cell_center if next_cell_center < next_pos  else next_pos
        # если привидение находится в центре клетки
        else:
            # меняем позицию(координаты) привидения когда оно прибывает в новую клетку
            if self.direction == 'up':
                self.pos.y -= 1
            elif self.direction == 'right':
                self.pos.x += 1
            elif self.direction == 'left':
                self.pos.x -= 1
            elif self.direction == 'down':
                self.pos.y += 1
            
            # узнаем все возможны направления движения, кроме "разворота назад"
            possible_directions = []
            if globals.game.map[self.pos.y - 1][self.pos.x] == '1' and self.direction != 'down':
                possible_directions.append('up')
            if globals.game.map[self.pos.y + 1][self.pos.x] == '1' and self.direction != 'up':
                possible_directions.append('down')
            if globals.game.map[self.pos.y][self.pos.x + 1] == '1' and self.direction != 'left':
                possible_directions.append('right')
            if globals.game.map[self.pos.y][self.pos.x - 1] == '1' and self.direction != 'right':
                possible_directions.append('left')
                
            # выбираем направление для привидения
            if len(possible_directions) == 0:
                if self.direction == 'up':
                    self.direction = 'down'
                elif self.direction == 'down':
                    self.direction = 'up'
                elif self.direction == 'right':
                    self.direction = 'left'
                elif self.direction == 'left':
                    self.direction = 'right'
            elif len(possible_directions) == 1:
                self.direction = possible_directions[0]
            else:
                good_directions = self.wall_hack(possible_directions)
                if len(good_directions):
                    self.direction = random.choice(good_directions)
                else:
                    self.direction = random.choice(possible_directions)
                 
            # приводим привидение в движение по нужному направлению
            if self.direction == 'up':
                self.coord.y -= (self.speed / (globals.game.fps / 70))
            elif self.direction == 'right':
                self.coord.x += (self.speed / (globals.game.fps / 70))
            elif self.direction == 'left':
                self.coord.x -= (self.speed / (globals.game.fps / 70))
            elif self.direction == 'down':
                self.coord.y += (self.speed / (globals.game.fps / 70))           
        
    def wall_hack(self, possible_directions):
        good_directions = []
        for dir in possible_directions:
            if globals.game.situation != 'hunt':
                if dir == 'up' and globals.game.pac_man.pos.y < self.pos.y:
                    good_directions.append(dir)
                elif dir == 'down' and globals.game.pac_man.pos.y > self.pos.y:
                    good_directions.append(dir)
                elif dir == 'right' and globals.game.pac_man.pos.x > self.pos.x:
                    good_directions.append(dir)
                elif dir == 'left' and globals.game.pac_man.pos.x < self.pos.x:
                    good_directions.append(dir)
            else:
                if dir == 'up' and globals.game.pac_man.pos.y > self.pos.y:
                    good_directions.append(dir)
                elif dir == 'down' and globals.game.pac_man.pos.y < self.pos.y:
                    good_directions.append(dir)
                elif dir == 'right' and globals.game.pac_man.pos.x < self.pos.x:
                    good_directions.append(dir)
                elif dir == 'left' and globals.game.pac_man.pos.x > self.pos.x:
                    good_directions.append(dir)
                
        return good_directions

    def check_collision(self):
        pac_man_hitbox = pygame.Rect(globals.game.pac_man.coord.x + Cell.size / 4, globals.game.pac_man.coord.y + Cell.size / 4, Cell.size / 2, Cell.size / 2)
        ghost_hitbox = pygame.Rect(self.coord.x + Cell.size / 4, self.coord.y + Cell.size / 4, Cell.size / 2, Cell.size / 2)
        
        if pac_man_hitbox.colliderect(ghost_hitbox):
            if globals.game.situation != 'hunt':
                pygame.mixer.music.stop()
                globals.game.pac_man.hp -= 1
                globals.game.hp_update()
                globals.game.restart_after_death()
                pygame.time.wait(1000)
            else:
                self.clear()
                self.pos = Coord(17, 7)
                self.coord = Coord(globals.game.topleft_x + self.pos.x * Cell.size - (self.speed / (globals.game.fps / 70)), globals.game.topleft_y + self.pos.y * Cell.size)
                self.direction = 'left'
        
    def clear(self):
        globals.game.screen.blit(Cell.skin, (self.coord.x, self.coord.y))

class PacMan(Cell):
    def __init__(self, speed = None, direction = None, next_dir = None, points = 0):
        self.speed = speed
        self.direction = direction
        self.next_dir = next_dir
        self.hp = globals.game.settings['pac_man_hp']
        self.points = points
        self.pos = Coord(globals.game.settings['pac_man_spawn_x'], globals.game.settings['pac_man_spawn_y'])
        self.coord = Coord(globals.game.topleft_x + self.pos.x * Cell.size, globals.game.topleft_y + self.pos.y * Cell.size)
        
        self.skins = {}
        directions = ('', '_left', '_right', '_up', '_down')
        for d in directions:
            name = "pac_man" + d
            pac_man = pygame.image.load("data/images/" + name + ".png")
            pac_man = pygame.transform.scale(pac_man, (Cell.size, Cell.size))
            self.skins[name] = pac_man
        
        self.skin = self.skins['pac_man']
        
        self.first = 0
        self.second = 0

    def update(self):
        if self.hp <= 0:
            globals.game.restart_lobby()
            return 0
        
        if not len(globals.game.points):
            globals.game.win()
            return 0
        
        self.clear()
        self.move()
        globals.game.screen.blit(self.skin, (self.coord.x, self.coord.y))
        
    def move(self):  
        # если пакман не находится в центре клетки
        if ((self.coord.x - globals.game.topleft_x) % Cell.size != 0) or ((self.coord.y - globals.game.topleft_y) % Cell.size != 0):               
            if self.direction == 'up':
                next_cell_center = globals.game.topleft_y + (self.coord.y - globals.game.topleft_y) // Cell.size * Cell.size
                next_pos = self.coord.y - (self.speed / (globals.game.fps / 70))
                self.coord.y = next_cell_center if next_cell_center > next_pos  else next_pos
                
            elif self.direction == 'left':
                next_cell_center = globals.game.topleft_x + (self.coord.x - globals.game.topleft_x) // Cell.size * Cell.size
                next_pos = self.coord.x - (self.speed / (globals.game.fps / 70))
                self.coord.x = next_cell_center if next_cell_center > next_pos  else next_pos
                
            elif self.direction == 'right':
                next_cell_center = globals.game.topleft_x + ((self.coord.x - globals.game.topleft_x) // Cell.size + 1) * Cell.size
                next_pos = self.coord.x + (self.speed / (globals.game.fps / 70))
                self.coord.x = next_cell_center if next_cell_center < next_pos  else next_pos
                               
            elif self.direction == 'down':
                next_cell_center = globals.game.topleft_y + ((self.coord.y - globals.game.topleft_y) // Cell.size + 1) * Cell.size
                next_pos = self.coord.y + (self.speed / (globals.game.fps / 70))
                self.coord.y = next_cell_center if next_cell_center < next_pos  else next_pos
                
                
            self.animation()
        # если пакман находится в центре клетки
        else:                       
            #меняем позицию(координаты) пакмана когда он прибывает в новую клетку и также останавливаем его если он уперся в стенку
            if self.direction == 'up':
                self.pos.y -= 1
                if globals.game.map[self.pos.y - 1][self.pos.x] == '0':
                    self.direction = None
            elif self.direction == 'right':
                self.pos.x += 1
                if globals.game.map[self.pos.y][self.pos.x + 1] == '0':
                    self.direction = None
            elif self.direction == 'left':
                self.pos.x -= 1
                if globals.game.map[self.pos.y][self.pos.x - 1] == '0':
                    self.direction = None
            elif self.direction == 'down':
                self.pos.y += 1
                if globals.game.map[self.pos.y + 1][self.pos.x] == '0':
                    self.direction = None
                    
            self.eating()
                
            # проверяем куда "хочет" пойти пакман и если он может, то меняем нужные переменные
            if self.next_dir == 'up':
                if globals.game.map[self.pos.y - 1][self.pos.x] == '1':
                    self.next_dir = None
                    self.direction = 'up'
            elif self.next_dir == 'down':
                if globals.game.map[self.pos.y + 1][self.pos.x] == '1':
                    self.next_dir = None
                    self.direction = 'down'
            elif self.next_dir == 'right':
                if globals.game.map[self.pos.y][self.pos.x + 1] == '1':
                    self.next_dir = None
                    self.direction = 'right'
            elif self.next_dir == 'left':
                if globals.game.map[self.pos.y][self.pos.x - 1] == '1':
                    self.next_dir = None
                    self.direction = 'left'
                    
            # приводим пакмана в движение по нужному направлению       
            if self.direction == 'up':
                self.coord.y -= (self.speed / (globals.game.fps / 70))
            elif self.direction == 'right':
                self.coord.x += (self.speed / (globals.game.fps / 70))
            elif self.direction == 'left':
                self.coord.x -= (self.speed / (globals.game.fps / 70))
            elif self.direction == 'down':
                self.coord.y += (self.speed / (globals.game.fps / 70))
               
    def clear(self):
        globals.game.screen.blit(Cell.skin, (self.coord.x, self.coord.y))

    def animation(self):
        self.second = pygame.time.get_ticks()
        if self.second - self.first < 100:
            return 0
        
        if self.skin != self.skins['pac_man']:
            self.skin = self.skins['pac_man']
        else:
            self.skin = self.skins['pac_man_' + self.direction]
        self.first = self.second
        
    def eating(self):
        has_pacman_ate = False
        i = 0
        while i < len(globals.game.points):
            if self.pos == globals.game.points[i].pos:
                globals.game.points.pop(i)
                globals.game.pac_man.points += 10
                globals.game.score_update()
                has_pacman_ate = True
            else:
                i += 1
        
        if has_pacman_ate:
            globals.game.music_play()
        else:
            globals.game.music_stop()

class Cherry(Cell):
    def __init__(self, pos):
        self.pos = pos
        self.coord = Coord(globals.game.topleft_x + self.pos.x * Cell.size, globals.game.topleft_y + self.pos.y * Cell.size)
        
        cherry_skin = pygame.image.load("data/images/cherry.png")
        cherry_skin = pygame.transform.scale(cherry_skin, (Cell.size, Cell.size))
        self.skin = cherry_skin

    def update(self, i):
        self.check_collision(i)
        globals.game.screen.blit(self.skin, (self.coord.x, self.coord.y))

    def check_collision(self, i):
        pac_man_hitbox = pygame.Rect(globals.game.pac_man.coord.x + Cell.size / 4, globals.game.pac_man.coord.y + Cell.size / 4, Cell.size / 2, Cell.size / 2)
        cherry_hitbox = pygame.Rect(self.coord.x + Cell.size / 4, self.coord.y + Cell.size / 4, Cell.size / 2, Cell.size / 2)
        
        if pac_man_hitbox.colliderect(cherry_hitbox):
            globals.game.cherries.pop(i)
            globals.game.situation = 'hunt'
            globals.game.hunt_start = pygame.time.get_ticks()
            wall = Wall()
            globals.game.map[6][15] = '0'
            globals.game.screen.blit(wall.skin, (globals.game.topleft_x + 15 * Cell.size, globals.game.topleft_y + 6 * Cell.size))
