

import re

PROD = True

with open("input" if PROD else "sample") as f:
    lines = [l.rstrip() for l in f.readlines()]

board = lines[:lines.index("")]
width, height = max(len(line) for line in board), len(board)

tiles = {"#": 1, ".": 0}
grid = {
    (x, y): tiles[cell] for y,line in enumerate(board) for x,cell in enumerate(line) if cell != " "
}
position = (min(cell[0] for cell in grid if cell[1] == 0 and grid[cell] == 0), 0)
direction = (1, 0)
turns = {
    (1, 0): {
        "L": (0, -1),
        "R": (0, 1)
    },
    (0, 1): {
        "L": (1, 0),
        "R": (-1, 0)
    },
    (-1, 0): {
        "L": (0, 1),
        "R": (0, -1)
    },
    (0, -1): {
        "L": (-1, 0),
        "R": (1, 0)
    }
}

instructions = lines[lines.index("")+1:][0]
insmatch = re.compile(R"(\d+)([RL])")
actions = [(int(a), b) for a,b in insmatch.findall(instructions)]

step = lambda x,y,dx,dy: ((x+dx) % width,(y+dy) % height)

for count, turn in actions:
    for _ in range(count):
        new = step(*position, *direction)
        advanced = False
        while new not in grid:
            advanced = True
            new = step(*new, *direction)
        if not advanced:
            new = step(*position, *direction)
        if grid[new] == 0:
            position = new
        else:
            break
    direction = turns[direction][turn]

final_row = position[1]+1
final_col = position[0]+1
final_facing = [(1,0),(0,1),(-1,0),(0,-1)].index(direction)

print(1000*final_row + 4*final_col + final_facing)