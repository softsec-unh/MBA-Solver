#!/usr/bin/python2

import re
import sys
import time
import stp
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
    s = stp.Solver()
    x = s.bitvec("x", bitnumber)
    y = s.bitvec("y", bitnumber)
    z = s.bitvec("z", bitnumber)
    t = s.bitvec("t", bitnumber)
    a = s.bitvec("a", bitnumber)
    b = s.bitvec("b", bitnumber)
    c = s.bitvec("c", bitnumber)
    d = s.bitvec("d", bitnumber)
    e = s.bitvec("e", bitnumber)
    f = s.bitvec("f", bitnumber)

    leftEval = eval(leftExpre)
    rightEval = eval(rightExpre)

    s.add(leftEval != rightEval)
    result = s.check()

    if result:
        res.value = 2
    else:
        res.value = 1

    return None



def stp_check_time(sourcefilename, timeout, bv=64):
    """input the expression from the source file, then check the equation and output the time and memory of process to desination file.
    Args:
        sourcefilename: source file.
    """
    desfilename = "{source}.stp.verify.{bv}bit.before.simplify.txt".format(source=sourcefilename, bv=bv)
    fwrite = open(desfilename, "w")
    comment = "#complex,groundtruth,stpres,verificationtime\n"
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
                res = Value('i', 0)
                #res = verify_mba_unsat(sourceExpreStr, groundExpreStr, bv)
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
    stp_check_time(sourcefilename, timeout)



if __name__ =="__main__":
    sourcefilename = sys.argv[1]
    timeout = int(sys.argv[2])
    main(sourcefilename, timeout)




