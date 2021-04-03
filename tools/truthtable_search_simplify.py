#!/usr/bin/python3

"""
simplify the polynomial(may b non-poly) MBA expression by the truth table searching:
    step1: get the entire truth table, then transform it into the linear combination of basis.
    step2: split the MBA expression, replace every bitwise expression with related the related basis.
    step3: simplify the MBA expression into the conbination of basis.
    trick: replace the basis with variable, simplify the MBA expression by the sympy library.
"""

import io
import numpy as np
import re
import sympy
import sys
import time
import traceback
import z3
from mba_string_operation import variable_list, verify_mba_unsat, truthtable_expression, truthtable_bitwise, expression_2_term
from commons import get_entire_bitwise


class PMBASimplify():
    """
    Attributes:
        vnumber: the number of variable in one expression.
        basisList: the basis vector defined by the user.
        truthBasisList: the related truth of the basis vector.
        bitTruthList: transform every one truth into the linear combination of the basis.
        middleNameList: in order to simplify the expression by 
    """

    def __init__(self, vnumber, basisList):
        self.vnumber = vnumber
        self.basisList = basisList
        self.truthBasisList = []
        for bit in self.basisList:
            self.truthBasisList.append(truthtable_bitwise(bit, vnumber))
        #transform bitwise to the combination of basis
        self.bitTruthList = self.bit_2_basis()
        #middle variable
        self.middleNameList = []
        for i in range(2 ** self.vnumber):
            vname = "X{num}".format(num=i)
            self.middleNameList.append(vname)
        
        return None


    def bit_2_basis(self):
        """get entire truth table, create the linear combination of every bitwise expression, just store the coefficient of every term.
        Args:
            None
        Returns:
            bitTruthList: the list of basis on every one bitwise expression.
        """
        bitList = get_entire_bitwise(self.vnumber)
        bitTruthList = []

        A = np.mat(self.truthBasisList).T
        for bit in bitList:
            truth = truthtable_bitwise(bit, self.vnumber)
            b = np.mat(truth).T
            resMatrix = np.linalg.solve(A, b)
            resList = np.array(resMatrix).reshape(-1,).tolist()
            resList = [int(i) for i in resList]
            bitTruthList.append(resList)

        return bitTruthList
        


    def simplify(self, pmbaExpre):
        """simplify the linear MBA expression based on the flag of standard.
        Algorithm:
            step1: split the expression into list of terms.
            step2: for every term, split the term into coeffcient and bitwise expression.
            step3: for the bitwise, transform it into linear combination of middle variable name.
            step4: construct every term into the multiplication of middle variable name.
            step5: goto step2, until loop end.
            step6: apply sympy to simplify the transformation.
            step7: replace the middle variable name with bitwise expression in the simplified expression.
        Arg:
            pmbaExpre: poly MBA expression.
        Return:
            resExpre: the related simplified MBA expression.
        """
        #print(pmbaExpre)
        #split the expression into terms
        termList = expression_2_term(pmbaExpre)
        newtermList = []
        for term in termList:
            #split the term
            itemList = re.split("\*", term)
            #the term is constant
            if len(itemList) == 1:
                if not re.search("[a-z]", itemList[0]):
                    coe = int(itemList[0])
                    if coe < 0:
                        coeStr = "+{coe}".format(coe=abs(coe))
                        itemList = [coeStr, "~(x&~x)"]
                    elif coe > 0:
                        coeStr = "-{coe}".format(coe=coe)
                        itemList = [coeStr, "~(x&~x)"]
            #get the coefficient
            coe = itemList[0]
            if not re.search("\d", coe):
                itemList.insert(0, "")
                if coe[0] == "-":
                    coe = "-1"
                else:
                    coe = "+1"
            bitTransList = []
            #transform every bitwise expression into linear combination of basis
            for bit in itemList[1:]:
                truth = truthtable_bitwise(bit, self.vnumber)
                #get the index of truth table
                index = 0
                for (idx, value) in enumerate(truth):
                    index += value *  2**idx
                #transform the truth table to the related basis
                basisVec = self.bitTruthList[index]
                basisStrList = []
                for (idx, value) in enumerate(basisVec):
                    if value < 0:
                        basisStrList.append(str(value) + "*" + self.middleNameList[idx]) 
                    elif value > 0:
                        basisStrList.append("+" + str(value) + "*" + self.middleNameList[idx]) 
                #construct one bitwise transformation 
                basisStr = "".join(basisStrList)
                if basisStr:
                    if basisStr[0] == "+":
                        basisStr = basisStr[1:]
                    #one bitwise transformation
                    bitTransList.append("({basis})".format(basis=basisStr))
            #not zero 
            if bitTransList:
                #construct the entire term.
                bitTrans = "*".join(bitTransList)
                #contain coefficient
                bitTrans = coe + "*" + bitTrans
                newtermList.append(bitTrans)
        #construct the transformation middle result
        midExpre = "".join(newtermList)
        #print(midExpre)
        #simplify the middle result, but must process the power operator
        resExpre = self.sympy_simplify(midExpre)
        #the result of z3 is unattractive
        #resExpre = self.z3_simplify(midExpre)
        resExpre = resExpre.strip()
        #print(resExpre)
        resExpre = resExpre.replace(" ", "")
        resExpre = self.power_expand(resExpre)
        #print(resExpre)
        #replace the middle variable name with real bitwise expression
        #for (idx, var) in enumerate(self.middleNameList):
        for idx in range(len(self.middleNameList)-1, -1, -1):
            var = self.middleNameList[idx]
            basis = self.basisList[idx]
            resExpre = resExpre.replace(var, basis)

        """
        #verification
        z3res = verify_mba_unsat(pmbaExpre, resExpre)
        if not z3res:
            print("error in simplify MBA expression.")
            sys.exit(0)
        """

        #print(resExpre)
        return resExpre


    def sympy_simplify(self, mbaExpre):
        """simplify the mba expression by the sympy library.
        Args:
            mbaExpre: the mba expression.
        Returns:
            newmbaExpre: the simplified mba expression.
        """
        #variable symbols
        if self.vnumber in [1, 2, 3, 4]:
            X0 = sympy.symbols("X0")
            X1 = sympy.symbols("X1")
            X2 = sympy.symbols("X2")
            X3 = sympy.symbols("X3")
            X4 = sympy.symbols("X4")
            X5 = sympy.symbols("X5")
            X6 = sympy.symbols("X6")
            X7 = sympy.symbols("X7")
            X8 = sympy.symbols("X8")
            X9 = sympy.symbols("X9")
            X10 = sympy.symbols("X10")
            X11 = sympy.symbols("X11")
            X12 = sympy.symbols("X12")
            X13 = sympy.symbols("X13")
            X14 = sympy.symbols("X14")
            X15 = sympy.symbols("X15")
        else:
            print("error in sympy_simplify")
            sys.exit(0)
        #simplify it
        resExpre = sympy.simplify(eval(mbaExpre))
        #output the result to a variable
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        print(resExpre, end="")
        newmbaExpre = new_stdout.getvalue()
        sys.stdout = old_stdout

        return newmbaExpre


    def power_expand(self, mbaExpre):
        """since the sympy simplification expression contains power operator, which is unaccepted by solver,we expand the power operator.
        Args:
            mbaExpre: mba expression.
        Returns:
            newmbaExpre: the expanded mba expression.
        """
        #split the expression by power operator.
        itemList = re.split("(\*\*)", mbaExpre)

        breakFlag = False
        for (idx, item) in enumerate(itemList):
            if r"**" in item:
                #pre/post-item of the power operator
                preStr = itemList[idx - 1]
                postStr = itemList[idx + 1]
                #get the one operand of power operator -- variable name
                splitList = re.split("\*", preStr)
                splitList = re.split("[\+-]", splitList[-1])
                varName = splitList[-1]
                #get the one operand of power operator -- value
                count = ""
                for (i, c) in enumerate(postStr):
                    #the beginning character must be a number
                    if re.search("\d", c):
                        count += c
                    else:
                        breakFlag = True
                        break
                count = int(count)
                #remove the value from the postStr
                if breakFlag:
                    itemList[idx + 1] = itemList[idx + 1][i:]
                    breakFlag = False
                else:
                    itemList[idx + 1] = itemList[idx + 1][i+1:]
                    breakFlag = False
                #expand the power operator
                #the number of 1 is because the preStr have one variable name
                powerList = [varName] * (count - 1)
                powerStr = "*" + "*".join(powerList)
                #replace the power operator with proper expression
                itemList[idx] = powerStr
            else:
                continue

        newmbaExpre = "".join(itemList)

        return newmbaExpre



    def z3_simplify(self, mbaExpre):
        """simplify the mba expression by the z3 library, but the simplification expression is unattractive, we discard it.
        Args:
            mbaExpre: the mba expression.
        Returns:
            newmbaExpre: the simplified mba expression.
        """
        #variable symbols
        if self.vnumber == 1:
            X0 = z3.Int("X0")
            X1 = z3.Int("X1")
        elif self.vnumber == 2:
            X0 = z3.Int("X0")
            X1 = z3.Int("X1")
            X2 = z3.Int("X2")
            X3 = z3.Int("X3")
        elif self.vnumber == 3:
            X4 = z3.Int("X4")
            X5 = z3.Int("X5")
            X6 = z3.Int("X6")
            X7 = z3.Int("X7")
            z3.Int("X0:7")
        elif self.vnumber == 4:
            X8 = z3.Int("X8")
            X9 = z3.Int("X9")
            X10 = z3.Int("X10")
            X11 = z3.Int("X11")
            X12 = z3.Int("X12")
            X13 = z3.Int("X13")
            X14 = z3.Int("X14")
            X15 = z3.Int("X15")
        else:
            print("error in sympy_simplify")
            sys.exit(0)
        #simplify it
        resExpre = z3.simplify(eval(mbaExpre))
        #output the result to a variable
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        print(resExpre, end="")
        newmbaExpre = new_stdout.getvalue()
        sys.stdout = old_stdout

        return newmbaExpre

def simplify_dataset(datafile, vnumber):
    """simplify the expression storing in the file.
    Args:
        datafile: the file storing linear MBA expression.
    Return:
        None
    """
    filewrite = "{source}.truthtable.search.simplify.txt".format(source=datafile)

    fw = open(filewrite, "w")
    print("complex,groundtruth,simplified,z3flag", file=fw)

    if vnumber == 2:
        basisVec = ["x", "y", "(x|y)", "~(x&~x)"]
    else:
        basisVec = ["x", "y", "z", "(x&y)",  "(y&z)", "(x&z)", "(x&y&z)", "~(x&~x)"]
    psObj = PMBASimplify(vnumber, basisVec)
    with open(datafile, "rt") as fr:
        for line in fr:
            if "#" not in line:
                line = line.strip()
                itemList = re.split(",", line)
                cmbaExpre = itemList[0]
                groundtruth = itemList[1]
                simExpre = psObj.simplify(cmbaExpre)
                print("z3 solving...")
                z3res = verify_mba_unsat(groundtruth, simExpre)
                print("z3 solved: ", z3res)
                print(cmbaExpre, groundtruth, simExpre, z3res, sep=",", file=fw)

    fw.close()
    return None

def test():
    """simplify the expression.
    """
    cmbaExpre = "(x&y)*(x|y)+(x&~y)*(~x&y)+1*(((y^~(~x|(y^z)))&~t)|((y^~(x&z))&t))+11*((~(x|y)&~t)|((z&(x^y))&t))-1*((~(x&z)&~t)|((~y|(x^z))&t))-10*~(x|(y|(z|t)))-10*~(x|(y|(~z|t)))+1*(x&(y&(~z&t)))-10*(x&(~y&(z&t)))-1*(x&(y&(z&t)))"
    groundExpre = "x*y+10*(~x&(y&(z&t)))"
    cmbaExpre = "(x&y)*(x|y)+(x&~y)*(~x&y)"
    groundExpre = "x*y"

    
    vnumber = 2
    if vnumber == 1:
        #basisVec = ["x","~(x&~x)"]
        basisVec = ["x","~x"]
    elif vnumber == 2:
        #basisVec = ["x", "y", "(x|y)", "~(x&~x)"]
        basisVec = ["(x&y)", "(~x&y)", "(x&~y)", "(~x&~y)"]
    elif vnumber == 3:
        #basisVec = ["x", "y", "z", "(x&y)",  "(y&z)", "(x&z)", "(x&y&z)", "~(x&~x)"]
        basisVec = ["(x&y&z)", "(~x&y&z)", "(x&~y&z)", "(x&y&~z)",  "(~x&~y&z)", "(~x&y&~z)", "(x&~y&~z)", "(~x&~y&~z)"]
    elif vnumber == 4:
        #basisVec = ["x", "y", "z", "t", "(x&y)",  "(x&z)", "(x&t)", "(y&z)", "(y&t)","(z&t)", "(x&y&z)", "(x&y&t)", "(x&z&t)", "(y&z&t)", "(x&y&z&t)", "~(x&~x)"]
        basisVec = ["(x&y&z&t)", "(~x&y&t&z)", "(x&~y&z&t)", "(x&y&~z&t)", "(x&y&z&~t)",  "(~x&~y&z&t)", "(x&~y&~z&t)", "(x&y&~z&~t)", "(~x&y&~z&t)","(~x&y&z&~t)", "(x&~y&z&~t)", "(x&~y&~z&~t)", "(~x&y&~z&~t)", "(~x&~y&z&~t)", "(~x&~y&~z&t)", "(~x&~y&~z&~t)"]
    psObj = PMBASimplify(vnumber, basisVec)
    simExpre1 = psObj.simplify(cmbaExpre)
    print(cmbaExpre, simExpre1)
    simExpre2 = psObj.simplify(groundExpre)
    print(groundExpre, simExpre2)
    print("z3 solving...")
    z3res = verify_mba_unsat(simExpre1, simExpre2, 8)
    print("z3 solved: ", z3res)
    print(cmbaExpre, groundExpre, simExpre1, simExpre2)


def main(fileread, vnumber):
    simplify_dataset(fileread, vnumber)

    return None



if __name__ == "__main__":
    #fileread = sys.argv[1]
    #vnumber = int(sys.argv[2])
    #main(fileread, vnumber)
    test()



