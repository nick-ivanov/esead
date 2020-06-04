import re

import tools


def findConstant(addressList, sourceCode):
    tokens = [value for value in re.split(r"(?:[ ;\t\b\n\r=])", sourceCode) if value != ""]
    for i in range(0, len(tokens)):
        token = tokens[i]
        pos = token.find("0x")
        if pos != -1 and token[pos:pos + 42] in addressList:
            if tokens[i - 2] == "constant":
                return True
    return False


def evaluate(sourceCode):
    addressList = tools.findAddresses(sourceCode)

    if addressList and findConstant(addressList, sourceCode) and sourceCode.find("emit") != -1:
        sequentialTransfer, count1, count2 = tools.detectTransfer(sourceCode)
        if sequentialTransfer:
            return True
    return False
