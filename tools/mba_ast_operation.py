#!/usr/bin/python3

"""
This file including the operation of MBA expression by AST.
"""

import ast
import astunparse


# Store all subtree
def store_all_subtree(ast_root, buf):
    for node in ast.iter_child_nodes(ast_root):
        buf.append([ast.dump(node, annotate_fields=False), node])
        store_all_subtree(node, buf)

# Return the max_common_subtree in buf
def max_common_subtree(buf):
    maxlen = 0
    mcsubtree = []
    s = set()
    for e in buf:
        if e[0] in s:
            if len(e[0]) > maxlen:
                maxlen = len(e[0])
                mcsubtree = e
        else:
            s.add(e[0])

    return mcsubtree


def main():
    mba3 = '((((x|y)*2)-(x^y))|z)+((((x|y)*2)-(x^y))&z)'
    mba5 = '((((x^y)+((x&y)+(x&y)))^~z)+((((x^y)+((x&y)+(x&y)))|z)+(((x^y)+((x&y)+(x&y)))|z)))+1'
    mba1000 = '(((~(x-1)&y)*(~(x-1)|y)+(~(x-1)&~y)*(~(~(x-1))&y))&z)*(((~(x-1)&y)*(~(x-1)|y)+(~(x-1)&~y)*(~(~(x-1))&y))|z)+(((~(x-1)&y)*(~(x-1)|y)+(~(x-1)&~y)*(~(~(x-1))&y))&~z)*(~((~(x-1)&y)*(~(x-1)|y)+(~(x-1)&~y)*(~(~(x-1))&y))&z)-1*~(x&~x)-2*(x|~y)-1*~(x&~y)+5*~(x|y)+9*~(x|~y)+3*(x&~y)+12*(x&y),((-x*y)*z)+1*~(x^y)+7*y'

    root = ast.parse(mba1000)
    subtree_buf = []
    store_all_subtree(root, subtree_buf)
    m = max_common_subtree(subtree_buf)

    print(m[0])
    print(astunparse.unparse(m[1]))

if __name__ =="__main__":
    # sourcefilename = sys.argv[1]
    # main(sourcefilename)
    main()
