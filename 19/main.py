from typing import Tuple, List

Cost = Tuple[int,int,int,int]

class Blueprint:
    def __init__(self, args: Tuple[Cost,Cost,Cost,Cost]):
        self.robots = [1,0,0,0]
        self.stores = [0,0,0,0]
        self.costs  = [*args]
    




PROD = True

with open("input" if PROD else "sample") as f:
    lines = [g.strip() for g in f.readlines()]