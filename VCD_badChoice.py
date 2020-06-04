import re


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


def evaluate(sourceCode, homographDatabase):
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
        if sig3:  # We use sig3 to detect the bad choice attack.
            return True
    return False
