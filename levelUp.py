import pygame
from sprites import *
from config import *
from enemyAI import *
import json

def check_for_lvlUp(exp, exp_to_lvlup, lvl):
    if exp >= exp_to_lvlup:
        lvlUp(exp, exp_to_lvlup, lvl)

def lvlUp(exp, exp_to_lvlup, lvl):
        with open('./data/mc.json', 'r') as f:
            data = json.load(f)
        data["lvl"] = lvl + 1
        data["exp"] = exp - exp_to_lvlup
        data["defense"] += 1
        data["exp_to_lvlup"] = math.ceil((math.pow(1.2, exp_to_lvlup) + 10) * lvl)
        data["hp"] = data["hp"] + lvl * 3
        data["attack"] = data["attack"] + lvl
        with open('./data/mc.json', 'w') as f:
            json.dump(data, f)