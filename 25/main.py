from __future__ import annotations

from typing import List

class SnafuDigit:
    symbols = "012=-"
    symbol_mappings = {
        "0": 0,
        "1": 1,
        "2": 2,
        "=": -2,
        "-": -1
    }
    
    def __init__(self, digit: str):
        if digit not in SnafuDigit.symbol_mappings:
            raise ValueError(f"invalid digit \"{digit}\"")
        self.digit = digit
    
    def __add__(self, other: SnafuDigit):
        return SnafuDigit(
            SnafuDigit.symbols[(SnafuDigit.symbol_mappings[self.digit]+SnafuDigit.symbol_mappings[other.digit])%5]
        )

    @classmethod
    def overflow(cls, *summands: List[SnafuDigit]):
        unmodded = sum(SnafuDigit.symbol_mappings[summand.digit] for summand in summands)
        if unmodded >= 3:
            return SnafuDigit("1")
        elif unmodded < -2:
            return SnafuDigit("-")
        return SnafuDigit("0")
    
    def __eq__(self, other: SnafuDigit):
        return self.digit == other.digit
    
    def __str__(self):
        return self.digit
    
    def __repr__(self):
        return str(self)

class SnafuNumber:
    def __init__(self, digits: List[SnafuDigit]):
        self.digits = digits # stored little-endian
    def __add__(self, other: SnafuNumber):
        longer = max(other, self, key=lambda number: len(number.digits))
        shorter = self if longer == other else other

        len_longer = len(longer.digits)
        len_shorter = len(shorter.digits)
        queue_shorter = shorter.digits + [SnafuDigit("0") for _ in range(len_longer-len_shorter)] # extend with 0s
        outdigits = []
        carry = SnafuDigit("0")
        for a,b in zip(longer.digits, queue_shorter):
            outdigits.append(a + b + carry)
            carry = SnafuDigit.overflow(a, b, carry)

        if carry != SnafuDigit("0"):
            outdigits.append(carry)
        return SnafuNumber(outdigits)
        
    def __repr__(self):
        return "".join(str(digit) for digit in self.digits[::-1])
    
    def __int__(self):
        return sum(
            (5**i)*SnafuDigit.symbol_mappings[digit.digit] for i,digit in enumerate(self.digits)
        )

    @classmethod
    def from_str(cls, digit_string: str):
        return cls([SnafuDigit(char) for char in digit_string[::-1]])

if __name__ == "__main__":
    PROD = True

    with open("input" if PROD else "sample") as f:
        lines = [g.strip() for g in f.readlines()]

    total = sum([SnafuNumber.from_str(line) for line in lines], SnafuNumber.from_str("0"))
    print("Part 1:", total, f"({int(total)})")