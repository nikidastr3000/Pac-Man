import pygame
import sys
import random
import globals
from constants import *
from utils import Coord, Button
from entities import Cell, Point, Wall, Ghost, PacMan, Cherry

class Game():
    difficulty = 'Easy'
    situation = 'normal'
    run = True
    map = []
    ghosts = []
    points = []
    cherries = []

    def init(self):
        pygame.init()
        
        with open('data/config/Settings.txt', 'r') as f:
            data = list(f)
            
        self.settings = {}
        for i in range(len(data)):
            s = data[i]
            name = ''
            value = ''
            j = 0
            separator = True
            while j < len(s) - 1:
                if s[j] == ' ':
                    j += 3
                    separator = False
                    continue
                
                if separator:
                    name += s[j] 
                else:
                    value += s[j]
                    
                j += 1
                
            if '.' in value:
                value = float(value)
            else:
                value = int(value)
            self.settings[name] = value
                
        
        pygame.mixer.init()
        pygame.mixer.music.load("data/audio/ok-i-pull-up-shorted.mp3")
        pygame.mixer.music.set_volume(self.settings['music_volume'])
        #pygame.mixer.music.load("pacman_chomp.wav")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.pause()
        full_screen = self.settings['full_screen']
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) if full_screen else pygame.display.set_mode((self.settings['screen_width'], self.settings['screen_height']))
        screen = self.screen
        self.screen_width, self.screen_height = screen.get_size()
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()
        self.fps = self.settings['fps']
        
        screen_width, screen_height = self.screen_width, self.screen_height
        
        with open('data/config/Map.txt', 'r') as f:
            data = list(f)
            for i in range(len(data)):
                self.map.append([])
                for j in range(len(data[i]) - 1):
                    self.map[i].append(data[i][j])

        height = len(self.map)
        width = len(self.map[0])
        
        size = min(screen_width // width - 2, screen_height // height - 2)
        black_rect = pygame.Surface((size, size))
        black_rect.fill(BLACK)
        Cell.size = size
        Cell.skin = black_rect
        
        middle_x = screen_width / 2 
        middle_y = screen_height / 2
        self.topleft_x = middle_x - width / 2 * Cell.size
        self.topleft_y = middle_y - height / 2 * Cell.size
        
        self.pac_man = PacMan()
        directions = ('down', 'up', 'right', 'left')
        
        ghost_skins = {}
        for d in directions:
            name = 'yellow_ghost_' + d
            skin = pygame.image.load("data/images/" + name + ".png")
            skin = pygame.transform.scale(skin, (Cell.size, Cell.size))
            ghost_skins[d] = skin
        ghost = Ghost(ghost_skins, Coord(self.settings['ghost_1_spawn_x'], self.settings['ghost_1_spawn_y']))
        self.ghosts.append(ghost)
        
        ghost_skins = {}
        for d in directions:
            name = 'red_ghost_' + d
            skin = pygame.image.load("data/images/" + name + ".png")
            skin = pygame.transform.scale(skin, (Cell.size, Cell.size))
            ghost_skins[d] = skin
        ghost = Ghost(ghost_skins, Coord(self.settings['ghost_2_spawn_x'], self.settings['ghost_2_spawn_y']))
        self.ghosts.append(ghost)
        
        ghost_skins = {}
        for d in directions:
            name = 'blue_ghost_' + d
            skin = pygame.image.load("data/images/" + name + ".png")
            skin = pygame.transform.scale(skin, (Cell.size, Cell.size))
            ghost_skins[d] = skin
        ghost = Ghost(ghost_skins, Coord(self.settings['ghost_3_spawn_x'], self.settings['ghost_3_spawn_y']))
        self.ghosts.append(ghost)
        
        self.cherries.append(Cherry(Coord(self.settings['cherry_1_spawn_x'], self.settings['cherry_1_spawn_y'])))
        self.cherries.append(Cherry(Coord(self.settings['cherry_2_spawn_x'], self.settings['cherry_2_spawn_y'])))

    def initial_lobby(self):
        self.init()
        
        self.wait_for_start = True
        
        width, height = Cell.size * 7, Cell.size * 3
        start_button = Button(
            x = (self.screen_width - width) / 2, y = (self.screen_height - height) / 2 - Cell.size * 1.7, 
            width = width, height = height, 
            text = 'Start', 
            font = pygame.font.Font(None, Cell.size * 2), 
            color = BLUE, hover_color = GREEN, text_color = WHITE, 
            action = self.start_the_game)
        self.difficulty_button = Button(
            x = (self.screen_width - width) / 2, y = (self.screen_height - height) / 2 + Cell.size * 1.7,
            width = width, height = height, 
            text = self.difficulty, 
            font = pygame.font.Font(None, Cell.size * 2), 
            color = BLUE, hover_color = ORANGE, text_color = WHITE, 
            action = self.change_difficulty)
        self.change_difficulty()  
        width, height = Cell.size * 3.5, Cell.size * 1.5
        self.exit_button = Button(
            x = self.screen_width - width - 10, y = 10, 
            width = width, height = height, 
            text = 'Exit', 
            font = pygame.font.Font(None, Cell.size), 
            color = BLUE, hover_color = RED, text_color = WHITE, 
            action = self.stop)
        
        while self.wait_for_start:
            self.screen.fill(BLACK)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                start_button.handle_event(event)
                self.difficulty_button.handle_event(event)
                self.exit_button.handle_event(event)
                
            start_button.draw(self.screen)
            self.difficulty_button.draw(self.screen)
            self.exit_button.draw(self.screen)
            
            
            pygame.display.flip()
            self.clock.tick(60)

        self.screen.fill(BLACK)
        width, height = Cell.size, Cell.size
        self.stop_button = Button(
            x = self.screen_width - width - 10, y = 10, 
            width = width, height = height, 
            text = 'X', 
            font = pygame.font.Font(None, Cell.size + 10), 
            color = BLUE, hover_color = RED, text_color = WHITE, 
            action = self.restart_lobby)

    def change_difficulty(self):
        if self.difficulty == 'Easy':
            self.difficulty = 'Normal'
            ghost_speed_factor = self.settings['ghost_speed_normal']
            pac_man_speed_factor = self.settings['pac_man_speed_normal']
        elif self.difficulty == 'Normal':
            self.difficulty = 'Hard'
            ghost_speed_factor = self.settings['ghost_speed_hard']
            pac_man_speed_factor = self.settings['pac_man_speed_hard']
        elif self.difficulty == 'Hard':
            self.difficulty = 'Easy'
            ghost_speed_factor = self.settings['ghost_speed_easy']
            pac_man_speed_factor = self.settings['pac_man_speed_easy']
            
        for i in range(len(self.ghosts)):
            self.ghosts[i].speed = Cell.size * ghost_speed_factor
        self.pac_man.speed = Cell.size * pac_man_speed_factor
        self.difficulty_button.text = self.difficulty           

    def start_the_game(self):
        self.wait_for_start = False

    def start(self):
        self.initial_lobby()
        
        self.draw_the_map()

        self.main_loop()                

    def main_loop(self):
        while self.run:
            self.handle_event()
            
            self.stop_button.draw(self.screen)
            
            for point in self.points:
                point.update()
                
            for i, cherry in enumerate(self.cherries):
                cherry.update(i)
            
            self.music_update()
                        
            self.pac_man.update()
            
            for ghost in self.ghosts:
                ghost.update()
            
            self.situation_update()
            
            pygame.display.flip()
            self.clock.tick(self.fps)

    def situation_update(self):
        if self.situation == 'hunt':
            time = pygame.time.get_ticks() - self.hunt_start
            if time > self.settings['hunt_time']:
                self.situation = 'normal'
                
                width, height = pygame.font.Font(None, 36).render('00:00', True, WHITE).get_size()
                gap = 5
                rect = pygame.Surface((width + gap * 2, height + gap * 2))
                rect.fill(BLACK)
                self.screen.blit(rect, ((self.screen_width - width) / 2 - gap, self.topleft_y - Cell.size - gap))
                
                for ghost in self.ghosts:
                    ghost.is_in_cage = False  
                    
                self.map[6][15] = '1'
                self.screen.blit(Cell.skin, (self.topleft_x + 15 * Cell.size, self.topleft_y + 6 * Cell.size))
                return 0
            
            time_left = self.settings['hunt_time'] - time
            sec_left = time_left // 1000
            sec_left = str(sec_left)
            if len(sec_left) < 2:
                sec_left = '0' + sec_left
            
            millisec_left = time_left % 1000
            if millisec_left >= 100:
                millisec_left = str(millisec_left // 10)
            elif millisec_left >= 10:
                millisec_left = '0' + str(millisec_left // 10)
            else:
                millisec_left = '00'
                
            font = pygame.font.Font(None, 36)
            score_surface = font.render(sec_left + ':' + millisec_left, True, WHITE)
            
            width, height = score_surface.get_size()
            gap = 5
            rect = pygame.Surface((width + gap * 2, height + gap * 2))
            rect.fill(BLACK)
            self.screen.blit(rect, ((self.screen_width - width) / 2 - gap, self.topleft_y - Cell.size - gap))
            
            self.screen.blit(score_surface, ((self.screen_width - width) / 2, self.topleft_y - Cell.size)) 
            
            wall = Wall()
            self.screen.blit(wall.skin, (self.topleft_x + 15 * Cell.size, self.topleft_y + 6 * Cell.size))        

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP):  
                    self.pac_man.next_dir = 'up'
                elif event.key in (pygame.K_a, pygame.K_LEFT):   
                    self.pac_man.next_dir = 'left' 
                elif event.key in (pygame.K_d, pygame.K_RIGHT):   
                    self.pac_man.next_dir = 'right'   
                elif event.key in (pygame.K_s, pygame.K_DOWN):   
                    self.pac_man.next_dir = 'down'
                        
            self.stop_button.handle_event(event)

    def draw_the_map(self):
        screen = self.screen
        
        wall = Wall()
        x, y = self.topleft_x, self.topleft_y
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                is_there_a_cherry = False
                for k, cherry in enumerate(self.cherries):
                    if Coord(j, i) == cherry.pos:
                        cherry.update(k)
                        is_there_a_cherry = True
                if is_there_a_cherry:
                    x += Cell.size
                    continue
                
                if self.map[i][j] == '0':
                    screen.blit(wall.skin, (x, y))
                    pygame.display.flip()
                    pygame.time.delay(10)
                elif Coord(j, i) != self.pac_man.pos:
                    point = Point(Coord(j, i))
                    self.points.append(point)
                    self.screen.blit(point.skin, (point.coord.x, point.coord.y))
                
                x += Cell.size
                
            x = self.topleft_x
            y += Cell.size
        
        self.score_update()
        self.hp_update()

    def restart_after_death(self):
        self.pac_man.clear()
        self.pac_man.pos = Coord(15, 13)
        self.pac_man.coord = Coord(self.topleft_x + self.pac_man.pos.x * Cell.size, self.topleft_y + self.pac_man.pos.y * Cell.size)
        self.pac_man.direction = None
        self.pac_man.next_dir = None
        self.pac_man.skin = self.pac_man.skins['pac_man']
        
        poses = (Coord(15, 5), Coord(1, 1), Coord(29, 1))
        for i in range(len(self.ghosts)):
            pos = poses[i]
            coord = Coord(self.topleft_x + pos.x * Cell.size, self.topleft_y + pos.y * Cell.size)
            
            self.ghosts[i].clear()
            self.ghosts[i].pos = pos
            self.ghosts[i].coord = coord
            self.ghosts[i].direction = None 
            
        pygame.mixer.music.stop()
        pygame.mixer.music.play(-1)
        pygame.mixer.music.pause() 

    def score_update(self):
        font = pygame.font.Font(None, 36)
        score_surface = font.render(str(self.pac_man.points), True, WHITE)
        
        width, height = score_surface.get_size()
        gap = 5
        rect = pygame.Surface((width + gap * 2, height + gap * 2))
        rect.fill(BLACK)
        self.screen.blit(rect, (self.topleft_x - gap, self.topleft_y - 30 - gap))
        
        self.screen.blit(score_surface, (self.topleft_x, self.topleft_y - 30))

    def hp_update(self):
        gap = 5
        rect = pygame.Surface(((self.pac_man.hp + 1) * (gap + Cell.size) + gap, Cell.size + gap * 2))
        rect.fill(BLACK)
        self.screen.blit(rect, (self.topleft_x - gap, self.topleft_y + len(self.map) * Cell.size))
        
        skin = self.pac_man.skins['pac_man_left']
        for i in range(self.pac_man.hp):
            self.screen.blit(skin, (self.topleft_x + i * (gap + Cell.size), self.topleft_y + len(self.map) * Cell.size + gap))

    def music_update(self):
        if pygame.mixer.music.get_pos() == -1:
            pygame.mixer.music.play(-1)

    def music_play(self):
        pygame.mixer.music.unpause()
            
    def music_stop(self):
        pygame.mixer.music.pause()

    def restart_lobby(self):
        self.music_stop()
        self.wait_for_restart = True
        
        width, height = Cell.size * 7, Cell.size * 3
        restart_button = Button(
            x = (self.screen_width - width) / 2, y = (self.screen_height - height) / 2 - Cell.size * 1.7, 
            width = width, height = height, 
            text = 'Restart', 
            font = pygame.font.Font(None, Cell.size * 2), 
            color = BLUE, hover_color = GREEN, text_color = WHITE, 
            action = self.restart_the_game)
        
        while self.wait_for_restart:
            self.screen.fill(BLACK)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                restart_button.handle_event(event)
                self.difficulty_button.handle_event(event)
                self.exit_button.handle_event(event)
                
            restart_button.draw(self.screen)
            self.difficulty_button.draw(self.screen)
            self.exit_button.draw(self.screen)  
            
            pygame.display.flip()
            self.clock.tick(60)
            
        self.screen.fill(BLACK)
        self.restart_after_loss()
        
    def restart_the_game(self):
        self.wait_for_restart = False
        
    def restart_after_loss(self):
        self.situation = 'normal'
        self.points = []
        self.pac_man.hp = 3
        self.pac_man.points = 0
        self.pac_man.pos = Coord(15, 13)
        self.cherries.append(Cherry(Coord(self.settings['cherry_1_spawn_x'], self.settings['cherry_1_spawn_y'])))
        self.cherries.append(Cherry(Coord(self.settings['cherry_2_spawn_x'], self.settings['cherry_2_spawn_y'])))
        
        self.draw_the_map()
            
        self.restart_after_death()
        
    def win(self):
        self.screen.fill(BLACK)
        font = pygame.font.Font(None, 100)
        congr_surface = font.render('!CONGRATULATIONS!', True, WHITE)
        width, height = congr_surface.get_size()
        x = (self.screen_width - width) / 2
        y = (self.screen_height - height) / 2
        congr_rect = congr_surface.get_rect()
        congr_rect.x = x
        congr_rect.y = y
        
        self.screen.blit(congr_surface, (x, y))
        pygame.display.flip()
        
        start = pygame.time.get_ticks()
        win_animation = True
        while win_animation:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            w_surface = font.render('W', True, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            w_rect = w_surface.get_rect()
            x = random.randint(-50, self.screen_width)
            y = random.randint(-50, self.screen_height)
            w_rect.x = x
            w_rect.y = y
            if w_rect.colliderect(congr_rect):
                continue
            self.screen.blit(w_surface, (x, y))
            now = pygame.time.get_ticks()
            if now - start > 10000:
                win_animation = False
            
            pygame.display.flip()
            self.clock.tick(40)
        
        
        self.restart_lobby()

    def stop(self):
        self.run = False
        pygame.quit()
        sys.exit()
               

if __name__ == '__main__':
    globals.game = Game()
    globals.game.start()
