#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument('-v', '--verbose', action='store_true')

args = parser.parse_args()
filename = args.filename
verbose = args.verbose

with open(filename, 'r') as f:
    prog = f.read().strip()

if verbose:
    print("the program:")
    print(prog)
    print("starting parsing...")

cells = [0] * 256
cur_cell = 0

matching_bracket = {}
balance_stack = []

for i in range(len(prog)):
    if prog[i] == "[":
        balance_stack.append(i)        
    elif prog[i] == "]":
        if len(balance_stack) == 0:
            print(f"at char {i}: a wrongly placed ending bracket!")
            exit(0)
        last_bracket = balance_stack.pop()
        matching_bracket[last_bracket] = i
        matching_bracket[i] = last_bracket
if len(balance_stack) != 0:
    print("at EOF: the brackets are improperly balanced!")
    exit(0)

if verbose:
    print("bracket mapping:")
    print(matching_bracket)
    print("executing the program...")

print_mode = "chr"

step = 0
i = 0
while i < len(prog):
    ch = prog[i]
    if verbose:
        print(f"STEP {step}, at character {repr(prog[i])}, cell {cur_cell}, value {cells[cur_cell]}")
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
            val = cells[cur_cell]
            if print_mode == "chr":
                val = chr(val) 
            print(val, end="")
            i += 1
        case ",":
            if verbose:
                print("enter a byte")
                print("> ", end="")
            cells[cur_cell] = ord(input())
            i += 1
        case "!":
            # a custom symbol just for my implementation
            # it switches output mode from char to int
            if print_mode == "chr":
                print_mode = "int"
            else:
                print_mode = "chr"
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
            if verbose:
                print("unknown character, skipping")
            i += 1
    step += 1
