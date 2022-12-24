from __future__ import annotations
import re

from typing import Tuple, Optional, Callable

operations = {
    "+": lambda a,b: a+b,
    "-": lambda a,b: a-b,
    "*": lambda a,b: a*b,
    "/": lambda a,b: a//b
}
inverses = {
    "+": operations["-"],
    "-": operations["+"],
    "*": operations["/"],
    "/": operations["*"]
}
BinaryArithmetic = Callable[[int, int], int]



PROD = False

grab = re.compile(R"(\w+): (\d+|(\w+) ([+\-*/]) (\w+))")

with open("input" if PROD else "sample") as f:
    lines = list([grab.search(g.strip()).groups() for g in f.readlines()])

compiled = {}
queued = {}

for name, predicate, dep1, operation, dep2 in lines:
    if dep1 is None: # raw value
        compiled[name] = {"value": int(predicate)}
    else: # dependencies
        queued[name] = {"value": None, "depends-on": [dep1, dep2], "operation": operations[operation]}

def in_dependency_tree(root, search): # see if search depends on root
    def search_(search):
        if search in compiled:
            return False
        elif root in queued[search]["depends-on"]:
            return search
        results = list(filter(bool, [search_(dep) for dep in queued[search]["depends-on"]]))
        if any(results):
            return results[0]
        return False
    return search_(search)

def resolve(name):
    if name in compiled:
        return compiled[name]["value"]
    dep1, dep2 = queued[name]["depends-on"]
    out = queued[name]["operation"](resolve(dep1), resolve(dep2))
    queued.pop(name)
    compiled[name] = {"value": out}
    return out

to_match_name, deps_on_hmn_name = sorted([(dep, in_dependency_tree("humn", dep)) for dep in queued["root"]["depends-on"]], key = lambda x: bool(x[1]))
# to_match = resolve(to_match_name[0])
deps_on_hmn = deps_on_hmn_name[0]
print(deps_on_hmn)

operation_stack = []

def resolve2(name):
    if in_dependency_tree(deps_on_hmn_name, name):
        operation_stack.append(name)
        
    if name in compiled:
        return compiled[name]["value"]
    dep1, dep2 = queued[name]["depends-on"]
    out = queued[name]["operation"](resolve2(dep1), resolve2(dep2))
    queued.pop(name)
    compiled[name] = {"value": out}
    return out

resolve2("root")
print(operation_stack)