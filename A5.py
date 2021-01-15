import re
import tools

def homographDetector(strings, nonAsciiStrings, database):
    sig2 = []
    sig3 = []
    sig4 = []
    for string in nonAsciiStrings:
        stringReport2 = string + ": "
        stringReport3 = string + ": "
        stringReport4 = string + ": "
        for i in range(0, len(string)):
            current = string[i]
            if not current.isascii():
                stringReport2 = stringReport2 + current + "[" + str(i) + "]"
                if current in database:
                    stringReport2 = stringReport2 + "[Sig2] "
                else:
                    stringReport2 = stringReport2 + " "
                previous = ""
                next = ""
                if i != 0:
                    previous = string[i - 1]
                if i != len(string) - 1:
                    next = string[i + 1]
                if current in database:
                    if previous != "" and previous.isascii() or next != "" and next.isascii():
                        stringReport3 = string + ": " + current + "[" + str(i) + "]" + "[Sig3] "
                        sig3.append(stringReport3 + "\n")

                if current in database:
                    if previous in database:
                        previous = database[previous]
                    if next in database:
                        next = database[next]
                    homographicString = previous + database[current] + next
                    for originalString in strings:
                        if originalString.count(homographicString) > 0:
                            stringReport4 = string + ": " + current + "[" + str(
                                i) + "]" + "[Sig4] (" + originalString + ")"
                            sig4.append(stringReport4 + "\n")
        sig2.append(stringReport2 + "\n")
    return sig2, sig3, sig4



def detectCmp(code):
    cmpkeccak = re.compile(
        "keccak256\(abi\.encode(?:Packed)?\(.*\)\)[\t\n\r ]*[=!]=[\t\n\r ]*keccak256\(abi\.encode(?:Packed)?\(.*\)\)")
    cmpripemd = re.compile(
        "ripemd160\(abi\.encode(?:Packed)?\(.*\)\)[\t\n\r ]*[=!]=[\t\n\r ]*ripemd160\(abi\.encode(?:Packed)?\(.*\)\)")
    keccak = cmpkeccak.findall(code)
    ripemd = cmpripemd.findall(code)
    return len(keccak)+len(ripemd)>0

def evaluate(sourceCode, homographDatabase):
    result = []

    strings = []
    nonAsciiStrings = []
    for string in re.findall(r"\"[^\"]*\"", sourceCode):
        string = string[1:-1].replace("\n", "")
        strings.append(string)
        if not string.isascii():
            nonAsciiStrings.append(string)
    if nonAsciiStrings:
        sig2, sig3, sig4 = homographDetector(strings, nonAsciiStrings,
                                             homographDatabase)  # siguatures are used for analyzing the sourceCode
        result.extend(sig3)
        result.extend(sig4)

    literals=[]
    startFun, endFun, funNames = tools.detectFunction(sourceCode)
    funCmp={}
    for i in range(len(funNames)):
        funCmp[funNames[i]]=detectCmp(sourceCode[startFun[i]:endFun[i]])
    startIf,endIf=tools.detectCondition(sourceCode)
    for i in range(len(startIf)):
        start=startIf[i]
        end=endIf[i]
        if(detectCmp(sourceCode[start:end])):
            result.append(sourceCode[start-3:end+1]+"\n")
        for literal in re.findall(r"\"[^\"]*\"", sourceCode[start:end]):
            literals.append(literal)
        for name in funNames:
            if sourceCode[start:end].find(name)>-1 and funCmp[name]:
                result.append(sourceCode[start-3:end+1]+"    "+name+'\n')

    return result,literals

