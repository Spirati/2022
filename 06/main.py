from time import perf_counter as perf_counter_ns

PROD = True

def first_unique(length: int, line: str):
    for i in range(len(line)-length):
        if len(set(line[i:i+length])) == length:
            return i+length

with open("input_big2.txt" if PROD else "sample") as f:
    lines = [g.strip() for g in f.readlines()]

start = perf_counter_ns()
a = [first_unique(4, line) for line in lines]
stop = perf_counter_ns()
print("Part 1:", stop - start)
start = perf_counter_ns()
a = [first_unique(14, line) for line in lines]
stop = perf_counter_ns()
print("Part 2:", stop - start)