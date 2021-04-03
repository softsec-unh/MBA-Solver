#!/usr/bin/python3

import re
import sys
import time
import z3
from multiprocessing import Process, Value

def verify_mba_unsat(leftExpre, rightExpre, bitnumber, res):
    """check the relaion whether the left expression is euqal to the right expression.
    Args:
        leftExpre: left expression.
        rightExpre: right expression.
        bitnumber: the number of the bits of the variable.
    Returns:
        True: equation.
        False: unequal.
    Raises:
        None.
    """
    x,y,z,t,a,b,c,d,e,f = z3.BitVecs("x y z t a b c d e f", bitnumber)

    try:
        leftEval = eval(leftExpre)
        rightEval = eval(rightExpre)
        solver = z3.Solver()
        solver.add(leftEval != rightEval)
        result = solver.check()
    except:
        res.value = 2
        return None

    if str(result) != "unsat":
        res.value = 2           # False
    else:
        res.value = 1           # True

    return None


def z3_check_time(sourcefilename, timeout, bv=64):
    """input the expression from the source file, then check the equation and output the time of process to desination file.
    Args:
        sourcefilename: source file.
        bv: the bit of the variable.
    """
    desfilename = "{source}.z3.verify.{bv}bit.after.simplify.txt".format(source=sourcefilename, bv=bv)
    fwrite = open(desfilename, "w")
    print("#complex,groundtruth,simcomplex,simground,z3res,verificationtime", file=fwrite)

    solvingList = [0, 0, 0]
    with open(sourcefilename, "r") as data:
        linenum = 0
        for line in data:
            line = line.strip().replace(" ", "")
            if "#" not in line:
                expreStrList = re.split(",", line)
                sourceExpreStr = expreStrList[0]
                groundtruthStr = expreStrList[1]
                sourceSimStr = expreStrList[2]
                groundtruthSimStr = expreStrList[3]
                start = time.time()

                res = Value('i', 0)  # Default value is 0
                # res = verify_mba_unsat(sourceSimStr, groundtruthSimStr, bv)
                p = Process(target=verify_mba_unsat, args=(sourceSimStr, groundtruthSimStr, bv, res,))
                p.start()
                p.join(timeout)      # wait timeout seconds or it finishes

                if p.is_alive():
                    print("Still solving, but kill it as timeout set to", timeout, "seconds ...")
                    p.terminate()
                    p.join()

                result = {
                    0: "Timeout",
                    1: "True",
                    2: "False",
                }
                
                end = time.time()
                elapsed = end - start
                print(sourceExpreStr, groundtruthStr, sourceSimStr, groundtruthSimStr, result[res.value], elapsed, sep=",", file=fwrite, flush=True)

                # print(linenum, sourceExpreStr, groundtruthStr, sourceSimStr, groundtruthSimStr, result[res.value], elapsed)
                print(linenum, result[res.value], "Time =", elapsed)
                linenum += 1
                solvingList[res.value] += 1

    fwrite.close()
    print("Timeout: ", solvingList[0])
    print("True: ", solvingList[1])
    print("False: ", solvingList[2])
    return None




def main(sourcefilename, timeout):
    z3_check_time(sourcefilename, timeout)



if __name__ =="__main__":
    sourcefilename = sys.argv[1]
    timeout = int(sys.argv[2])
    main(sourcefilename, timeout)
