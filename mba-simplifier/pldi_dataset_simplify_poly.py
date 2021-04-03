#!/usr/bin/python3



import re
import sys
sys.path.append("../tools")
import time
from mba_string_operation import verify_mba_unsat, variable_list, expression_2_term
from svector_simplify import SvectorSimplify
from truthtable_search_simplify import PMBASimplify


def simplify_linear_combination(mbaExpre):
    """
    """
    #basisVec2 = ["x", "y", "(x|y)", "~(x&~x)"]
    basisVec2 = ["(x&y)", "(~x&y)", "(x&~y)", "(~x&~y)"]
    basisVec4 = ["x", "y", "z", "t", "(x&y)",  "(x&z)", "(x&t)", "(y&z)", "(y&t)","(z&t)", "(x&y&z)", "(x&y&t)", "(x&z&t)", "(y&z&t)", "(x&y&z&t)", "~(x&~x)"]
    #basisVec4 = ["(x&y&z&t)", "(~x&y&t&z)", "(x&~y&z&t)", "(x&y&~z&t)", "(x&y&z&~t)",  "(~x&~y&z&t)", "(x&~y&~z&t)", "(x&y&~z&~t)", "(~x&y&~z&t)","(~x&y&z&~t)", "(x&~y&z&~t)", "(x&~y&~z&~t)", "(~x&y&~z&~t)", "(~x&~y&z&~t)", "(~x&~y&~z&t)", "(~x&~y&~z&~t)"]
    termList = expression_2_term(mbaExpre)
    xytermList = []
    nxytermList = []
    for term in termList:
        if len(variable_list(term)) == 2:
            xytermList.append(term)
        else:
            nxytermList.append(term)
    xyExpre = "".join(xytermList)
    nxyExpre = "".join(nxytermList)
    psObj = PMBASimplify(2, basisVec2)
    simxyExpre = psObj.simplify(xyExpre)
    psObj = PMBASimplify(4, basisVec4)
    simnxyExpre = psObj.simplify(nxyExpre)
    if simnxyExpre[0] == "-" or simnxyExpre[0] == "+":
        simExpre = simxyExpre + simnxyExpre
    else:
        simExpre = simxyExpre + "+" + simnxyExpre

    return simExpre


def simplify_pmba(datafile):
    """simplify poly mba expression by the signatrue vector. 
    Args:
        datafile: file storing the original mba expression.
    """
    filewrite = "{source}.simplify.txt".format(source=datafile)

    fw = open(filewrite, "w")
    print("#complex,groundtruth,simplifiedcomplex,simplifiedgroundtruth,z3flag,simtime", file=fw)

    linenum = 0
    with open(datafile, "rt") as fr:
        for line in fr:
            if "#" not in line:
                linenum += 1
                line = line.strip()
                itemList = re.split(",", line)
                cmbaExpre = itemList[0]
                groundtruth = itemList[1]
                vnumber = len(variable_list(cmbaExpre))
                if vnumber == 1:
                    #basisVec = ["x","~(x&~x)"]
                    basisVec = ["x","~x"]
                elif vnumber == 2:
                    basisVec = ["x", "y", "(x|y)", "~(x&~x)"]
                    #basisVec = ["(x&y)", "(~x&y)", "(x&~y)", "(~x&~y)"]
                elif vnumber == 3:
                    basisVec = ["x", "y", "z", "(x&y)",  "(y&z)", "(x&z)", "(x&y&z)", "~(x&~x)"]
                    #basisVec = ["(x&y&z)", "(~x&y&z)", "(x&~y&z)", "(x&y&~z)",  "(~x&~y&z)", "(~x&y&~z)", "(x&~y&~z)", "(~x&~y&~z)"]
                elif vnumber == 4:
                    #basisVec = ["x", "y", "z", "t", "(x&y)",  "(x&z)", "(x&t)", "(y&z)", "(y&t)","(z&t)", "(x&y&z)", "(x&y&t)", "(x&z&t)", "(y&z&t)", "(x&y&z&t)", "~(x&~x)"]
                    basisVec = ["(x&y&z&t)", "(~x&y&t&z)", "(x&~y&z&t)", "(x&y&~z&t)", "(x&y&z&~t)",  "(~x&~y&z&t)", "(x&~y&~z&t)", "(x&y&~z&~t)", "(~x&y&~z&t)","(~x&y&z&~t)", "(x&~y&z&~t)", "(x&~y&~z&~t)", "(~x&y&~z&~t)", "(~x&~y&z&~t)", "(~x&~y&~z&t)", "(~x&~y&~z&~t)"]
                if vnumber == 4:
                    start = time.time()
                    simExpre1 = simplify_linear_combination(cmbaExpre)
                    simExpre2 = simplify_linear_combination(groundtruth)
                    elapsed = time.time() - start
                    print("z3 solving...")
                    z3res = verify_mba_unsat(simExpre1, simExpre2, 2)
                    print(linenum, cmbaExpre, groundtruth, simExpre1, simExpre2, z3res)
                    print("z3 solved: ", z3res)
                    print(cmbaExpre, groundtruth, simExpre1, simExpre2, z3res, elapsed, sep=",", file=fw)
                    continue
                psObj = PMBASimplify(vnumber, basisVec)
                start = time.time()
                simExpre1 = psObj.simplify(cmbaExpre)
                simExpre2 = psObj.simplify(groundtruth)
                elapsed = time.time() - start
                print("z3 solving...")
                z3res = verify_mba_unsat(simExpre1, simExpre2, 2)
                print(linenum, cmbaExpre, groundtruth, simExpre1, simExpre2, z3res)
                print("z3 solved: ", z3res)
                print(cmbaExpre, groundtruth, simExpre1, simExpre2, z3res, elapsed, sep=",", file=fw)

    fw.close()
    return None



def main(fileread):
    simplify_pmba(fileread)

    return None



if __name__ == "__main__":
    fileread = sys.argv[1]
    main(fileread)



