#!/usr/bin/python3

"""
simplify the linear MBA expression by the signal vector:
    step1: create signal vector, which the truth table of the linear MBA expression.
    step2: transform the signal vector into standard basis or non-standard basis.
"""

import numpy as np
import os
import re
import sys
import time
import traceback
from commons import get_entire_bitwise
from mba_string_operation import variable_list, verify_mba_unsat, truthtable_expression, truthtable_bitwise


class LinearMBA():
    """linear MBA expression generation.
    Attributes:
        vnumber: the number of variables.
    """
    def __init__(self, vnumber):
        if vnumber in [1, 2, 3, 4]:
            self.vnumber = vnumber
        else:
            print("the value of vnumber is wrong!")
            traceback.print_stack()
            sys.exit(0)
        self.standardBitList = [None] * 2**vnumber
        self.nonstandardBitList = [] 
        self.get_truthtable()

        return None

    def get_truthtable(self):
        """read the entire truth table from the related file. 
        Args:
            vnumber: the number of variables.
        """
        abspath = os.path.realpath(__file__)
        (dirpath, filename) = os.path.split(abspath)
        fileread = "{dirpath}/{vnumber}variable_truthtable.txt".format(dirpath=dirpath, vnumber=self.vnumber)
        #fileread = "{vnumber}variable_truthtable.txt".format(vnumber=self.vnumber)
        #check the file of truth table
        #try:
        #    with open(fileread, "r") as fr:
        #        pass
        #except:
        #    command = """ python3 -c "from truthtable_generate import exec_all; exec_all()" """
        #    os.system(command)

        with open(fileread, "r") as fr:
            linenum = 0
            for line in fr:
                if "#" not in line:
                    line = line.strip("\n")
                    itemList = re.split(",", line)
                    truthtable = itemList[0]
                    bitwiseExpre = itemList[1]
                    #discard the zero value
                    if not re.search("1", truthtable):
                        continue
                    #standard basis vector
                    elif truthtable.count("1") == 1:
                        truthtable = truthtable.strip("[]")
                        truthtableList = [int(item) for item in truthtable.split(" ")]
                        index = truthtableList.index(1)
                        self.standardBitList[index] = bitwiseExpre
                    else:
                        self.nonstandardBitList.append(bitwiseExpre)
    
        return None

class SvectorSimplify():
    """simplify the linear MBA expression by the signal vector.
    Attributes:
        lmbaExpre: line MBA expression.
        vnumber: the number of variables in the mba expression.
        nonstandardBasis: non-standard basis used to simplify the mba expression.
    """

    def __init__(self):
        
        return None


    def standard_simplify(self, lmbaExpre, vnumber):
        """simplify the linear MBA expression based on the standard basis.
        Arg:
            lmbaExpre: line MBA expression.
            vnumber: the number of variables in the mba expression.
        Return:
            mbaExpre: the related simplified MBA expression.
        """
        self.vnumber = vnumber
        #get standard basis
        lmbaObj = LinearMBA(self.vnumber)
        self.standardBitList = lmbaObj.standardBitList
        self.nonstandardBitList = lmbaObj.nonstandardBitList

        #get the related truth table
        truthtable = truthtable_expression(lmbaExpre, self.vnumber)
        #truthtable can be optimized to one term or constant
        refineList = refine_res_truthtable(truthtable, self.vnumber)
        if refineList[0]:
            mbaExpre = refineList[1]
            #verification
            """
            z3res = verify_mba_unsat(lmbaExpre, mbaExpre)
            if not z3res:
                print("error in simplify MBA expression by standard basis.")
                sys.exit(0)
            """
            return mbaExpre

        #get the term on simplified expression
        termList = []
        for (idx, coe) in enumerate(truthtable):
            bit = self.standardBitList[idx]
            if coe > 0:
                coe = "+" + str(coe)
            elif coe < 0:
                coe = str(coe)
            else:
                continue
            term = coe + "*" + bit
            termList.append(term)
        #construct simplified MBA expression
        mbaExpre = "".join(termList)
        if mbaExpre[0] == "+":
            mbaExpre = mbaExpre[1:]
         
        """
        #verification
        z3res = verify_mba_unsat(lmbaExpre, mbaExpre)
        if not z3res:
            print("error in simplify MBA expression.")
            sys.exit(0)
        """

        return mbaExpre


    def nonstandard_simplify(self, lmbaExpre, vnumber, nonstandardBasis):
        """simplify the linear MBA expression based on the non-standard basis
        Arg:
            lmbaExpre: line MBA expression.
            vnumber: the number of variables in the mba expression.
            nonstandardBasis: non-standard basis used to simplify the mba expression.
        Return:
            mbaExpre: the related simplified MBA expression.
        """
        self.vnumber = vnumber
        self.nonstandardBasis = nonstandardBasis
        if not self.nonstandardBasis:
            print("must input the non-standard basis")
            sys.exit(0)
        #get the related truth table
        truthtable = truthtable_expression(lmbaExpre, self.vnumber)
        #truthtable can be optimized to one term or constant
        refineList = refine_res_truthtable(truthtable, self.vnumber)
        if refineList[0]:
            mbaExpre = refineList[1]
            """
            #verification
            z3res = verify_mba_unsat(lmbaExpre, mbaExpre)
            if not z3res:
                print("error in simplify MBA expression by non-standard basis.")
                sys.exit(0)
            """
            return mbaExpre

        #get the related vector of the non-standard basis
        nonsVectorList = []
        for bit in self.nonstandardBasis:
            vec = truthtable_bitwise(bit, self.vnumber)
            nonsVectorList.append(vec)

        #process the linear equation system
        A = np.mat(nonsVectorList).T
        b = np.mat(truthtable).T
        resultMatrix = np.linalg.solve(A, b)
        resList = np.array(resultMatrix).reshape(-1,).tolist()
        #if there is factor in the member of resultMatrix, the result expression will be error! This is a big mistake!!!
        resList = [int(number) for number in resList]

        #obtain the standard bitwise result based on the result vector
        termList = []
        for (idx, coe) in enumerate(resList): 
            bit = self.nonstandardBasis[idx]
            if coe < 0:
                coe = str(coe)
            elif coe > 0:
                coe = "+" + str(coe)
            else:
                continue
            term = coe + "*" + bit
            termList.append(term)
        #assemble the mbaExpre
        mbaExpre = "".join(termList)
        if mbaExpre[0] == "+":
            mbaExpre = mbaExpre[1:]


        """
        #verification
        z3res = verify_mba_unsat(lmbaExpre, mbaExpre)
        if not z3res:
            print("non-standard basis cannot be used to simplify linear MBA expression.")
            sys.exit(0)
        """

        return mbaExpre


def refine_res_truthtable(truthtable, vnumber):
    """after get the result vector, refine the result expression to one constant or a term.
    Args:
        truthtable: the result truth table of the mba expression.
        vnumber: the number of the variables.
    Return:
        (True, simExpre): sucessfully refine the result expression.
        (False,): the result expression can't be refined.
    """
    #refine the simplification result
    resultSet = set(truthtable)
    bitList = get_entire_bitwise(vnumber)
    if len(resultSet) == 1:
        coefficient = resultSet.pop()
        #result is 0
        if coefficient == 0:
            #print("vector calculation error!")
            #traceback.print_stack()
            #sys.exit(0)
            return (True, str(0))
        #result is a constant
        else:
            simExpre = str(-1 * coefficient)
            return (True, simExpre)
    elif len(resultSet) == 2 and (0 in resultSet):
        #result is one term
        coefficient = resultSet.pop()
        if coefficient == 0:
            coefficient = resultSet.pop()
            if coefficient == 0:
                print("vector calculation error!", sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno)
                traceback.print_stack()
                sys.exit(0)
        index = 0
        for i in range(len(truthtable)):
            if truthtable[i]:
                index += 2**i
        simExpre = str(coefficient) + "*" + bitList[index]
        return (True, simExpre)
    else:
        return (False, )


def simplify_dataset(datafile, standard=True):
    """simplify the expression storing in the file.
    Args:
        datafile: the file storing linear MBA expression.
        standard: flag of simplification method.
    Return:
        None
    """
    if standard:
        filewrite = "{source}.svector.standard.simplify.txt".format(source=datafile)
    else:
        filewrite = "{source}.svector.non-standard.simplify.txt".format(source=datafile)

    fw = open(filewrite, "w")
    print("complex,groundtruth,simplified,z3flag", file=fw)

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
                simExpre1 = svObj.standard_simplify(cmbaExpre, vnumber)
                simExpre2 = svObj.standard_simplify(groundtruth, vnumber)
                print("z3 solving...")
                #z3res = verify_mba_unsat(groundtruth, simExpre)
                z3res = verify_mba_unsat(simExpre1, simExpre2)
                print(linenum, cmbaExpre, groundtruth, simExpre1, simExpre2, z3res)
                print("z3 solved: ", z3res)
                print(cmbaExpre, groundtruth, simExpre1, simExpre2, z3res, sep=",", file=fw)

    fw.close()
    return None


def main(fileread):
    simplify_dataset(fileread)
    #simplify_dataset(fileread, False)



if __name__ == "__main__":
    fileread = sys.argv[1]
    main(fileread)



