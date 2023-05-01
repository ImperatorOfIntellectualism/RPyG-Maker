from sprites import *
from config import *

def enemyAI(self, enemy, player, turn):
    if enemy.id == 1:
        enemy.cooldown[0] -= 1
        enemy.cooldown[1] -= 1
        if player.defense >= 2 and enemy.cooldown[0] <= 0:
            enemy.cooldown[0] = 3
            return "Armor attack"
        elif player.attack > 4 and enemy.cooldown[1] <= 0:
            enemy.cooldown[1] = 3
            return "Defend"
        elif turn % 3 == 0 and turn != 0:
            return "Mighty attack"
        else: 
            return "Attack"