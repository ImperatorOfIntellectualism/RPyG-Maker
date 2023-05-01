import pygame
from sprites import *
from config import *
from battle import *
import sys
from worldGen import *
import random
import math

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('arial.ttf', 32)
        self.running = True
        self.current_screen = "menu"
        self.player = None
        self.enemy = None
        self.current_enemy = None
        self.list = []
        self.frame = 0
        self.battle = 0
        self.debug = 0
        self.play_music = 1
        self.max_level = 3

        pygame.mixer.music.load('./src/ambience_1.wav')

        self.character_spritesheet = Spritesheet('./img/player.png')
        self.attack_spritesheet = Spritesheet('./img/attack_animation.png')
        self.defense_spritesheet = Spritesheet('./img/defense_animation.png')
        self.defense_break_spritesheet = Spritesheet('./img/defense_break_animation.png')
        self.charge_spritesheet = Spritesheet('./img/charge_animation.png')
        self.enemy_spritesheet = Spritesheet('./img/enemy.png')
        self.terrain_spritesheet = Spritesheet('./img/terrain.png')
        self.intro_background = pygame.image.load('./img/background.png')
        self.battle_background = pygame.image.load('./img/Battle_screen.png')
        self.ability_menu = pygame.image.load('./img/Ability_menu.png')
        self.credits = pygame.image.load('./img/credits.png')
        self.save_sprite = pygame.image.load('./img/save.png')

    def createTilemap(self):
        a = math.floor(random.randrange(20, 64, 2))
        tilemap = ["".join(item) for item in generateMap(a,math.floor(a/2))]
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "S":
                    Save(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)
                if column == "E":
                    self.enemies.add(Enemy(self, j, i, 1, random.randint(1, self.max_level)))


    def new(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.saves = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.createTilemap()
        self.centered = 0


    def events(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def draw(self):
        self.all_sprites.draw(self.screen)
        if self.centered == 0:
            for sprite in self.all_sprites:
                sprite.rect.x += WIN_WIDTH / 2 - self.player.x
                sprite.rect.y += WIN_HEIGHT / 2 - self.player.y
            self.centered = 1
        self.clock.tick(FPS)
        pygame.display.update()

    def update(self):
        self.all_sprites.update()
        if len(self.enemies) == 0:
            self.max_level += 1
            self.new()
 
    def main(self):
        with open('./data/save.json', 'r') as f:
                sData = json.load(f)
        with open('./data/mc.json', 'w') as f:
            json.dump(sData['mc'], f)
        invincibility_frame = 0
        while self.playing:
            keys = pygame.key.get_pressed()
            self.frame += 1
            if self.debug == 1:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        print(event.pos)
                    if event.type == pygame.QUIT:
                        sys.exit()  
                    #DEBUGGING RESET
                    if keys[pygame.K_t] and self.debug:
                        self.new()
            if g.current_screen == "menu":
                g.intro_screen()
            self.screen.fill(BLACK)
            self.events()
            self.draw()
            self.update()
            if invincibility_frame > 0: 
                invincibility_frame -= 1
            if g.battle == 1 and invincibility_frame == 0:
                invincibility_frame = 120
                pygame.mixer.music.stop()
                pygame.mixer.music.load('./src/battle_1.wav')
                pygame.mixer.music.play(-1)
                with open('./data/mc.json', 'r') as f:
                    data = json.load(f)
                self.player.lvl = data['lvl']
                self.player.hp = data['hp']
                self.player.defense = data['defense']
                self.player.attack = data['attack']
                self.player.exp = data['exp']
                self.player.exp_to_lvlup = data['exp_to_lvlup']
                self.player.set_of_abilities = data['set_of_abilities']
                Battle_Screen(self, g, self.player, self.current_enemy)
                pygame.mixer.music.stop()
                pygame.mixer.music.load('./src/ambience_1.wav')
                pygame.mixer.music.play(-1)
            pygame.display.update()
            g.battle = 0
        self.running = False
            
    def game_over(self):
        pass

    def intro_screen(self):
        title = self.font.render('Awesome Game', True, BLACK)
        title_rect = title.get_rect(x = 10, y = 10)


        credits_show = 0

        play_button = Button(10, 50, 100, 50, WHITE, BLACK, 'Play', 32)
        reset_button = Button(10, 150, 100, 50, WHITE, BLACK, 'Reset', 32)
        credits_button = Button(10, 250, 100, 50, WHITE, BLACK, 'Credits', 32)
        while g.current_screen == "menu" and self.running == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()  

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if play_button.is_pressed(mouse_pos, mouse_pressed):
                self.current_screen = "game"
            if reset_button.is_pressed(mouse_pos, mouse_pressed):
                with open('./data/save.json', 'r') as f:
                    data = json.load(f)
                    data["mc"]['lvl'] = 1
                    data["mc"]['hp'] = 15
                    data["mc"]['attack'] = 1
                    data["mc"]['defense'] = 3
                    data["mc"]['exp'] = 0
                    data["mc"]['exp_to_lvlup'] = 10
                    data["mc"]['set_of_abilities'] = ['Charge']
                with open('./data/save.json', 'w') as f:
                    json.dump(data, f)
            if credits_button.is_pressed(mouse_pos, mouse_pressed):
                if credits_show == 0:
                    credits_show = 1
                else: credits_show = 0
            self.screen.fill(BLACK)
            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(reset_button.image, reset_button.rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(credits_button.image, credits_button.rect)
            if credits_show:
                self.screen.blit(self.credits, (700, 200))
            self.clock.tick(FPS)
            with open('./data/save.json', 'r') as f:
                sData = json.load(f)
            with open('./data/mc.json', 'w') as f:
                json.dump(sData['mc'], f)
            pygame.display.update()
        

g = Game()
g.new()

while g.running:
    if (g.play_music):
        pygame.mixer.music.play(-1)
    g.main()
    g.game_over()

pygame.quit()
sys.exit()        