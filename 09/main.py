from __future__ import annotations
from typing import Optional

sign = lambda x: 1 if x >= 0 else -1

class Knot:
    x: int
    y: int
    parent: Optional[Knot]
    child: Optional[Knot]

    def __init__(self, parent: Optional[Knot] = None):
        self.parent = parent
        if parent:
            self.parent.child = self
        self.child = None
        self.x = 0
        self.y = 0
    def step(self, dx = 0, dy = 0):

        if self.parent:
            if abs(self.parent.x-self.x) == 2 and abs(self.parent.y-self.y) == 0:
                self.x+=sign(self.parent.x-self.x)
            elif abs(self.parent.y-self.y) == 2 and abs(self.parent.x-self.x) == 0:
                self.y+=sign(self.parent.y-self.y)
            elif abs(self.parent.x-self.x)+abs(self.parent.y-self.y) > 2:
                self.x+=sign(self.parent.x-self.x)
                self.y+=sign(self.parent.y-self.y)
        else:
            self.x += dx
            self.y += dy

        if self.child:
            self.child.step()


PROD = True

directions = {
    "R": (1,0),
    "U": (0,1),
    "D": (0,-1),
    "L": (-1,0)
}

with open("input" if PROD else "sample") as f:
    lines = [g.strip().split(" ") for g in f.readlines()]

instructions = []
[instructions.extend([directions[d]]*int(n)) for d,n in lines]

knots = [Knot()]
for _ in range(9):
    knots.append(Knot(knots[-1]))

positions_knotone = set()
positions_tail = set()


for (dx,dy) in instructions:
    knots[0].step(dx,dy)

    positions_knotone.add((knots[1].x,knots[1].y))
    positions_tail.add((knots[-1].x,knots[-1].y))

print("Part 1:",len(positions_knotone))
print("Part 2:",len(positions_tail))