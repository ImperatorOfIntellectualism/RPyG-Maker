import pygame
from sprites import *
from config import *
from enemyAI import *
from levelUp import *
import sys


def Battle_Screen(self, g, player, enemy):
    with open('./data/mc.json', 'r') as f:
        data = json.load(f)
    
    ability_shown = 0
    expire_turn = None
    self.animation_is_finished = 0
    BFPS = 60
    
    attack_animation = [self.attack_spritesheet.get_sprite(0,0, 160, 150),
                            self.attack_spritesheet.get_sprite(161,0, 160, 150),
                            self.attack_spritesheet.get_sprite(322,0, 160, 150),
                            self.attack_spritesheet.get_sprite(483,0, 160, 150),]
    
    defense_animation = [self.defense_spritesheet.get_sprite(0,0, 160, 150),
                            self.defense_spritesheet.get_sprite(161,0, 160, 150),
                            self.defense_spritesheet.get_sprite(322,0, 160, 150),
                            self.defense_spritesheet.get_sprite(483,0, 160, 150),]
    
    defense_break_animation = [self.defense_break_spritesheet.get_sprite(0,0, 160, 150),
                            self.defense_break_spritesheet.get_sprite(161,0, 160, 150),
                            self.defense_break_spritesheet.get_sprite(322,0, 160, 150),
                            self.defense_break_spritesheet.get_sprite(483,0, 160, 150),]

    charge_animation = [self.charge_spritesheet.get_sprite(0,0, 160, 150),
                            self.charge_spritesheet.get_sprite(161,0, 160, 150),
                            self.charge_spritesheet.get_sprite(322,0, 160, 150),
                            self.charge_spritesheet.get_sprite(483,0, 160, 150),]
    
    animation = "None"
    turn = 0

    player_hp = player.hp
    player_lvl = player.lvl
    enemy_lvl = enemy.lvl
    player_true_defense = player.defense
    player_true_attack = player.attack
    enemy_true_defense = enemy.defense
    enemy_hp = enemy.hp

    #BUTTONS
    attack_button = Button(650, 520, 100, 50, WHITE, BLACK, 'Attack', 32)
    ability_button = Button(760, 520, 100, 50, WHITE, BLACK, 'Ability', 32)
    defend_button = Button(870, 520, 100, 50, WHITE, BLACK, 'Defend', 32)
    run_button = Button(980, 520, 100, 50, WHITE, BLACK, 'Run', 32)

    first_ability_button = Button(1130, 220, 179, 57, WHITE, BLACK, player.set_of_abilities[0], 32)

    self.animation_value = 0
    self.enemy_animation_value = 0
    self.defense_animation_value = 0
    self.charge_animation_value = 0
    self.defense_break_animation_value = 0

    self.battle_text = "The Battle has started!"

    def animate():
        frame = 0
        while self.animation_is_finished == 0:
            if frame % BFPS == 0:
                image = attack_animation[self.animation_value]
                self.screen.blit(image, (800, 220))
                self.animation_value += 1
                if self.animation_value == len(attack_animation):
                    self.animation_is_finished = 1
            frame +=1
            pygame.display.update()

        
    def animate_charge(type):
        frame = 0
        while self.animation_is_finished == 0:
            if frame % BFPS == 0:
                if self.charge_animation_value == len(charge_animation) and type == 1:
                    self.animation_is_finished = 1
                    break
                elif self.charge_animation_value == len(charge_animation) * 2 + 1 and type != 1:
                    self.charge_animation_value = 0
                    self.animation_is_finished = 1
                if self.charge_animation_value < 4:
                    image = charge_animation[self.charge_animation_value]
                else:
                    image2 = attack_animation[self.charge_animation_value - 5]
                if type == 1:
                    self.screen.blit(image, (370, 400))
                else: 
                    if self.charge_animation_value < 4:
                        self.screen.blit(image, (800, 220))
                    else:
                        self.screen.blit(image2, (370, 400))
                self.charge_animation_value += 1
            frame +=1
            pygame.display.update()

        
    def animate_enemyTrue():
        frame = 0
        while self.animation_is_finished == 0:
            if frame % BFPS == 0:
                image = attack_animation[self.enemy_animation_value]
                self.screen.blit(image, (370, 400))
                self.enemy_animation_value += 1
                if self.enemy_animation_value == len(attack_animation):
                    self.animation_is_finished = 1
            frame +=1
            pygame.display.update()
        
    def animate_defense_break():
        frame = 0
        while self.animation_is_finished == 0:
            if frame % BFPS == 0:
                image = defense_break_animation[self.defense_break_animation_value]
                self.screen.blit(image, (370, 400))
                self.defense_break_animation_value += 1
                if self.defense_break_animation_value == len(defense_break_animation):
                    self.animation_is_finished = 1
            frame +=1
            pygame.display.update()


    def animate_defense(type):
        frame = 0
        while self.animation_is_finished == 0:
            if frame % BFPS == 0:
                print(self.defense_animation_value)
                image = defense_animation[self.defense_animation_value]
                if type == 1:
                    self.screen.blit(image, (370, 400))
                else:
                    self.screen.blit(image, (800, 220))
                self.defense_animation_value += 1
                if self.defense_animation_value == len(defense_animation):
                    self.animation_is_finished = 1
            frame +=1
            pygame.display.update()
    

    while g.battle == 1:
        if expire_turn != None:
            if expire_turn < turn:
                player.attack = player_true_attack

        battle_text_box = self.font.render(self.battle_text, True, BLACK)
        hpmeter = self.font.render(str(player_hp), True, BLACK)
        hpmeter_rect = hpmeter.get_rect(x = 720, y = 475)
        lvlmeter = self.font.render(str(player_lvl), True, BLACK)
        lvlmeter_rect = lvlmeter.get_rect(x = 910, y = 475)
        elvlmeter = self.font.render(str(enemy_lvl), True, BLACK)
        elvlmeter_rect = elvlmeter.get_rect(x = 610, y = 230)
        enemyhpmeter = self.font.render(str(enemy_hp), True, BLACK)
        enemyhpmeter_rect = hpmeter.get_rect(x = 460, y = 230)
        turn_debug = self.font.render(f"Turn: {'player' if turn % 2 == 0 else 'enemy'}", True, BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() 
            if self.debug == 1:
                if event.type == pygame.MOUSEBUTTONDOWN:
                        print(event.pos)    
            if animation == "None":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and turn % 2 == 0:
                    if attack_button.is_pressed(event.pos,[True]):
                        animation = "player"
                        self.animation_value = 0
                    if defend_button.is_pressed(event.pos,[True]):
                        animation = "defense"
                        self.animation_value = 0
                        self.defense_animation_value = 0
                    if run_button.is_pressed(event.pos,[True]):
                        animation = "enemy"
                        turn+=1
                        self.battle_text = f"The {g.player_name} tried to run away, but FAILED"
                        if random.randint(0,1) == 1:
                            g.battle = 0
                    if ability_button.is_pressed(event.pos,[True]) and ability_shown == 0:
                        ability_shown = 1
                    elif ability_button.is_pressed(event.pos,[True]) and ability_shown == 1:
                        ability_shown = 0
                    if first_ability_button.is_pressed(event.pos,[True]):
                        animation = "charge"
                        self.animation_value = 0

        self.screen.blit(self.battle_background, (300,200))
        self.screen.blit(battle_text_box, (500,635))
        self.screen.blit(hpmeter, hpmeter_rect)
        self.screen.blit(lvlmeter, lvlmeter_rect)
        self.screen.blit(enemyhpmeter, enemyhpmeter_rect)
        self.screen.blit(elvlmeter, elvlmeter_rect)
        self.screen.blit(attack_button.image, attack_button.rect)
        self.screen.blit(ability_button.image, ability_button.rect)
        self.screen.blit(defend_button.image, defend_button.rect)
        self.screen.blit(run_button.image, run_button.rect)
        if ability_shown == 1:
            self.screen.blit(self.ability_menu, (1120,200))
            self.screen.blit(first_ability_button.image, first_ability_button.rect)

        if animation == "player":
            self.battle_text = f"The {g.player_name} has attacked"
            animation_debug = self.font.render(f"Animation playing: Player", True, BLACK)
            animate()
            if player.attack - enemy.defense <= 0:
                enemy_hp -= 1
            else:
                enemy_hp -= player.attack - enemy.defense
            turn += 1
            animation = "enemy"
            self.enemy_animation_value = 0
            enemy.defense = enemy_true_defense
            self.animation_is_finished = 0
        elif animation == "enemy":
            animation_debug = self.font.render(f"Animation playing: Enemy", True, BLACK)
            match enemyAI(self, enemy, player, turn):
                case "Attack":
                    self.battle_text = f"The {self.enemy.name} has attacked"
                    animate_enemyTrue()
                    player_hp -= 4 - player.defense
                    turn += 1
                    animation = "None"
                    self.animation_is_finished = 0
                    self.enemy_animation_value = 0
                case "Defend":
                    self.battle_text = f"The {self.enemy.name} used Defend"
                    animate_defense(2)
                    enemy.defense += 2
                    turn += 1
                    animation = "None"
                    self.animation_is_finished = 0
                    self.defense_animation_value = 0
                case "Armor attack":
                    self.battle_text = f"The {self.enemy.name} used Armor attack"
                    animate_defense_break()
                    if player.defense > 2:
                        player.defense -= 2
                    else: player.defense = 0
                    player_hp -= 3 - player.defense
                    turn += 1
                    self.defense_break_animation_value = 0
                    animation = "None"
                    player.defense = player_true_defense
                    self.animation_is_finished = 0
                case "Mighty attack":
                    self.battle_text = f"The {self.enemy.name} used Mighty attack"
                    animate_charge(2)
                    player_hp -= 6 - player.defense
                    self.charge_animation_value = 0
                    turn += 1
                    animation = "None"
                    self.animation_is_finished = 0

            
            self.animation_value = 0

        elif animation == "defense":
            animation_debug = self.font.render(f"Animation playing: Defense", True, BLACK)
            animate_defense(1)
            player.defense += 1
            turn += 1
            animation = "enemy"
            self.animation_is_finished = 0
            self.defense_animation_value = 0
        elif animation == "charge":
            animation_debug = self.font.render(f"Animation playing: Charge", True, BLACK)
            self.battle_text = f"The {g.player_name} used Charge"
            animate_charge(1)
            player.attack += 3
            expire_turn = turn + 2
            turn += 1
            animation = "enemy"
            self.animation_is_finished = 0
            self.charge_animation_value = 0
            self.animation_value = 0
        else:
            animation_debug = self.font.render(f"Animation playing: None", True, BLACK)
        
        #DEBUG OPTIONS
        if self.debug == 1:
            self.screen.blit(animation_debug, (460, 300))
            self.screen.blit(turn_debug, (460, 350))
        self.clock.tick(10)
        pygame.display.update()
        if enemy_hp <= 0:
            g.battle = 0
            self.current_enemy.kill()
            #LEVEL UP
            data["exp"] += enemy.exp
            with open('./data/mc.json', 'w') as f:
                json.dump(data, f)
            with open('./data/mc.json', 'r') as f:
                data = json.load(f)
            check_for_lvlUp(data["exp"], data["exp_to_lvlup"], data["lvl"])
        else: 
            if player_hp <=0:
                sys.exit()