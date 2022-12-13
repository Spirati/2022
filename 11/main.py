import yaml
from tqdm import tqdm
import json

def compose(*functions): # return f(g(x))
    if len(functions) == 1:
        return lambda x: functions[0](x)
    return lambda x: functions[0](compose(*functions[1:])(x))

PROD = False
START = True

if START:
    total = 0

    with open("input" if PROD else "sample") as f:
        lines = f.readlines()
        newlines = []
        for line in lines:
            if "Test" in line:
                newlines.append("  Test:\n")
                newlines.append("    test: " + line[line.index("Test"):].split(" ",1)[1])
            else:
                newlines.append(line)

        monkeys_raw = yaml.load("".join(newlines), yaml.UnsafeLoader)

    items = []
    operations = []
    tests = []
    inspections = []
    operation_strings = []
    mods = []
    mod_strings = []
    test_strings = []

    for name,monkey in monkeys_raw.items():
        iftrue = int(monkey['Test']['If true'].split(" ")[-1])
        iffalse = int(monkey['Test']['If false'].split(" ")[-1])
        monkey['Starting items'] = str(monkey['Starting items'])

        
        items.append(list(map(int,monkey["Starting items"].split(", "))))
        operations.append(eval(f"lambda old: {monkey['Operation'].split(' = ')[1]}"))
        operation_strings.append(f"lambda old: {monkey['Operation'].split(' = ')[1]}")
        tests.append(eval(f"lambda val: {iftrue} if not val else {iffalse}"))
        test_strings.append(f"lambda val: {iftrue} if not val else {iffalse}")
        mod_strings.append(f"lambda val: val % {monkey['Test']['test'].split('by ')[-1]}")
        mods.append(eval(mod_strings[-1]))
        inspections.append(0)
else:
    with open("out.json") as f:
        data = json.load(f)
    
    total = data['total']
    items = data['items']
    operations = list(eval(x) for x in data['operations'])
    operation_strings = data['operations']
    tests = list(eval(x) for x in data['tests'])
    test_strings = data['tests']
    mods = list(eval(x) for x in data['mods'])
    mod_strings = data['mods']
    inspections = data['inspections']


def round():
    for i in range(len(items)):
        operation = operations[i]
        test = tests[i]
        mod = mods[i]
        addto = int(mod_strings[i].split("% ")[1])

        inspections[i] += len(items[i])
        for item in items[i]:
            worry = addto + compose(mod, operation)(item)
            target = test(worry)

            items[target].append(worry)
        items[i] = []

for _ in tqdm(range(20)):
    round()

with open("out.json", "w") as f:
    json.dump({
        'items': items, 'operations': operation_strings, 'tests': test_strings, 'mods': mod_strings, 'inspections': inspections, 'total': total
    }, f, indent=2)


monkey_business = sorted(inspections, reverse=True)
print("Part 1:", monkey_business[0] * monkey_business[1])
