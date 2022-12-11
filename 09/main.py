PROD = False

dirs = {
    "R":(1,0),
    "U":(0,-1),
    "D":(0,1),
    "L":(-1,0)
}

tupsum = lambda *tuples: tuple(sum(t[c] for t in tuples) for c in range(len(tuples[0])))

with open("input" if PROD else "sample") as f:
    lines = [g.strip().split(" ") for g in f.readlines()]
    _steps = [(dirs[d],int(c)) for d,c in lines]

steps = []
[steps.extend([d]*c) for d,c in _steps]

positions = set()
head = (0,0)
phead = [0,0]
tail = (0,0)

tlog = [(0,0)]
hlog = [(0,0)]

last_steps = ((0,0),(0,0))

for i,step in enumerate(steps[2:]):
    if abs(tail[0]-head[0])+abs(tail[1]-head[1]) > 2:
        last_steps = (last_steps[1], steps[i])
        tail = tupsum(*last_steps, tail)
    else:
        last_steps = (last_steps[1], (0,0))
    head = tupsum(head, step)
    positions.add(tail)
    hlog.append(head)
    tlog.append(tail)

print(hlog)
print(tlog)
print(len(positions))