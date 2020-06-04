import re

import tools


def findVariables(addressList, code):
    variableList = []
    tokens = [value for value in re.split(r"(?:[ ()!;\t\b\n\r=])", code) if value != ""]
    for i in range(0, len(tokens)):
        token = tokens[i]
        pos = token.find("0x")
        if pos != -1 and token[pos:pos + 42] in addressList:
            variable = tokens[i - 1]
            if variable not in variableList:
                address = token[pos:pos + 42]
                cmpHard = re.compile("%s[\t\n\r ]*=[\t\n\r ]*%s[\t\n\r ]*;" % (re.escape(variable), re.escape(address)))
                hard = cmpHard.findall(code)
                if hard:
                    variableList.append(variable)
    return variableList


def findAssign(code, start, end, variableList):
    assignedVariables = []
    for k in range(0, len(start)):
        functionCode = code[start[k]:end[k]]
        for variable in variableList:
            cmpAssign = re.compile("[\t\n\r( ]%s[\t\n\r ]*=[\t\n\r ]*[^;]*;" % re.escape(variable))
            assign = cmpAssign.findall(functionCode)
            if assign:
                assignedVariables.append(variable)
    return assignedVariables


def evaluate(sourceCode):
    addressList = tools.findAddresses(sourceCode)
    if addressList:
        variableList = findVariables(addressList, sourceCode)
        if variableList:
            startFun, endFun, _ = tools.detectFunction(sourceCode)
            assignedVariables = findAssign(sourceCode, startFun, endFun, variableList)
            conditionVariable = []
            for variable in assignedVariables:
                cmpCondition = re.compile("if[\t\n\r ]*[(][^;]*[=\t\n\r( ]%s[^;]*[)][^;]*;" % re.escape(variable))
                condition = cmpCondition.findall(sourceCode)
                if condition and variable not in conditionVariable:
                    conditionVariable.append(variable)
            if conditionVariable:
                return True
    return False
