import VCD_badChoice
import VCD_blackBox
import VCD_eavesdropper
import VCD_nameCalling
import VCD_spittingImage
import VCD_unfairShare
import tools
import sys

homographDatabase = tools.loadDatabase("Database/homograph_database.txt")

contractName=sys.argv[1]

sourceCode = tools.preprocessing(contractName)

if VCD_badChoice.evaluate(sourceCode, homographDatabase):
    print("Bad Choice")

if VCD_nameCalling.evaluate(sourceCode):
    print("Name Calling")

if VCD_unfairShare.evaluate(sourceCode):
    print("Unfair Share")

if VCD_eavesdropper.evaluate(sourceCode):
    print("Eavesdropper")

if VCD_spittingImage.evaluate(sourceCode):
    print("Spitting Image")

lower, valid = VCD_blackBox.evaluate(sourceCode)
if valid > 0:
    print("Black Box: valid lower case EIP-55 address")
if valid == 0 and lower > 0:
    print("Black Box: invalid lower case EIP-55 address")
