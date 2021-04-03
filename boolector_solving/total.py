#!/usr/bin/python3

import re
import sys
import time



def total_simplify(smtsolver, solver):
    """count the solving number after solving by smt solver.
    """
    true = 0
    false = 0
    timeout = 0

    if "mba" in solver:
        path = "../dataset"
        dataFile = ["linear", "poly", "nonpoly"]
        for data in dataFile:
            fileread = "{path}/pldi_dataset_{data}_MBA.txt.simplify.txt.{smtsolver}.verify.64bit.after.simplify.txt".format(path=path, data=data, smtsolver=smtsolver)
            with open(fileread, "r") as fr:
                for line in fr:
                    line = line.strip().replace(" ", "")
                    if "#" not in line:
                        expreStrList = re.split(",", line)
                        flag = expreStrList[4]
                        if "ue" in flag:
                            true += 1
                        elif "out" in flag:
                            timeout += 1
                        else:
                            false += 1
    elif "sspam" in solver:
        path = "../sspam"
        dataFile = ["linear", "poly", "nonpoly"]
        for data in dataFile:
            fileread = "{path}/{data}.MBA.SSPAM.result.txt.{smtsolver}.verify.64bit.after.simplify.txt".format(path=path, data=data, smtsolver=smtsolver)
            with open(fileread, "r") as fr:
                for line in fr:
                    line = line.strip().replace(" ", "")
                    if "#" not in line:
                        expreStrList = re.split(",", line)
                        flag = expreStrList[3]
                        if "ue" in flag:
                            true += 1
                        elif "out" in flag:
                            timeout += 1
                        else:
                            false += 1
    elif "syntia" in solver:
        path = "../syntia"
        dataFile = ["linear", "poly", "nonpoly"]
        for data in dataFile:
            fileread = "{path}/{data}.64bit.result.txt.{smtsolver}.verify.64bit.after.simplify.txt".format(path=path, data=data, smtsolver=smtsolver)
            with open(fileread, "r") as fr:
                for line in fr:
                    line = line.strip().replace(" ", "")
                    if "#" not in line:
                        expreStrList = re.split(",", line)
                        flag = expreStrList[3]
                        if "ue" in flag:
                            true += 1
                        elif "out" in flag:
                            timeout += 1
                        else:
                            false += 1
    total = true+false+timeout
    print("Total: ", total)
    print("True: ", true)
    print("False: ", false)
    print("Timeout: ", timeout)

    return None     
                        


def total_original(smtsolver):
    """count the solving number before solving by smt solver.
    """
    true = 0
    false = 0
    timeout = 0


    path = "../dataset"
    dataFile = ["linear", "poly", "nonpoly"]
    for data in dataFile:
        fileread = "{path}/pldi_dataset_{data}_MBA.txt.{smtsolver}.verify.64bit.before.simplify.txt".format(path=path, data=data, smtsolver=smtsolver)
        with open(fileread, "r") as fr:
            for line in fr:
                line = line.strip().replace(" ", "")
                if "#" not in line:
                    expreStrList = re.split(",", line)
                    flag = expreStrList[2]
                    if "ue" in flag:
                        true += 1
                    elif "out" in flag:
                        timeout += 1
                    else:
                        false += 1
    total = true+false+timeout
    print("Total: ", total)
    print("True: ", true)
    print("False: ", false)
    print("Timeout: ", timeout)

    return None    





def main(smtsolver, flag, solver=None):
    if flag:
        #after simplification
        total_simplify(smtsolver, solver)
    else:
        #before simplification
        total_original(smtsolver)



if __name__ =="__main__":
    #smt solver
    smtsolver = sys.argv[1]
    #before/after simplification
    flag = int(sys.argv[2])
    #if simplificationn, tools
    if len(sys.argv) > 3:
        solver = sys.argv[3]
        main(smtsolver, flag, solver)
    else:
        main(smtsolver, flag)


