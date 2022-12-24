from typing import Dict, List

DEBUG = False
DEBUG_LEVEL = False

def debug(*args, level=True):
    if DEBUG and (DEBUG_LEVEL == level):
        print(*args)

class Shift:
    def __init__(self, index, value, mod):
        self.index = index
        self.value = value
        self.mod = mod
    
    def refresh_index(self):
        if self.value == 0:
            return self.index
        raw = self.index + self.value
        new = raw % self.mod
        if raw <= 0:
            if raw == 0:
                self.index = self.mod-1
            else:
                self.index = new+raw//self.mod
        elif raw >= self.mod-1:
            if new == self.mod-1:
                self.index = 0
            else:
                self.index = new + raw//self.mod
        else:
            self.index = new
        return self.index

class Permuter:
    new_order: List[Shift]
    original_order: List[Shift] 

    all_important_zero: Shift

    def __init__(self, instructions):
        self.new_order = []
        self.original_order = []
        mod = len(instructions)
        for i,instruction in enumerate(instructions):
            s = Shift(i, instruction, mod)
            if instruction == 0:
                self.all_important_zero = s
            self.new_order.append(s)
            self.original_order.append(s)

    def shuffle(self):
        for instruction in self.original_order:
            old_index = instruction.index
            new_index = instruction.refresh_index()

            for k in range(max(old_index-1, 0), new_index+1):
                self.new_order[k].index -= 1
            for k in range(old_index+1):
                self.new_order[k].index += 1
            self.new_order.pop(old_index)
            self.new_order.insert(new_index, instruction)
    
    def dump(self):
        return [k.value for k in self.new_order]


PROD = False

with open("input" if PROD else "lola.txt") as f:
    _nums = list(map(int, [g.strip() for g in f.readlines()]))

c = Permuter(_nums)

debug(c.dump(), "initial")
c.shuffle()
out = c.dump()
m = len(out)
v = c.all_important_zero.index
coords = [out[(v+(1000*(k+1))) % m] for k in range(3)]
print(coords, sum(coords))