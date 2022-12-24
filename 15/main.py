from __future__ import annotations

from typing import List, Callable

PROD = True

def symmetric(test: Callable[[any, any], bool]) -> Callable[[any, any], bool]:
    return lambda x,y: test(x, y) or test(y, x)

@symmetric
def bound_check(R1, R2):
    return R1.start >= R2.start and R1.start <= R2.stop


def shift_range(r: range, n: int):
    return range(r.start+n, r.stop+n)

class UnifiedRange:
    def __init__(self, *ranges):
        self.ranges = ranges
    
    @classmethod
    def union(cls, *ranges):
        # remove redundant ranges for efficiency
        r: List[range] = sorted(ranges, key=lambda r: r.start)
        merged = True
        while merged:
            temp = []
            merged = False
            for i in range(len(r)-1):
                r1,r2 = r[i],r[i+1]

                if bound_check(r1, r2):
                    temp.append(range(min(r1.start, r2.start), max(r2.start, r2.stop)))
                    merged = True
                else:
                    temp.append(r2)
            if merged:
                r = temp.copy()

        return cls(*r)

    @classmethod
    def intersection(cls, *ranges):
        out = ranges
        merged = True
        while len(out) > 1 or merged:
            merged = True
            temp = []
            for r1,r2 in zip(out, out[1:]):
                if bound_check(r1, r2):
                    merged = False
                    temp.append(range(max(r1.start, r2.start), min(r1.stop, r2.stop)))
            out = temp
        return cls(*out)

    def intersection(self, *others: UnifiedRange):
        ranges = [r for other in others for r in other.ranges]
        return UnifiedRange.intersection(*self.ranges, *ranges)
    
    def union(self, *others: UnifiedRange):
        ranges = [r for other in others for r in other.ranges]
        return UnifiedRange.union(*self.ranges, *ranges)

    def contains(self, val):
        return any(val in r for r in self.ranges)



with open("input" if PROD else "sample") as f:
    lines = [g.strip() for g in f.readlines()]