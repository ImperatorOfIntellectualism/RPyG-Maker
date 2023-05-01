import math
import random

def generateMap(num_columns, num_lines):
    def create_enemy_coords(num_columns, num_lines):
        enemy_coords = []
        num_enemies = random.randint(1, math.floor(num_columns * num_lines / 30))
        for i in range(num_enemies):
            coord_x = random.randint(1, num_columns - 2)
            coord_y = random.randint(1, num_lines - 2)
            enemy_coords.append([coord_x, coord_y])
        return enemy_coords
    
    def create_blocks(num_columns, num_lines):
        block_coords = []
        num_blocks = random.randint(1, math.floor(num_columns * num_lines / 7))
        for i in range(num_blocks):
            coord_x = random.randint(1, num_columns - 2)
            coord_y = random.randint(1, num_lines - 2)
            block_coords.append([coord_x, coord_y])
        return block_coords
    
    def find_center(num_columns, num_lines):
        col_center = math.floor(num_columns / 2)
        line_center = math.floor(num_lines / 2)
        return col_center, line_center

    line_arr = [["B" if j == 0 or j == num_lines - 1 or i == 0 or i == num_columns - 1 else "." for i in range(num_columns)]
                for j in range(num_lines)]

    block_arr = create_blocks(num_columns, num_lines)
    for block in block_arr:
        x = block[0]
        y = block[1]
        line_arr[y][x] = "B"
    
    enemy_arr = create_enemy_coords(num_columns, num_lines)
    for enemy in enemy_arr:
        x = enemy[0]
        y = enemy[1]
        line_arr[y][x] = "E"

    center_x, center_y = find_center(num_columns, num_lines)
    line_arr[center_y][center_x] = "P"
    line_arr[center_y][center_x - 1] = "S"

    return line_arr