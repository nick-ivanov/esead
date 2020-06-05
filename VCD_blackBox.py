from ethereum.utils import check_checksum

import tools


def findLowerCase(addressList):
    total = len(addressList)
    lower = 0
    valid = 0
    validList = []
    for address in addressList:
        if address == address.lower():
            lower = lower + 1
            if check_checksum(address):
                valid = valid + 1
                validList.append(address + '\n')
    return validList, total, lower, valid


def evaluate(sourceCode):
    addressList = tools.findAddresses(sourceCode)
    validList, total, lower, valid = findLowerCase(addressList)
    return lower, valid
