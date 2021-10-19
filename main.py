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

    #returns the position of the key if it already exists in our sorted symbol table and -1 otherwise
    def checkIfElementExists(self, pair):
        for i in range(len(self.list)):
            if self.list[i].getKey() <= pair.getKey():
                if self.list[i].getKey() == pair.getKey():
                    return i
            else:
                return -1

    # adds new element in the table (if the key doesn't exists already)  so that the list keeps it's sorted property
    # returns -1 if element doesn't exist and it's position in list otherwise
    def addElement(self, pair):
        for i in range(len(self.list)):
            if self.list[i].getKey() == pair.getKey():
                return
            if self.list[i].getKey() > pair.getKey():
                self.list.insert(i, pair)
                return
        # in case our list is empty:
        self.list.append(pair)


    #returns the alphabetically sorted symbol table
    def getList(self):
        return self.list


class Scanner:
    def detectNextToken(self):
        return

    def classifyToken(self):
        return

    def codifyToken(self):
        return



if __name__ == '__main__':
    #TEST:
    elem1 = Pair('a', '100')
    elem2 = Pair('b', '200')
    elem3 = Pair('d', '250')
    elem4 = Pair('x', '50')
    elem5 = Pair('b', '950')
    mySortedList = AlphabeticallySortedST()
    mySortedList.addElement(elem3)
    mySortedList.addElement(elem4)
    mySortedList.addElement(elem2)
    mySortedList.addElement(elem1)
    mySortedList.addElement(elem5)
    for element in mySortedList.getList():
        print(element.getKey())
    print(mySortedList.checkIfElementExists(elem3))

