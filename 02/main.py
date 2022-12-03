PROD = True

value = lambda letter, them=False: 1 + ord(letter)-(65 if them else 88)
score = lambda you, them: 3*((value(you) - value(them, True) + 1) % 3)

with open("input" if PROD else "sample") as f:
    lines = [g.strip() for g in f.readlines()]

print("Part 1", sum(
    value(you) + score(you, them) for them,you in map(lambda line: line.split(" "), lines)
))

print("Part 2", sum(
    1+(value(them, True) + value(you)) % 3 +
    3*(value(you)-1) 
    for them,you in map(lambda line: line.split(" "), lines)
))