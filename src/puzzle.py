from copy import deepcopy
from queue import PriorityQueue
from time import time

class PositionMatrix:
    # CONSTANT ATTRIBUTE
    nRow = 4
    nCol = 4
    moveDir = {"UP" : (-1, 0), "RIGHT" : (0, 1), "DOWN" : (1, 0), "LEFT" : (0, -1)}

    # STATIC ATTRIBUTE
    visitedNodes = []

    # STATIC METHOD
    def getEmptyMatrix():
        matrix = [[None for j in range(PositionMatrix.nCol)] for i in range(PositionMatrix.nRow)]

        return matrix
    
    def fromFile(rawString):
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
        matrix = []

        listOfRow = rawString.split('\n')

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

                    matrix.append(temp)

        PM = PositionMatrix(matrix)

        return PM

    # CONSTRUCTOR
    def __init__(self, data):

        # INITIALIZE matrix
        self.matrix = data

        # INITIALIZE prevPosition
        self.prevPosition = None

        # INITIALIZE nextPosition
        self.nextPosition = {}

        # INITIALIZE currentCost
        self.currentCost = 0

        # INITIALIZE currentLength
        self.currentLength = 0

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

        return (i + j) % 2

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
        return self.currentCost + self.currentLength

    def isReachable(self):
        return (self.getSumKurang() + self.getX()) % 2 == 0

    # OPERATOR OVERLOADING
    def __eq__(self, other):
        for i in range(PositionMatrix.nRow):
            for j in range(PositionMatrix.nCol):
                if (self.matrix[i][j] != other.matrix[i][j]):
                    return False
        return True

    def __lt__(self, other):
        return self.getTotalCost() <= other.getTotalCost()

    def __lshift__(self, move):
        # ADD matrix
        other = PositionMatrix(deepcopy(self.matrix))

        i, j = other.getIndexKosong()
        deltaX, deltaY = PositionMatrix.moveDir[move]

        other.matrix[i][j], other.matrix[i + deltaX][j + deltaY] = other.matrix[i + deltaX][j + deltaY], other.matrix[i][j]

        if other not in PositionMatrix.visitedNodes:
            # ADD prevPosition
            other.prevPosition = self

            # ADD nextPosition
            self.nextPosition[move] = other

            # ADD currentCost
            N = 1
            for i in range(PositionMatrix.nRow):
                for j in range(PositionMatrix.nCol):
                    other.currentCost = other.currentCost + 1 if other.matrix[i][j] != N and other.matrix[i][j] != PositionMatrix.nRow * PositionMatrix.nCol else other.currentCost
                    N += 1

            # ADD currentLength
            other.currentLength = self.currentLength + 1

            # ADD visitedNodes
            PositionMatrix.visitedNodes.append(other)

            return other

        else:
            return None


class PositionTree:
    # STATIC ATTRIBUTE
    move = ["UP", "RIGHT", "DOWN", "LEFT"]
    targetPosition = PositionMatrix([[PositionMatrix.nRow * i + j + 1 for j in range(PositionMatrix.nCol)] for i in range(PositionMatrix.nRow)])

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

            print(("ROOT", rootNode.getStringMatrix())) # REMOVE THIS

            Q.put(rootNode)
            PositionMatrix.visitedNodes.append(rootNode)

            currentNode = None

            while not Q.empty():
                currentNode = Q.get()

                if currentNode == PositionTree.targetPosition:
                    Q.queue.clear()

                else:
                    for move in PositionTree.move:
                        try:
                            childNode = currentNode << move

                            if childNode is not None:
                                print((move, childNode.getTotalCost(), childNode.getStringMatrix())) # REMOVE THIS

                                Q.put(childNode)

                        except IndexError:
                            pass

            if currentNode is None:
                raise Exception("Puzzle tidak dapat diselesaikan!")

            else:
                result = []

                while currentNode is not None:
                    result.insert(0, currentNode)
                    currentNode = currentNode.prevPosition

                return result

    def calculate(self):
        startTime = time()
        PT = self.branchAndBound()
        endTime = time()

        N = len(PositionMatrix.visitedNodes)
        PositionMatrix.visitedNodes = []

        return (PT, N, endTime - startTime)

if __name__ == "__main__":
    try:
        file = open("test/bisa2.txt")
        PM = PositionMatrix.fromFile(file.read())
        file.close()

        T = PositionTree(PM)
        listOfNode, N, time = T.calculate()
        
        print()
        for node in listOfNode:
            print(node.getStringMatrix())

        print()
        print(f"Jumlah simpul yang dibangkitkan : {N}")
        print(f"Lama eksekusi : {time} s")

    except Exception as e:
        print(e)