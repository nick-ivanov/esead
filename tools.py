import numpy as np


def loadDatabase(filename):
    f = open(filename, "r")
    homographDatabase = {}
    for line in f.readlines():
        nonAsciiChar, asciiChar = line.replace("\n", "").split(" ")
        homographDatabase[nonAsciiChar] = asciiChar
    return homographDatabase


def preprocessing(filename):
    f = open(filename, 'r')
    source_code = f.read()
    return removeComments(source_code)


def removeComments(sourceCode):
    length = len(sourceCode)
    isCode = [True for _ in range(0, length)]
    comment = False
    for i in range(0, len(sourceCode)):

        if comment:
            isCode[i] = False
        if i > 0 and not comment:
            if sourceCode[i] == "/" and sourceCode[i - 1] == "/":
                comment = True
                commentType = "//"
                isCode[i - 1] = False
                isCode[i] = False
            elif sourceCode[i] == "*" and sourceCode[i - 1] == "/" and (i <= 1 or sourceCode[i - 2] != "*"):
                comment = True
                commentType = "/*"
                isCode[i - 1] = False
                isCode[i] = False
        if i > 1 and comment:
            if commentType == "//" and sourceCode[i] == "\n" or sourceCode[i] == "/" and sourceCode[i - 1] == "*":
                comment = False
            elif commentType == "/*" and sourceCode[i] == "/" and sourceCode[i - 1] == "*":
                comment = False

    newSourceCode = ""
    for i in range(0, length):
        if isCode[i]:
            newSourceCode = newSourceCode + sourceCode[i]
    return newSourceCode


def findAddresses(code):
    hexList = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'D',
               'E', 'F']
    addressList = []
    for token in code.split(" "):
        start = token.find("0x")
        if start != -1 and len(token) - start >= 42:
            end = ""
            if len(token) - start > 42:
                end = token[start + 42]
            address = token[start:start + 42]
            isAddress = True
            if end in hexList:
                isAddress = False
            index = 2
            while isAddress and index < 42:
                if address[index] not in hexList:
                    isAddress = False
                index = index + 1
            if isAddress:
                addressList.append(address)
    return addressList


def detectFunction(code):
    starts = []
    ends = []
    names = []
    pos = code.find(" function", 0)
    while pos != -1:
        ns = pos + 8
        while code[ns] == " ":
            ns = ns + 1
        ne = ns
        while code[ne] != " " and code[ne] != "(":
            ne = ne + 1
        name = code[ns:ne]

        start = ne + 1
        flag = True
        while code[start] != "{":
            start = start + 1
            if code[start] == ";":
                flag = False
                break
        end = start
        if flag:
            brace = 1
            while brace != 0:
                end = end + 1
                if code[end] == "{":
                    brace = brace + 1
                if code[end] == "}":
                    brace = brace - 1
            names.append(name)
            starts.append(start)
            ends.append(end)
        pos = code.find(" function", end + 1)
    return starts, ends, names


def DFS(origin, vertex, funNum, connection, adjMatrix):
    for i in range(0, funNum):
        if connection[origin][i] == 0 and adjMatrix[vertex][i] == 1:
            connection[origin][i] = 1
            DFS(origin, i, funNum, connection, adjMatrix)


def searchConnection(k, funNum, connection, adjMatrix):
    DFS(k, k, funNum, connection, adjMatrix)


def findtransfer(remaining, code):
    c1 = code.find(".send(", remaining)
    c2 = code.find(".transfer(", remaining)
    if c1 == -1:
        pos = c2
    elif c2 == -1:
        pos = c1
    else:
        pos = min(c1, c2)
    return pos


def detectTransfer(code):
    starts, ends, names = detectFunction(code)
    funNum = len(names)
    adjMatrix = np.zeros((funNum, funNum))

    for k in range(0, funNum):
        start = starts[k]
        end = ends[k]
        subcode = code[start:end + 1]
        for i in range(0, funNum):
            if subcode.find(names[i] + "(") > -1:
                adjMatrix[k][i] = 1

    transfers = []
    for k in range(0, funNum):
        start = starts[k]
        end = ends[k]
        transfer = []
        subcode = code[start:end + 1]
        pos = findtransfer(0, subcode)
        while pos != -1:
            ts = pos
            while ts > 0 and subcode[ts] != " " and subcode[ts] != "\n" and subcode[ts] != "(" and subcode[ts] != "\t":
                ts = ts - 1
            te = pos
            while te < len(subcode) - 1 and subcode[te] != ")":
                te = te + 1
            transfer.append(subcode[ts + 1:te + 1])
            pos = findtransfer(te + 1, subcode)
        transfers.append(transfer)
    count1 = 0
    count2 = 0
    sequentialTransfer = []
    connection = np.zeros((funNum, funNum))
    for k in range(0, funNum):
        searchConnection(k, funNum, connection, adjMatrix)
    for k in range(0, funNum):
        if transfers[k] != []:
            for i in range(0, len(transfers[k]) - 1):
                if transfers[k][i].count(".transfer(") > 0:
                    for j in range(i + 1, len(transfers[k])):
                        name1 = transfers[k][i][0:transfers[k][i].rfind(".")]
                        name2 = transfers[k][j][0:transfers[k][j].rfind(".")]
                        if name1 != name2:
                            sequentialTransfer.append("Sig1: " + transfers[k][i] + " --> " + transfers[k][j] + '\n')
                            count1 = count1 + 1
    for k in range(0, funNum):
        if transfers[k] != []:
            for i in range(0, funNum):
                if transfers[i] != [] and connection[k][i] > 0:
                    for t1 in transfers[k]:
                        if t1.count(".transfer(") > 0:
                            for t2 in transfers[i]:
                                name1 = t1[0:t1.rfind(".")]
                                name2 = t2[0:t2.rfind(".")]
                                if name1 != name2:
                                    sequentialTransfer.append("Sig2: " + t1 + " --> " + t2 + '\n')
                                    count2 = count2 + 1
    return sequentialTransfer, count1, count2
