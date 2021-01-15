import A1
import A2
import A3
import A4
import A5
import A6_A7
import tools
import sys



homographDatabase = tools.loadDatabase("Database/homograph_database.txt")

sourceCode = tools.preprocessing(sys.argv[1])

result= A1.evaluate(sourceCode)
if result:
    print("A1 Suspicious")
    for line in result:
        print(line)
else:
    print("A1 Benign")

result= A2.evaluate(sourceCode)
if result:
    print("A2 Suspicious")
    for line in result:
        print(line)
else:
    print("A2 Benign")

result=A3.evaluate(sourceCode)
if result:
    print("A3 Suspicious")
    for line in result:
        print(line)
else:
    print("A3 Benign")

result = A4.evaluate(sourceCode)
if result:
    print("A4 Suspicious")
    for line in result:
        print(line)
else:
    print("A4 Benign")

result,_= A5.evaluate(sourceCode, homographDatabase)
if result:
    print("A5 Suspicious")
    for line in result:
        print(line)
else:
    print("A5 Benign")

result= A6_A7.evaluate(sourceCode)
if result:
    print("A6,A7 Suspicious")
    for line in result:
        print(line)
else:
    print("A6,A7 Benign")