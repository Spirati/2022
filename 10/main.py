PROD = True

registers = {
    "X": 0
}

with open("input" if PROD else "sample") as f:
    lines = [g.strip() for g in f.readlines()]

cycle = 0
