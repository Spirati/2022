PROD = True

from time import perf_counter

t = perf_counter()

with open("input" if PROD else "sample") as f:
    lines = [g.strip() for g in f.readlines()]
width = len(lines[0])
height = len(lines)

order = [0, 1, 2, 3]

def neighbors(x,y):
    global order

    output = (
        [(x+i, y-1) for i in (-1, 0, 1)],
        [(x+i, y+1) for i in (-1, 0, 1)],
        [(x-1, y+i) for i in (-1, 0, 1)],
        [(x+1, y+i) for i in (-1, 0, 1)]
    )
    return [output[i] for i in order]


elves = set()
ground = set()
proposal = {}

for y,line in enumerate(lines):
    for x,cell in enumerate(line):
        if cell == "#":
            elves.add((x,y))
        else:
            ground.add((x,y))

def round():
    global proposal, order

    proposal = {}
    for x,y in elves:
        n,s,w,e = neighbors(x,y)
        # no elves in those positions
        if all(neighbor not in elves for neighbor in [*n,*s,*w,*e]):
            continue

        if all(north_neighbor not in elves for north_neighbor in n):
            if n[1] not in proposal:
                proposal[n[1]] = (x,y)
            else:
                proposal[n[1]] = None
        elif all(south_neighbor not in elves for south_neighbor in s):
            if s[1] not in proposal:
                proposal[s[1]] = (x,y)
            else:
                proposal[s[1]] = None
        elif all(west_neighbor not in elves for west_neighbor in w):
            if w[1] not in proposal:
                proposal[w[1]] = (x,y)
            else:
                proposal[w[1]] = None
        elif all(east_neighbor not in elves for east_neighbor in e):
            if e[1] not in proposal:
                proposal[e[1]] = (x,y)
            else:
                proposal[e[1]] = None

    moved = False
    for destination,value in proposal.items():
        if value is not None:
            moved = True
            elves.remove(value)
            ground.add(value)
            elves.add(destination)
    
    order.append(order.pop(0))
    return moved

# uncomment for part 1
# ================== #
# for _ in range(10):
#     round()

# top_coord = min(elves, key=lambda elf: elf[1])[1]
# bottom_coord = max(elves, key=lambda elf: elf[1])[1]
# left_coord = min(elves, key=lambda elf: elf[0])[0]
# right_coord = max(elves, key=lambda elf: elf[0])[0]

# print((bottom_coord-top_coord+1)*(right_coord-left_coord+1) - len(elves))


# uncomment for part 2
# ================== #
counter = 0
while round():
    counter += 1

print(counter+1)
print(perf_counter() - t)