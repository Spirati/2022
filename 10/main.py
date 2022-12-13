PROD = True

registers = {
    "X": 1
}
queue = {
    "X": 0
}

grid = {(x, y): "." for x in range(40) for y in range(6)}

with open("input" if PROD else "sample") as f:
    lines = [g.strip() for g in f.readlines()]

busy = False
countdown = 0
cycle = 1
consumer = iter(lines)

total = 0

line = next(consumer, None)
if line == "noop":
    countdown = 0
elif line.split(" ")[0] == "addx":
    queue["X"] = int(line.split(" ")[1])
    countdown = 1

while line:

    pixel_raw = cycle-1
    px = pixel_raw % 40
    py = pixel_raw//40

    if any(px+i == registers["X"] for i in range(-1,2)):
        grid[px,py] = "█"


    total += cycle*(registers["X"]*int(not ((cycle-20) % 40)))

    if countdown > 0:
        countdown -= 1
    else:
        registers["X"] += queue["X"]
        queue["X"] = 0
        line = next(consumer, None)
        if not line:
            break
        if line == "noop":
            countdown = 0
        elif line.split(" ")[0] == "addx":
            queue["X"] = int(line.split(" ")[1])
            countdown = 1
    cycle += 1


print("Part 1:", total)
print("Part 2:")
print(*["".join(grid[x,y] for x in range(40)) for y in range(6)], sep="\n")