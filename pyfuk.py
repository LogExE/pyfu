#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument('-v', '--verbose', action='store_true')

args = parser.parse_args()
filename = args.filename
verbose = args.verbose

with open(filename, 'r') as f:
    prog = f.read()

if verbose:
    print("Read:")
    print(prog)
    print("Executing...")

cells = [0] * 256
cur_cell = 0

matching_bracket = {}
balance_stack = []

for i in range(len(prog)):
    if prog[i] == "[":
        balance_stack.append(i)        
    elif prog[i] == "]":
        if len(balance_stack) == 0:
            print("wrongly placed ending bracket.")
            exit(0)
        last_bracket = balance_stack.pop()
        matching_bracket[last_bracket] = i
        matching_bracket[i] = last_bracket
if len(balance_stack) != 0:
    print("brackets are improperly placed.")
    exit(0)

if verbose:
    print("Bracket mapping:")
    print(matching_bracket)

step = 0
i = 0
while i < len(prog):
    ch = prog[i]
    if verbose:
        print(f"STEP {step}, at character '{prog[i]}', cell {cur_cell}, value {cells[cur_cell]}")
    match ch:
        case ">":
            cur_cell += 1
            i += 1
        case "<":
            cur_cell -= 1
            i += 1
        case "+":
            cells[cur_cell] += 1
            i += 1
        case "-":
            cells[cur_cell] -= 1
            i += 1
        case ".":
            print(chr(cells[cur_cell]), end="")
            i += 1
        case ",":
            cells[cur_cell] = ord(input())
            i += 1
        case "[":
            if cells[cur_cell] == 0:
                i = matching_bracket[i]
            else:
                i += 1
        case "]":
            if cells[cur_cell] != 0:
                i = matching_bracket[i]
            else:
                i += 1
        case _:
            i += 1
    step += 1
