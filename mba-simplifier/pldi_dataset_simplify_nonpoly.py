#!/usr/bin/python3



import re
import sys
sys.path.append("../tools")
import time
from mba_string_operation import verify_mba_unsat, variable_list, expression_2_term
from svector_simplify import SvectorSimplify
from truthtable_search_simplify import PMBASimplify


def simplify_pmba(mbaExpre):
    """
    """
    basisVec = ["x", "y", "(x|y)", "~(x&~x)"]
    vnumber = 2
    if re.search("z", mbaExpre):
        basisVec = ["x", "y", "z", "(x&y)",  "(y&z)", "(x&z)", "(x&y&z)", "~(x&~x)"]
        vnumber = 3
    psObj = PMBASimplify(vnumber, basisVec)
    simExpre = psObj.simplify(mbaExpre)
    z3res = verify_mba_unsat(simExpre, mbaExpre, 2)
    if z3res:
        return simExpre
    else:
        print("error in simplify_pmba")



def simplify_npmba(datafile):
    """simplify nonpoly mba expression by the signatrue vector. 
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

                #cannot simplify
                if len(itemList) < 3:
                    start = time.time()
                    cmbaSimExpre = cmbaExpre
                    #print("z3 solving: ")
                    z3res = verify_mba_unsat(cmbaSimExpre, groundtruth, 2)
                    elapsed = time.time() - start
                    #print("z3 solved: ", z3res)
                    if z3res:
                        print("MBA Solver cannot process: unkown expression")
                        print(linenum, cmbaExpre, groundtruth, cmbaSimExpre, groundtruth, "unknown")
                        print(cmbaExpre, groundtruth, cmbaSimExpre, groundtruth, "unknown", elapsed, sep=",",file=fw)
                    else:
                        print("error in simplify_npmba")
                        exit(1)
                    continue
                #can simplify
                subExpre = itemList[2]
                start = time.time()
                #process complex MBA expression 
                if re.search("x", cmbaExpre):
                    #process sub-expression
                    subExpre1 = subExpre.replace("a", "x").replace("b", "y")[1:-1]
                    subSimExpre = simplify_pmba(subExpre1)
                    subSimExpre = subSimExpre.replace("x", "a").replace("y", "b")
                    #replace the sub expression with y variable
                    cmbaExpre1 = cmbaExpre.replace(subExpre, "y")
                    cmbaSimExpre = simplify_pmba(cmbaExpre1)
                    #replace the "y" variable with subSimExpre
                    cmbaSimExpre = cmbaSimExpre.replace("y", subSimExpre)
                elif re.search("y", cmbaExpre):
                    #process sub-expression
                    subExpre1 = subExpre.replace("a", "x").replace("b", "y")[1:-1]
                    subSimExpre = simplify_pmba(subExpre1)
                    subSimExpre = subSimExpre.replace("x", "a").replace("y", "b")
                    #replace the sub expression with x variable
                    cmbaExpre1 = cmbaExpre.replace(subExpre, "x")
                    cmbaSimExpre = simplify_pmba(cmbaExpre1)
                    #replace the "y" variable with subSimExpre
                    cmbaSimExpre = cmbaSimExpre.replace("x", subSimExpre)
                #process ground truth
                if re.search("x", groundtruth):
                    groundtruthSim = groundtruth.replace("b", "y")
                    groundtruthSim = simplify_pmba(groundtruthSim)
                    groundtruthSim = groundtruthSim.replace("y", "b")
                elif re.search("y", cmbaExpre):
                    groundtruthSim = groundtruth.replace("a", "x")
                    groundtruthSim = simplify_pmba(groundtruthSim)
                    groundtruthSim = groundtruthSim.replace("x", "a")

                elapsed = time.time() - start
                print("z3 solving: ")
                z3res = verify_mba_unsat(cmbaSimExpre, groundtruth, 2)
                print("z3 solved: ", z3res)
                if z3res:
                    print(linenum, cmbaExpre, groundtruth, cmbaSimExpre, groundtruthSim, z3res)
                    print(cmbaExpre, groundtruth, cmbaSimExpre, groundtruthSim, z3res, elapsed, sep=",",file=fw)
                else:
                    print("error in simplify_npmba")
                    exit(1)

    fw.close()
    return None



def main(fileread):
    simplify_npmba(fileread)

    return None



if __name__ == "__main__":
    fileread = sys.argv[1]
    main(fileread)



