from __future__ import print_function # Py2 compat
from collections import namedtuple
import sys

Keep = namedtuple('Keep', ['line'])
Insert = namedtuple('Insert', ['line'])
Remove = namedtuple('Remove', ['line'])

Frontier = namedtuple('Frontier', ['x', 'history'])

def myers_diff(a_lines, b_lines):
    
    frontier = {1: Frontier(0, [])}

    def one(idx):
        return idx - 1

    a_max = len(a_lines)
    b_max = len(b_lines)
    for d in range(0, a_max + b_max + 1):
        for k in range(-d, d + 1, 2):
            go_down = (k == -d or 
                    (k != d and frontier[k - 1].x < frontier[k + 1].x))
            if go_down:
                old_x, history = frontier[k + 1]
                x = old_x
            else:
                old_x, history = frontier[k - 1]
                x = old_x + 1
            history = history[:]
            y = x - k
            if 1 <= y <= b_max and go_down:
                history.append(Insert(b_lines[one(y)]))
            elif 1 <= x <= a_max:
                history.append(Remove(a_lines[one(x)]))
            while x < a_max and y < b_max and a_lines[one(x + 1)] == b_lines[one(y + 1)]:
                x += 1
                y += 1
                history.append(Keep(a_lines[one(x)]))

            if x >= a_max and y >= b_max:
                return history
            else:
                frontier[k] = Frontier(x, history)
    assert False, 'Could not find edit script'

def getDiff(old,new):
    
    old_char = []
    for char in old:
        old_char.append(char)
    new_char = []
    for char in new:
        new_char.append(char)

    diff = myers_diff(old_char, new_char)
    i = 0
    add_pos = []
    delete_pos = []
    for elem in diff:
        if isinstance(elem, Insert):
            add_pos.append((i,elem.line))
        elif isinstance(elem,Remove):
            delete_pos.append(i)
        i+=1
    return add_pos,delete_pos
