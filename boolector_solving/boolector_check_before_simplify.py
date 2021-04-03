#!/usr/bin/python2

import pyboolector
import re
import sys
sys.path.append("../tools")
import time
from pyboolector import Boolector, BoolectorException
#from mba_string_operation import variable_list
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
    btor = Boolector()
    btor.Set_opt(pyboolector.BTOR_OPT_INCREMENTAL, True)
    btor.Set_opt(pyboolector.BTOR_OPT_MODEL_GEN, 1)
    _bv = btor.BitVecSort(bitnumber)

    x = btor.Var(_bv, "x")
    y = btor.Var(_bv, "y")
    z = btor.Var(_bv, "z")
    t = btor.Var(_bv, "t")
    a = btor.Var(_bv, "a")
    b = btor.Var(_bv, "b")
    c = btor.Var(_bv, "c")
    d = btor.Var(_bv, "d")
    e = btor.Var(_bv, "e")
    f = btor.Var(_bv, "f")

    leftEval = eval(leftExpre)
    rightEval = eval(rightExpre)
    btor.Assert(leftEval != rightEval)
    btor.Sat()

    variableList = variable_list(leftExpre)
    try:
        for variable in variableList:
            eval(variable).assignment
    except:
        res.value = 1
    else:
        res.value = 2 

    return None

def variable_list(expreStr):
    """get the set of variable of expression.
    Args:
        expreStr: the mba expression string.
    Return:
        variableList: the list of variables.
    Raise:
        None.
    """
    varSet = set(expreStr)
    variableList = []
    for i in varSet:
        #the variable name
        if i in ["x", "y", "z", "t", "a", "b", "c", "d", "e", "f"]:
            variableList.append(i)

    return variableList



def boolector_check_time(sourcefilename, timeout, bv=64):
    """input the expression from the source file, then check the equation and output the time of process to desination file.
    Args:
        sourcefilename: source file.
    Returns:
        None.
    Raises:
        None.
    """
    desfilename = "{source}.boolector.verify.{bv}bit.before.simplify.txt".format(source=sourcefilename, bv=bv)
    fwrite = open(desfilename, "w")
    comment = "#complex,groundtruth,boolectorres,verificationtime\n"
    fwrite.write(comment)

    with open(sourcefilename, "r") as data:
        linenum = 0
        for line in data:
            line = line.strip().replace(" ", "")
            if "#" not in line:
                expreStrList = re.split(",", line)
                sourceExpreStr = expreStrList[0]
                groundExpreStr = expreStrList[1]
                start = time.time()
                #res = verify_mba_unsat(sourceExpreStr, groundExpreStr, bv)
                res = Value('i', 0)
                p = Process(target=verify_mba_unsat, args=(sourceExpreStr, groundExpreStr, bv, res,))
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
                resultStr = "{source},{ground},{res},{vtime}\n".format(source=sourceExpreStr, ground=groundExpreStr, res=result[res.value], vtime=elapsed)
                fwrite.write(resultStr)
                fwrite.flush()

                # print linenum, sourceExpreStr, groundExpreStr, result[res.value], elapsed
                print linenum, result[res.value], "Time =", elapsed
                linenum += 1

    fwrite.close()
    return None


def main(sourcefilename, timeout):
    boolector_check_time(sourcefilename, timeout)
    
    return None


if __name__ =="__main__":
    sourcefilename = sys.argv[1]
    timeout = int(sys.argv[2])
    main(sourcefilename, timeout)

