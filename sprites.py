import pygame
from config import *
import math
import random
import json
import sys

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.screen = pygame.display.get_surface()
        #DATA
        f = open('./data/mc.json')
        data = json.load(f)
        f.close()

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.font = pygame.font.Font('arial.ttf', 32)
        self.game.player_name = data['characterName']
        self.lvl = data['lvl']
        self.hp = data['hp']
        self.defense = data['defense']
        self.attack = data['attack']
        self.exp = data['exp']
        self.exp_to_lvlup = data['exp_to_lvlup']

        self.set_of_abilities = data['set_of_abilities']

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE - 2
        self.height = TILESIZE - 2

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.game.player = self

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                 sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                 sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
           for sprite in self.game.all_sprites:
                 sprite.rect.y += PLAYER_SPEED
           self.y_change -= PLAYER_SPEED
           self.facing = 'up'
        if keys[pygame.K_DOWN]:
           for sprite in self.game.all_sprites:
                 sprite.rect.y -= PLAYER_SPEED
           self.y_change += PLAYER_SPEED
           self.facing = 'down'

    def animate(self):
        down_animation = [self.game.character_spritesheet.get_sprite(0,0,self.width, self.height),
                          self.game.character_spritesheet.get_sprite(66,0,self.width, self.height),
                          self.game.character_spritesheet.get_sprite(132,0,self.width, self.height),]
        up_animation = [self.game.character_spritesheet.get_sprite(0,33,self.width, self.height),
                        self.game.character_spritesheet.get_sprite(66,33,self.width, self.height),
                        self.game.character_spritesheet.get_sprite(132,33,self.width, self.height),]
        left_animation = [self.game.character_spritesheet.get_sprite(33,33,self.width, self.height),
                          self.game.character_spritesheet.get_sprite(99,33,self.width, self.height),
                          self.game.character_spritesheet.get_sprite(165,33,self.width, self.height),]
        right_animation = [self.game.character_spritesheet.get_sprite(33,0,self.width, self.height),
                          self.game.character_spritesheet.get_sprite(99,0,self.width, self.height),
                          self.game.character_spritesheet.get_sprite(165,0,self.width, self.height),]
        
        if self.facing == "down":
            if self.y_change == 0:
                self.image = down_animation[0]
            else:
                self.image = down_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "up":
            if self.y_change == 0:
                self.image = up_animation[0]
            else:
                self.image = up_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "left":
            if self.x_change == 0:
                self.image = left_animation[0]
            else:
                self.image = left_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "right":
            if self.x_change == 0:
                self.image = right_animation[0]
            else:
                self.image = right_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

    def update(self):
        self.movement()
        self.animate()
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        self.collide_enemy()
        self.collide_save()
        self.x_change = 0
        self.y_change = 0

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED

    def collide_enemy(self):
        
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.game.battle = 1
            self.game.current_enemy = hits[0]

    def collide_save(self):
        with open('./data/mc.json', 'r') as f:
            newData = json.load(f)
        with open('./data/save.json', 'r') as f:
            currentData = json.load(f)
        title = self.font.render('Press Spacebar to save', True, WHITE)
        title_rect = title.get_rect(x = 70, y = 10)
        hits = pygame.sprite.spritecollide(self, self.game.saves, False)
        if hits:
            self.screen.blit(title, title_rect)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                currentData['mc'] = newData
                with open('./data/save.json', 'w') as f:
                    json.dump(currentData, f)
                

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y, id, lvl):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.id = id
        self.name = "Monster"
        self.hp = lvl * 2 + 2
        self.lvl = lvl
        self.defense = self.lvl
        self.attack = self.lvl * 2
        self.cooldown = [1,1]
        self.exp = math.ceil(math.pow(1.2, lvl*4) + 8)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.enemy_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.game.enemy = self

    def movement(self):
        movement = random.randint(0, 250)
        if movement == 0: 
            self.x_change -= ENEMY_SPEED
            self.facing = 'left'
        if movement == 1:
            self.x_change += ENEMY_SPEED
            self.facing = 'right'
        if movement == 2:
           self.y_change -= ENEMY_SPEED
           self.facing = 'up'
        if movement == 3:
           self.y_change += ENEMY_SPEED
           self.facing = 'down'

    def animate(self):
        down_animation = [self.game.enemy_spritesheet.get_sprite(0,0,self.width, self.height),
                          self.game.enemy_spritesheet.get_sprite(66,0,self.width, self.height),
                          self.game.enemy_spritesheet.get_sprite(132,0,self.width, self.height),]
        up_animation = [self.game.enemy_spritesheet.get_sprite(0,33,self.width, self.height),
                        self.game.enemy_spritesheet.get_sprite(66,33,self.width, self.height),
                        self.game.enemy_spritesheet.get_sprite(132,33,self.width, self.height),]
        left_animation = [self.game.enemy_spritesheet.get_sprite(33,33,self.width, self.height),
                          self.game.enemy_spritesheet.get_sprite(99,33,self.width, self.height),
                          self.game.enemy_spritesheet.get_sprite(165,33,self.width, self.height),]
        right_animation = [self.game.enemy_spritesheet.get_sprite(33,0,self.width, self.height),
                          self.game.enemy_spritesheet.get_sprite(99,0,self.width, self.height),
                          self.game.enemy_spritesheet.get_sprite(165,0,self.width, self.height),]
        
        if self.facing == "down":
            if self.y_change == 0:
                self.image = down_animation[0]
            else:
                self.image = down_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "up":
            if self.y_change == 0:
                self.image = up_animation[0]
            else:
                self.image = up_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "left":
            if self.x_change == 0:
                self.image = left_animation[0]
            else:
                self.image = left_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "right":
            if self.x_change == 0:
                self.image = right_animation[0]
            else:
                self.image = right_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1


    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False) + pygame.sprite.spritecollide(self, self.game.saves, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False) + pygame.sprite.spritecollide(self, self.game.saves, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def update(self):
        self.movement()
        self.animate()
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        self.x_change = 0
        self.y_change = 0

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
         self.game = game
         self._layer = BLOCK_LAYER
         self.groups = self.game.all_sprites, self.game.blocks
         pygame.sprite.Sprite.__init__(self, self.groups)

         self.x = x * TILESIZE
         self.y = y * TILESIZE
         self.width = TILESIZE
         self.height = TILESIZE

         self.image = self.game.terrain_spritesheet.get_sprite(0, 0, self.width, self.height)

         self.rect = self.image.get_rect()
         self.rect.x = self.x
         self.rect.y = self.y

class Save(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
         self.game = game
         self._layer = BLOCK_LAYER
         self.groups = self.game.all_sprites, self.game.saves
         pygame.sprite.Sprite.__init__(self, self.groups)

         self.x = x * TILESIZE
         self.y = y * TILESIZE
         self.width = TILESIZE
         self.height = TILESIZE

         self.image = self.game.save_sprite

         self.rect = self.image.get_rect()
         self.rect.x = self.x
         self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
         self.game = game
         self._layer = GROUND_LAYER
         self.groups = self.game.all_sprites
         pygame.sprite.Sprite.__init__(self, self.groups)

         self.x = x * TILESIZE
         self.y = y * TILESIZE
         self.width = TILESIZE
         self.height = TILESIZE

         self.image = self.game.terrain_spritesheet.get_sprite(32, 0, self.width, self.height)

         self.rect = self.image.get_rect()
         self.rect.x = self.x
         self.rect.y = self.y         

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('arial.ttf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)
        
    def is_pressed(self, pos, mouse_pressed):
        if self.rect.collidepoint(pos) and mouse_pressed[0]:
            return True
        return False
