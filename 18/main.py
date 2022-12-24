from typing import Tuple
from tqdm import tqdm

def adjoining(x,y,z):
    return (
        (x+1,y,z),
        (x-1,y,z),
        (x,y+1,z),
        (x,y-1,z),
        (x,y,z+1),
        (x,y,z-1)
    )

cache = dict()

def exposed_sides(world, coords):
    if coords in cache:
        neighbors = cache[coords]
    else:
        neighbors = adjoining(*coords)
        cache[coords] = neighbors
    return 6-sum(1 for neighbor in neighbors if neighbor in world)

def filter_to_axis(world, coords, axis):
    other_ax = {0: [1,2], 1: [0,2], 2: [0,1]}[axis]
    o1,o2 = other_ax

    return [c for c in world if (c[o1], c[o2]) == (coords[o1], coords[o2])]

def all_hidden(world, coords):
    for axis in (0,1,2):
        if sum(1 for coord in filter_to_axis(world, coords, axis) if coord[axis] > coords[axis])*sum(1 for coord in filter_to_axis(world, coords, axis) if coord[axis] < coords[axis]) == 0:
            return False
    return True


world = set()


PROD = True

with open("input" if PROD else "sample") as f:
    lines = [g.strip() for g in f.readlines()]

[world.add(
    tuple(map(int,line.split(",")))
) for line in lines]

part1 = sum(exposed_sides(world, k) for k in world)

print("Part 1:", part1)

maxX = max(coords[0] for coords in world)
minX = min(coords[0] for coords in world)
maxY = max(coords[1] for coords in world)
minY = min(coords[1] for coords in world)
maxZ = max(coords[2] for coords in world)
minZ = min(coords[2] for coords in world)

pockets = 0
ps = set()

for x in tqdm(range(minX, maxX)):
    for y in range(minY, maxY):
        for z in range(minZ, maxZ):
            if all_hidden(world, (x,y,z)) and (x,y,z) not in world:
                pockets += 1
                ps.add((x,y,z))
print(pockets, ps)

print(part1-6*pockets)