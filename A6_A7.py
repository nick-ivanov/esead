import re


def findcall(remaining, sourceCode):
    calls = []
    calls.append(sourceCode.find(".call(", remaining))
    calls.append(sourceCode.find(".delegatecall(", remaining))
    calls.append(sourceCode.find(".encodeWithSignature(", remaining))
    pos = 2147483647
    for pMin in calls:
        if pMin > -1 and pMin < pos:
            pos = pMin
    if pos == 2147483647:
        return -1
    else:
        return pos


def evaluate(sourceCode):
    nonAsciiCalls = []
    pos = findcall(0, sourceCode)
    while pos != -1:
        start = pos + 4
        while sourceCode[start] != "(":
            start = start + 1
        stack = 1
        end = start
        while stack != 0:
            end = end + 1
            if sourceCode[end] == "(":
                stack = stack + 1
            if sourceCode[end] == ")":
                stack = stack - 1
        strings = re.findall(r"\"[^\"]*\"", sourceCode[start:end])
        for string in strings:
            if not string.isascii():
                nonAsciiCalls.append(string + "is non-ASCII in a function call\n")
        pos = findcall(end + 1, sourceCode)
    return nonAsciiCalls
