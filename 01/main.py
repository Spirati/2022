PROD = True

with open("input" if PROD else "sample") as f:
    lines = [
        [int(z or 0) for z in x.split("\n")] for x in f.read().split("\n\n")
    ]

print("Part 1:", 
    max(map(sum, lines)))

print("Part 2:", 
    sum(sorted(list(map(sum, lines))[-3:]))) 