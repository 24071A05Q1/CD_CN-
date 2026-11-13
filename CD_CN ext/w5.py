
from collections import defaultdict, deque

n = int(input("Number of productions: "))

grammar = []
nts = []

for _ in range(n):
    line = input()
    lhs, rhs = line.split("->")
    lhs = lhs.strip()

    if lhs not in nts:
        nts.append(lhs)

    for part in rhs.split("|"):
        part = part.strip()
        grammar.append((lhs, tuple(part.split()) if part != "#" else ()))

start = input("Start symbol: ").strip()

aug = start + "'"
while aug in nts:
    aug += "'"

grammar.insert(0, (aug, (start,)))
nts = [aug] + nts

terms = set()
for lhs, rhs in grammar:
    for s in rhs:
        if s not in nts:
            terms.add(s)

terms.add("$")

by_lhs = defaultdict(list)
for i, (lhs, rhs) in enumerate(grammar):
    by_lhs[lhs].append(i)

first = {nt: set() for nt in nts}

def first_seq(seq):
    result = set()

    if not seq:
        return {"#"}

    for s in seq:
        if s in nts:
            result |= first[s] - {"#"}
            if "#" not in first[s]:
                break
        else:
            result.add(s)
            break
    else:
        result.add("#")

    return result

changed = True
while changed:
    changed = False
    for lhs, rhs in grammar:
        old = len(first[lhs])
        first[lhs] |= first_seq(rhs)
        if len(first[lhs]) != old:
            changed = True


def closure(items):
    items = set(items)
    changed = True

    while changed:
        changed = False
        new_items = set()

        for p, dot, look in items:
            lhs, rhs = grammar[p]

            if dot < len(rhs) and rhs[dot] in nts:
                B = rhs[dot]
                seq = rhs[dot + 1:] + (look,)
                lookaheads = first_seq(seq) - {"#"}

                for q in by_lhs[B]:
                    for b in lookaheads:
                        item = (q, 0, b)
                        if item not in items:
                            new_items.add(item)

        if new_items:
            items |= new_items
            changed = True

    return frozenset(items)


def goto(items, symbol):
    moved = set()

    for p, dot, look in items:
        rhs = grammar[p][1]

        if dot < len(rhs) and rhs[dot] == symbol:
            moved.add((p, dot + 1, look))

    return closure(moved) if moved else frozenset()


# Construct canonical LR(1) states
I0 = closure({(0, 0, "$")})
states = [I0]
transitions = {}
queue = deque([0])

symbols = list(terms - {"$"}) + nts

while queue:
    i = queue.popleft()

    for symbol in symbols:
        nxt = goto(states[i], symbol)

        if not nxt:
            continue

        if nxt not in states:
            states.append(nxt)
            queue.append(len(states) - 1)

        j = states.index(nxt)
        transitions[(i, symbol)] = j


# Merge states with identical LR(0) cores
cores = []
merged = []
state_map = {}

for i, state in enumerate(states):
    core = frozenset((p, dot) for p, dot, look in state)

    if core not in cores:
        cores.append(core)
        merged.append(set())

    group = cores.index(core)
    merged[group] |= set(state)
    state_map[i] = group


# Build LALR ACTION and GOTO tables
action = {}
goto_table = {}
conflict = False


def put(table, key, value):
    global conflict

    if key in table and table[key] != value:
        print("CONFLICT:", key, table[key], value)
        conflict = True
    else:
        table[key] = value


for i, state in enumerate(merged):

    for p, dot, look in state:
        lhs, rhs = grammar[p]

        if dot < len(rhs):
            symbol = rhs[dot]
            old_target = transitions.get(
                (next(k for k, v in state_map.items()
                      if v == i and (k, symbol) in transitions), symbol)
            )

            # Find the corresponding merged destination
            for old_state in range(len(states)):
                if state_map[old_state] == i and (old_state, symbol) in transitions:
                    target = state_map[transitions[(old_state, symbol)]]

                    if symbol in terms:
                        put(action, (i, symbol), ("s", target))
                    else:
                        put(goto_table, (i, symbol), target)

        else:
            if lhs == aug:
                put(action, (i, "$"), ("acc",))
            else:
                put(action, (i, look), ("r", p))


if conflict:
    print("\nGrammar has LALR parsing conflicts.")
    print("Status: REJECTED")
else:
    print("\nLALR Parsing Actions:")

    string = input("Input string: ").split()
    string.append("$")

    stack = [0]
    symbols_stack = []
    i = 0
    step = 1
    accepted = False

    while True:
        state = stack[-1]
        current = string[i] if i < len(string) else "$"
        act = action.get((state, current))

        print(step, "Stack:", stack,
              "Symbols:", symbols_stack,
              "Input:", string[i:], end=" ")

        if act is None:
            print("ERROR")
            break

        if act[0] == "s":
            print("SHIFT", current)
            symbols_stack.append(current)
            stack.append(act[1])
            i += 1

        elif act[0] == "r":
            p = act[1]
            lhs, rhs = grammar[p]

            print("REDUCE", lhs, "->",
                  " ".join(rhs) if rhs else "#")

            for _ in rhs:
                symbols_stack.pop()
                stack.pop()

            new_state = goto_table.get((stack[-1], lhs))

            if new_state is None:
                print("ERROR: GOTO missing")
                break

            symbols_stack.append(lhs)
            stack.append(new_state)

        elif act[0] == "acc":
            print("ACCEPT")
            accepted = True
            break

        step += 1

    print("\nStatus:", "ACCEPTED" if accepted else "REJECTED")
