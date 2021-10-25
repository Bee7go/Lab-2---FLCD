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
            # if self.list[i].getKey() <= pair.getKey():
            if self.list[i].getKey() == pair.getKey():
                return self.list[i].getValue()
            # else:
            #    return -1
        return -1

    # adds new element in the table (if the key doesn't exists already)  so that the list keeps it's sorted property
    # returns -1 if element doesn't exist and it's position in list otherwise
    def addElement(self, token):
        pair = Pair(token, len(self.list)+1)
        for i in range(len(self.list)):
            if self.list[i].getKey() == pair.getKey():
                return
            if self.list[i].getKey() > pair.getKey():
                self.list.insert(i, pair)
                return
        # in case our list is empty:
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

    def genPIF(self, token, index):
        pair = Pair(token, index)
        self.pif.append(pair)

    def getPIF(self):
        return self.pif

    def detectNextToken(self):
        while not len(self.line):
            self.line = self.problem.readline()
            if not self.line:
                return 0
            self.line = self.line.split()
            self.lineCount += 1
        self.tokenCount += 1
        currentToken = self.line.pop(0)
        # self.prevToken = self.classifyToken(currentToken)
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

        if 3 <= self.prevToken <= 8:
            self.symbolTable.addElement(currentToken)
            return 1

        if currentToken == 'yes' or 'no' or currentToken.isnumeric() or (
                currentToken.startsWith("[[") and currentToken.endswith("]]")) \
                or (currentToken.startsWith("'") and currentToken.endsWith("'")):
            self.symbolTable.addElement(currentToken)
            return 2
        return -1

    def classifyCodification(self, code):
        if code == 1:
            return 'identifier'
        if code == 2:
            return 'constant'
        if 3 <= code <= 14:
            return 'reserved-word'
        if 15 <= code <= 23:
            return 'operator'
        if 24 <= code <= 27:
            return 'separator'
        return 'lexical error'


if __name__ == '__main__':
    myScanner = Scanner(open("files/p2.in"))

    currentToken = myScanner.detectNextToken()
    line = 0
    while currentToken:
        #print(currentToken)
        tokenClassified = myScanner.classifyCodification(myScanner.codifyToken(currentToken))
        #print(tokenClassified + ' line:' + str(myScanner.lineCount) + ' token:' + str(myScanner.tokenCount))
        if tokenClassified == 'reserved-word' or tokenClassified == 'operator' or tokenClassified == 'separator':
            myScanner.genPIF(currentToken, 0)
        else:
            if tokenClassified == 'identifier' or tokenClassified == 'constant':
                pair = Pair(currentToken, 0)
                myScanner.genPIF(currentToken, myScanner.symbolTable.checkIfElementExists(pair))
        myScanner.prevToken = myScanner.codifyToken(currentToken)
        currentToken = myScanner.detectNextToken()

    print("- - - - SYMBOL TABLE - - - - - - -")
    f = open("files/ST.out", "w")
    for element in myScanner.symbolTable.getList():
        print(element.getKey() + ' ' + str(element.getValue()))
        f.write(element.getKey() + ' ' + str(element.getValue()) + '\n')
    f.close()

    print("- - - - PIF - - - - - - -")
    f = open("files/PIF.out", "w")
    for el in myScanner.pif:
        print(el.getKey() + ' ' + str(el.getValue()))
        f.write(el.getKey() + ' ' + str(el.getValue()) + '\n')
    f.close()


    # print(myScanner.symbolTable.list)
    # print(myScanner.detectNextToken())
