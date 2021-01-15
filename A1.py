import re

import tools


def findPublic(addressList, sourceCode):
    flag = False
    varList = []

    tokens = [value for value in re.split(r"(?:[ ;\t\b\n\r=])", sourceCode) if value != ""]
    for i in range(0, len(tokens)):
        token = tokens[i]
        pos = token.find("0x")
        if pos != -1 and token[pos:pos + 42] in addressList:
            if tokens[i - 2] == "public":
                varList.append(tokens[i - 1])
                flag = True
    return flag, varList


def findAssign(sourceCode, varName):
    pos = sourceCode.find(varName, 0)
    pos = sourceCode.find(varName, pos + 1)
    while pos != -1:
        next = pos + len(varName)
        while sourceCode[next] == " ":
            next += 1
        if sourceCode[next] == "=" and sourceCode[next + 1] != "=":
            return True
        pos = sourceCode.find(varName, next + 1)
    return False


def evaluate(sourceCode):
    flag = False
    addressList = tools.findAddresses(sourceCode)
    if addressList:
        flagPublic, varNames = findPublic(addressList, sourceCode)
        if flagPublic:
            for varName in varNames:
                if findAssign(sourceCode, varName):
                    flag = True
    if flag:
        sequentialTransfer, count1, count2 = tools.detectTransfer(sourceCode)
        return sequentialTransfer
    return []
