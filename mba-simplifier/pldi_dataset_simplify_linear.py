#!/usr/bin/python3



import re
import sys
sys.path.append("../tools")
import time
from mba_string_operation import verify_mba_unsat, variable_list
from svector_simplify import SvectorSimplify
from truthtable_search_simplify import PMBASimplify



def simplify_lmba(datafile):
    """simplify linear mba expression by the signatrue vector. 
    Args:
        datafile: file storing the original mba expression.
    """
    filewrite = "{source}.simplify.txt".format(source=datafile)

    fw = open(filewrite, "w")
    print("#complex,groundtruth,simplifiedcomplex,simplifiedgroundtruth,z3flag,simtime", file=fw)

    svObj = SvectorSimplify()
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
                start = time.time()
                simExpre1 = svObj.standard_simplify(cmbaExpre, vnumber)
                simExpre2 = svObj.standard_simplify(groundtruth, vnumber)
                elapsed = time.time() - start
                print("z3 solving...")
                #z3res = verify_mba_unsat(groundtruth, simExpre)
                z3res = verify_mba_unsat(simExpre1, simExpre2, 2)
                print(linenum, cmbaExpre, groundtruth, simExpre1, simExpre2, z3res)
                print("z3 solved: ", z3res)
                print(cmbaExpre, groundtruth, simExpre1, simExpre2, z3res, elapsed, sep=",", file=fw)

    fw.close()
    return None




def main(fileread):
    simplify_lmba(fileread)

    return None



if __name__ == "__main__":
    fileread = sys.argv[1]
    main(fileread)



