from functools import reduce

def bubblesort(l, c):
    n = len(l)
    swapped = False
    for j in range(n-1): # max repeats
        for i in range(0, n-j-1): # one fewer each time
            if not c(l[i], l[i+1]):
                swapped = True
                l[i],l[i+1] = l[i+1],l[i]
        if not swapped:
            return

def compare(left, right):
    if isinstance(left, int):
        if isinstance(right, int):
            if left < right:
                return True
            elif left > right:
                return False
            else:
                return None
        elif isinstance(right, list):
            return compare([left], right)
    elif isinstance(left, list):
        if isinstance(right, int):
            return compare(left, [right])
        elif isinstance(right, list):
            for x,y in zip(left, right):
                check = compare(x,y)
                if check is not None:
                    return check
            if len(left) < len(right):
                return True
            elif len(left) > len(right):
                return False
            return None

PROD = True

with open("input" if PROD else "sample") as f:
    lines = list(map(eval, filter(bool, [g.strip() for g in f.readlines()])))
    pairs = [lines[2*i:2*(i+1)] for i in range(len(lines)//2)]

print(
    "Part 1:",
    sum(i+1 for i,p in enumerate(pairs) if compare(*p))
)

part2 = sum(pairs, [ [[2]], [[6]] ])
bubblesort(part2, compare)

stringified = list(map(str, part2))

# i do not feel like doing this for both [[2]] and [[6]] so just do it to both and multiply
decoderkey = reduce(lambda a,b: a*b,
    map(lambda c: stringified.index(c)+1, ["[[2]]","[[6]]"]),1
)

print("Part 2:", decoderkey)