#!/usr/bin/python2

import re
import sspam
from sspam import simplifier
import sys
import time



def sspam_simplify(sourcefilename, desfilename):
    fwrite = open(desfilename, "w")
    fwrite.write("#complex,groundtruth,simplified,simtime\n")

    with open(sourcefilename) as data:
        linenum = 0
        for line in data:
            line = line.replace("\n","")
            if "#" not in line and line:
                expreStrList = re.split(",", line)
                sourceStr = expreStrList[0]
                start = time.time()
                simStr = simplifier.simplify(sourceStr).replace(" ", "")
                end = time.time()
                elapsed = end - start
                resultStr = line
                resultStr += "," + simStr + "," + str(elapsed) + "\n"
                fwrite.write(resultStr)
                fwrite.flush()
                print linenum, sourceStr, simStr
                linenum += 1

    return None

    
def main(sourcefilename, desfilename):
    sspam_simplify(sourcefilename, desfilename)
    


if __name__ == "__main__":
    sourcefilename = sys.argv[1]
    desfilename = sys.argv[2]
    main(sourcefilename, desfilename)



