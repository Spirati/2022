from __future__ import annotations
from typing import Optional, Tuple

from math import inf
from queue import PriorityQueue

PROD = True

def letter_to_height(letter):
    if letter == "S":
        return 0
    if letter == "E":
        return 25
    return ord(letter)-ord("a")

with open("input" if PROD else "sample") as f:
    lines = [g.strip() for g in f.readlines()]
    grid = {}
    start = None
    end = None

    width = len(lines[0])
    height = len(lines)


    for y in range(height):
        for x in range(width):
            if lines[y][x] == "S":
                start = (x,y)
            if lines[y][x] == "E":
                end = (x,y)
            grid[x,y] = letter_to_height(lines[y][x])

print(start, end)

def neighbors(x,y):
    return [
        (x+i, y+j) for i in (-1,0,1) for j in (-1,0,1) if (x+i,y+j) != (x,y) and x+i < width and x+i >= 0 and y+j < height and y+j >= 0 and (i,j) != (1,1) and (i,j) != (-1,-1) and (i,j) != (1,-1) and (i,j) != (-1,1)
    ]

heuristic = lambda x,y: (x - end[0])**2 + (y-end[1])**2

def unwind(retrace, current):
    out = []
    while current in retrace:
        current = retrace[current]
        out.insert(0, current)
    return out

def bfs():
    root = start

    retrace = {}

    nodes = PriorityQueue()
    nodes.put(root)
    explored = set([root])

    while not nodes.empty():
        current = nodes.get()
        if current == end:
            return unwind(retrace, current)
        for neighbor in neighbors(*current):
            if grid[neighbor]-grid[current] > 1:
                continue
            if neighbor not in explored:
                explored.add(neighbor)
                retrace[neighbor] = current
                nodes.put(neighbor)

path = bfs()

print(path,len(path))