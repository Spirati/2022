PROD = True
from functools import reduce
from time import perf_counter

with open("input" if PROD else "sample") as f:
    lines = [[int(c) for c in g.strip()] for g in f.readlines()]

candidates = set()

def traverse(vert: bool):
    for y in range(1,len(lines)-1):
        for x in range(1,len(lines)-1):
            if vert:
                if all(lines[y][x] > lines[y+i][x] for i in range(1,len(lines)-y)):
                    candidates.add((x,y))
                    # print(x,y,"is visible from the bottom")
                if all(lines[y][x] > lines[y-i][x] for i in range(1, y+1)):
                    candidates.add((x,y))
                    # print(x,y,"is visible from the top")
            else:
                if all(lines[y][x] > lines[y][x+i] for i in range(1,len(lines)-x)):
                    candidates.add((x,y))
                    # print(x,y,"is visible from the right")
                if all(lines[y][x] > lines[y][x-i] for i in range(1, x+1)):
                    candidates.add((x,y))
                    # print(x,y,"is visible from the left")

traverse(True)
traverse(False)

def get_until(condition, iterable):
    index = 0
    while index < len(iterable):
        if condition(iterable[index]):
            index += 1
            break
        index += 1
    return iterable[:index]

print("Part 1",len(candidates)+4*len(lines)-4)

def viewing_distance(candidate):
    x,y = candidate
    return reduce(lambda a,b: a*b, (len(get_until(
            lambda entry: lines[y][x] <= entry, s
        )) for s in [
            lines[y][x+1:], # looking right
            lines[y][:x][::-1], # looking left
            [lines[k][x] for k in range(y+1, len(lines))], # looking down
            [lines[k][x] for k in range(0, y)][::-1] # looking up
        ]), 1)

print("Part 2", max(viewing_distance(candidate) for candidate in candidates))