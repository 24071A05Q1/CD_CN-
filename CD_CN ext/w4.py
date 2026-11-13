
n = int(input("Number of productions: "))

grammar = {}
for _ in range(n):
    line = input()
    lhs, rhs = line.split("->")
    lhs = lhs.strip()
    grammar[lhs] = [x.strip().split() if x.strip() != "#" else []
                    for x in rhs.split("|")]

start = input("Start symbol: ").strip()
string = input("Input string: ").split()
string.append("$")

nts = list(grammar.keys())
ts = set()

for lhs in grammar:
    for prod in grammar[lhs]:
        for s in prod:
            if s not in nts:
                ts.add(s)

first = {nt: set() for nt in nts}
follow = {nt: set() for nt in nts}
follow[start].add("$")


def first_seq(seq):
    result = set()
    if not seq:
        result.add("#")
        return result

    for symbol in seq:
        if symbol in nts:
            result |= first[symbol] - {"#"}
            if "#" not in first[symbol]:
                break
        else:
            result.add(symbol)
            break
    else:
        result.add("#")

    return result


changed = True
while changed:
    changed = False
    for nt in nts:
        for prod in grammar[nt]:
            old = len(first[nt])
            first[nt] |= first_seq(prod)
            if len(first[nt]) != old:
                changed = True

changed = True
while changed:
    changed = False
    for nt in nts:
        for prod in grammar[nt]:
            for i, symbol in enumerate(prod):
                if symbol in nts:
                    f = first_seq(prod[i + 1:])
                    old = len(follow[symbol])
                    follow[symbol] |= f - {"#"}
                    if "#" in f:
                        follow[symbol] |= follow[nt]
                    if len(follow[symbol]) != old:
                        changed = True

table = {}
conflict = False

for nt in nts:
    for prod in grammar[nt]:
        f = first_seq(prod)
        for t in f - {"#"}:
            key = (nt, t)
            if key in table and table[key] != prod:
                conflict = True
            table[key] = prod

        if "#" in f:
            for t in follow[nt]:
                key = (nt, t)
                if key in table and table[key] != prod:
                    conflict = True
                table[key] = prod

print("\nFIRST:")
for nt in nts:
    print(nt, "=", first[nt])

print("\nFOLLOW:")
for nt in nts:
    print(nt, "=", follow[nt])

if conflict:
    print("\nGrammar is NOT LL(1).")
else:
    print("\nPredictive Parsing Actions:")
    stack = ["$", start]
    i = 0
    step = 1
    accepted = False

    while stack:
        top = stack[-1]
        current = string[i] if i < len(string) else None

        print(step, stack, string[i:], end=" ")

        if top == "$" and current == "$":
            print("ACCEPT")
            accepted = True
            break

        if top not in nts:
            if top == current:
                print("Match", top)
                stack.pop()
                i += 1
            else:
                print("ERROR")
                break
        else:
            prod = table.get((top, current))
            if prod is None:
                print("ERROR: No production")
                break

            stack.pop()
            for symbol in reversed(prod):
                stack.append(symbol)

            print(top, "->", " ".join(prod) if prod else "#")

        step += 1

    print("\nStatus:", "ACCEPTED" if accepted else "REJECTED")
