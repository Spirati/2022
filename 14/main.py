from scipy import sparse
from numpy import roll
from typing import Tuple

def compose(*functions):
    if len(functions) == 1:
        return lambda x: functions[0](x)
    return lambda x: functions[0](compose(*functions[1:]))

max_y = 0

def parse_instruction(state: sparse.lil_matrix, instruction: str):
    global max_y
    instructions = tuple([
        tuple(map(int, inst.split(","))) for inst in instruction.split(" -> ")
    ])
    for (sx,sy),(ex,ey) in zip(instructions, instructions[1:]):
        if (m := max(sy, ey)) > max_y:
            max_y = m
        dim_y, dim_x = state.shape
        if sx >= dim_x or ex >= dim_x or sy >= dim_y or ey >= dim_y:
            dim_x = max(sx, ex, dim_x)
            dim_y = max(sy, ey, dim_y)
            state.resize(dim_y+1,dim_x+1)
        if sx == ex:
            diff = 1 if sy < ey else -1
            for y in range(sy, ey+diff, diff):
                state[y,sx] = 1
        elif sy == ey:
            diff = 1 if sx < ex else -1
            for x in range(sx, ex+diff, diff):
                state[sy,x] = 1


shifts = 0

def add_grain(state: sparse.lil_matrix, source: Tuple[int, int]) -> bool:
    global max_y
    global shifts
    sy,sx = source
    bound_y, bound_x = state.shape
    can_move = True
    while can_move:
        if state[source[0],source[1]] == 2:
            return False
        if sy+1 == max_y:
            can_move = False
            break
        else:
            if not state[sy+1, sx+shifts]: # immediately below is free
                sy += 1
            else:
                if not state[sy+1, sx-1+shifts]: # DL is free
                    sy += 1
                    sx -= 1
                else:
                    if sx+1 == bound_x:
                        state.resize(bound_y, bound_x+1)
                        bound_x += 1
                    if not state[sy+1, sx+1]: # DR is free
                        sy += 1
                        sx += 1
                    else:
                        can_move = False
    state[sy, sx] = 2
    return True


PROD = True

state = sparse.lil_matrix((501, 501), dtype=int)
state[0,500] = 3 # source

with open("input" if PROD else "sample") as f:
    lines = [g.strip() for g in f.readlines()]
    for line in lines:
        parse_instruction(state, line)

max_y += 2

cy,cx = state.shape
state.resize(max_y+1, cx)

counter = 0
can_add = True
try:
    while can_add:
        can_add = add_grain(state, (0, 500))
        counter += 1
except KeyboardInterrupt:
    pass

print(counter-1)

with open("outfile.txt", "w") as f:
    symbols = ".#o+"
    out = state.todense()
    for y in range(out.shape[0]):
        f.write("".join(symbols[int(a)] for a in str(out[y]).replace("\n","").replace(" ","").replace("[","").replace("]","")) + "\n")