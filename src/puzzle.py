from queue import PriorityQueue
from copy import deepcopy

class PositionMatrix:
    # STATIC ATTRIBUTE
    nRow = 4
    nCol = 4

    # CONSTRUCTOR
    def __init__(self, data):
        # INITIALIZE legalElement
        legalElement = []
        N = 1

        for i in range(PositionMatrix.nRow):
            for j in range(PositionMatrix.nCol):
                if N != PositionMatrix.nRow * PositionMatrix.nCol:
                    legalElement.append(str(N))
                    N += 1
                else:
                    legalElement.append("-")

        # INITIALIZE matrix
        self.matrix = []

        listOfRow = data.split('\n')

        if len(listOfRow) != PositionMatrix.nRow:
            raise Exception(f"Jumlah baris pada file txt harus berjumlah 4! Jumlah baris pada file adalah {len(listOfRow)}.")

        else:
            for row in listOfRow:
                listOfElement = row.split(" ")

                if len(listOfElement) != PositionMatrix.nCol:
                    raise Exception(f"Jumlah kolom pada file txt harus berjumlah 4! Terdapat kolom pada file dengan jumlah {len(row)}.")

                else:
                    temp = []
                    for element in listOfElement:
                        if element not in legalElement:
                            raise Exception(f"Terdapat elemen ilegal pada file txt! Elemen ilegal tersebut adalah \"{element}\".")

                        else:
                            legalElement.remove(element)
                            temp.append(int(element) if element.isnumeric() else PositionMatrix.nRow * PositionMatrix.nCol)

                    self.matrix.append(temp)

        # INITIALIZE prevPosition
        self.prevPosition = None

        # INITIALIZE nextPosition
        self.nextPosition = {}

        # INITIALIZE currentCost
        self.currentCost = 0
        N = 1

        for i in range(PositionMatrix.nRow):
            for j in range(PositionMatrix.nCol):
                self.currentCost = self.currentCost + 1 if self.matrix[i][j] != N else self.currentCost
                N += 1

    # OPERATION
    def getKurang(self, N):
        nilaiKurang = -1

        for i in range(PositionMatrix.nRow):
            for j in range(PositionMatrix.nCol):
                if self.matrix[i][j] == N:
                    nilaiKurang = 0
                else:
                    nilaiKurang = nilaiKurang + 1 if nilaiKurang != -1 and self.matrix[i][j] < N else nilaiKurang

        if nilaiKurang == -1:
            if N != PositionMatrix.nRow * PositionMatrix.nCol:
                raise Exception(f"Tidak terdapat elemen \"{N}\" pada matrix!")

            else:
                raise Exception("Tidak terdapat elemen kosong pada matrix!")
            
        else:
            return nilaiKurang

    def getSumKurang(self):
        nilaiSumKurang = 0
        N = 1

        for i in range(PositionMatrix.nRow):
            for j in range(PositionMatrix.nCol):
                nilaiSumKurang += self.getKurang(N)
                N += 1

        return nilaiSumKurang

    def getIndexKosong(self):
        for i in range(PositionMatrix.nRow):
            for j in range(PositionMatrix.nCol):
                if self.matrix[i][j] == PositionMatrix.nRow * PositionMatrix.nCol:
                    return (i, j)

        raise Exception("Tidak terdapat elemen kosong pada matrix!")

    def getX(self):
        i, j = self.getIndexKosong()

        return (i + j) % 2 == 0

    def getStringMatrix(self):
        stringMatrix = []

        for i in range(PositionMatrix.nRow):
            temp = []

            for j in range(PositionMatrix.nCol):
                if self.matrix[i][j] != PositionMatrix.nRow * PositionMatrix.nCol:
                    temp.append(str(self.matrix[i][j]))

                else:
                    temp.append("-")

            stringMatrix.append(temp)

        return stringMatrix

    def getTotalCost(self):
        if self.prevPosition == None:
            return self.currentCost
        
        else:
            return self.currentCost + self.prevPosition.getTotalCost()

    def isReachable(self):
        return (self.getSumKurang() + self.getX()) % 2 == 0

    # OPERATOR OVERLOADING
    def __eq__(self, other):
        for i in range(PositionMatrix.nRow):
            for j in range(PositionMatrix.nCol):
                if (self.matrix[i][j] != other.matrix[i][j]):
                    return False

        return True

class PositionTree:
    # STATIC ATTRIBUTE
    moveDirection = {"BOTTOM" : (1, 0), "LEFT" : (0, -1), "UP" : (-1, 0), "RIGHT" : (0, 1)}

    # STATIC METHOD
    def getTargetPosition():
        N = 1
        data = ""

        for i in range(PositionMatrix.nRow):
            temp = []

            for j in range(PositionMatrix.nCol):
                if N != PositionMatrix.nRow * PositionMatrix.nCol:
                    temp.append(str(N))
                    N += 1
                else:
                    temp.append("-")

            if i != PositionMatrix.nRow - 1:
                data = data + " ".join(temp) + "\n"
            else:
                data = data + " ".join(temp)

        return PositionMatrix(data)

    # CONSTRUCTOR
    def __init__(self, first):
        self.first = first

    # OPERATION
    def branchAndBound(self):
        rootNode = self.first
        
        if not rootNode.isReachable():
            raise Exception("Puzzle tidak dapat diselesaikan!")

        else:
            Q = PriorityQueue()

            Q.put((rootNode.getTotalCost(), rootNode))

            while not Q.empty():
                currentNode = Q.get()

                for move in PositionTree.moveDirection.keys():
                    try:
                        newNode = deepcopy(currentNode)

                    except IndexError:
                        pass

if __name__ == "__main__":
    try:
        data = "1 2 3 4\n5 6 - 8\n9 10 7 11\n13 14 15 12"
        PM = PositionMatrix(data)
        print(PM.getStringMatrix())

        T = PositionTree(PM)
        print(T.branchAndBound())

    except Exception as e:
        print(e)