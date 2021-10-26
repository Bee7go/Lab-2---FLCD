import re

class Pair:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def getValue(self):
        return self.value

    def setValue(self, newValue):
        self.value = newValue

    def getKey(self):
        return self.key

    def setKey(self, newKey):
        self.key = newKey


class AlphabeticallySortedST:

    def __init__(self):
        self.list = []

    # returns the position of the key if it already exists in our sorted symbol table and -1 otherwise
    def checkIfElementExists(self, pair):
        for i in range(len(self.list)):
            if self.list[i].getKey() > pair.getKey():
                return -1
            if self.list[i].getKey() == pair.getKey():
                return self.list[i].getValue()
        return -1

    # adds new element in the table (if the key doesn't exists already)  so that the list keeps it's sorted property
    # returns -1 if element doesn't exist and it's dictionary value otherwise
    def addElement(self, token):
        pair = Pair(token, len(self.list)+1)
        for i in range(len(self.list)):
            if self.list[i].getKey() == pair.getKey():
                return
            if self.list[i].getKey() > pair.getKey():
                self.list.insert(i, pair)
                return
        self.list.append(pair)

    # returns the alphabetically sorted symbol table
    def getList(self):
        return self.list


class Scanner:
    def __init__(self, problem):
        self.problem = problem
        self.symbolTable = AlphabeticallySortedST()
        self.line = []
        self.lineCount = -1
        self.tokenCount = -1
        self.prevToken = 0
        self.pif = []

    def __iter__(self):
        return self

    def genPIF(self, classification, token, index):
        pair = Pair(token, index)
        self.pif.append([classification, pair])

    def getPIF(self):
        return self.pif

    def detectNextToken(self):
        while not len(self.line):
            self.line = self.problem.readline()
            if not self.line:
                return 0
            self.line = self.line.split()
            self.lineCount += 1
            self.tokenCount = -1
        self.tokenCount += 1
        currentToken = self.line.pop(0)
        return currentToken

    def codifyToken(self, currentToken):
        pair = Pair(currentToken, 0)
        if self.symbolTable.checkIfElementExists(pair) != -1:
            return 1

        with open("files/token.in") as f:
            for line in f:
                splitedLine = line.split()
                if currentToken == splitedLine[0]:
                    return int(splitedLine[1])

        #check if identifier
        if re.match("^([a-zA-Z_$][a-zA-Z\\d_$]*)$", currentToken):
            if 3 <= self.prevToken <= 8 or self.prevToken == 10:
                self.symbolTable.addElement(currentToken)
                return 1

        #check if constant
        if currentToken == 'yes' or currentToken == 'no' or currentToken.isdigit() or \
                (currentToken.startswith('-') and currentToken[1:].isdigit()) or \
            (currentToken.startswith("[[") and currentToken.endswith("]]")) \
                or (currentToken.startswith("'") and currentToken.endswith("'")) \
            or (currentToken.startswith("\"") and currentToken.endswith("\"")):
            self.symbolTable.addElement(currentToken)
            return 2
        return -1

    def classifyCodification(self, code):
        if code == 1:
            return 'identifier'
        if code == 2:
            return 'constant'
        if 3 <= code <= 15:
            return 'reserved-word'
        if 16 <= code <= 24:
            return 'operator'
        if 25 <= code <= 26:
            return 'separator'
        return 'lexical error'


if __name__ == '__main__':
    myScanner = Scanner(open("files/p1.in"))
    currentToken = myScanner.detectNextToken()
    error = 0
    while currentToken:
        tokenClassified = myScanner.classifyCodification(myScanner.codifyToken(currentToken))
        if tokenClassified == 'lexical error':
            print("LEXICAL ERROR AT LINE " + str(myScanner.lineCount) + ' TOKEN ' + str(myScanner.tokenCount))
            error = 1
        if tokenClassified == 'reserved-word' or tokenClassified == 'operator' or tokenClassified == 'separator':
            myScanner.genPIF(tokenClassified,currentToken, 0)
        else:
            if tokenClassified == 'identifier' or tokenClassified == 'constant':
                pair = Pair(currentToken, 0)
                myScanner.genPIF(tokenClassified, currentToken, myScanner.symbolTable.checkIfElementExists(pair))
        myScanner.prevToken = myScanner.codifyToken(currentToken)
        currentToken = myScanner.detectNextToken()

    f = open("files/ST.out", "w")
    for element in myScanner.symbolTable.getList():
        f.write(element.getKey() + ' ' + str(element.getValue()) + '\n')
    f.close()

    f = open("files/PIF.out", "w")
    for el in myScanner.pif:
        f.write(el[0] + ' ' + el[1].getKey() + ' ' + str(el[1].getValue()) + '\n')
    f.close()

    if not error:
        print("LEXICALLY CORRECT")