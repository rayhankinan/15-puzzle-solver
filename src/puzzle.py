from queue import PriorityQueue
from time import time

import numpy as np

class PositionMatrix:
    # CONSTANT ATTRIBUTE
    nRow = 4
    nCol = 4
    moveDir = {"UP" : (-1, 0), "RIGHT" : (0, 1), "DOWN" : (1, 0), "LEFT" : (0, -1)}

    # STATIC ATTRIBUTE
    visitedNodes = {}

    # STATIC METHOD
    def getEmptyMatrix():
        matrix = np.array([[None for j in range(PositionMatrix.nCol)] for i in range(PositionMatrix.nRow)])

        return matrix
    
    def fromFile(rawString):
        # INITIALIZE legalElement
        legalElement = [str(i) for i in range(1, PositionMatrix.nRow * PositionMatrix.nCol + 1)]

        # INITIALIZE matrix
        matrix = np.empty((PositionMatrix.nRow, PositionMatrix.nCol), int)

        listOfRow = rawString.split("\r\n")

        if len(listOfRow) != PositionMatrix.nRow:
            raise Exception(f"Jumlah baris pada file txt harus berjumlah 4! Jumlah baris pada file adalah {len(listOfRow)}.")

        else:
            for i in range(len(listOfRow)):
                listOfElement = listOfRow[i].split(" ")

                if len(listOfElement) != PositionMatrix.nCol:
                    raise Exception(f"Jumlah kolom pada file txt harus berjumlah 4! Terdapat kolom pada file dengan jumlah {len(listOfElement)}.")

                else:
                    for j in range(len(listOfElement)):
                        if listOfElement[j] not in legalElement:
                            raise Exception(f"Terdapat elemen ilegal pada file txt! Elemen ilegal tersebut adalah \"{listOfElement[j]}\".")

                        else:
                            legalElement.remove(listOfElement[j])
                            matrix[i, j] = int(listOfElement[j])

            PM = PositionMatrix(matrix)

            if not PM.isReachable():
                raise Exception(f"Puzzle tidak dapat diselesaikan! (SUM KURANG + X = {PM.getSumKurang() + PM.getX()})")

            else:
                return PM

    # CONSTRUCTOR
    def __init__(self, data):

        # INITIALIZE matrix
        self.matrix = data

        # INITIALIZE prevPosition
        self.prevPosition = None

        # INITIALIZE currentCost
        self.currentCost = 0

        # INITIALIZE currentLength
        self.currentLength = 0

        # INITIALIZE indexKosong
        self.indexKosong = (-1, -1)

    # OPERATION
    def getKurang(self, N):
        nilaiKurang = -1

        for i in range(PositionMatrix.nRow):
            for j in range(PositionMatrix.nCol):
                if self.matrix[i, j] == N:
                    nilaiKurang = 0
                else:
                    nilaiKurang = nilaiKurang + 1 if nilaiKurang != -1 and self.matrix[i, j] < N else nilaiKurang

        if nilaiKurang == -1:
            if N != PositionMatrix.nRow * PositionMatrix.nCol:
                raise Exception(f"Tidak terdapat elemen \"{N}\" pada matrix!")

            else:
                raise Exception("Tidak terdapat elemen kosong pada matrix!")
            
        else:
            return nilaiKurang

    def getSumKurang(self):
        nilaiSumKurang = 0

        for i in range(PositionMatrix.nRow):
            for j in range(PositionMatrix.nCol):
                nilaiSumKurang += self.getKurang(PositionMatrix.nRow * i + j + 1)

        return nilaiSumKurang

    def getIndexKosong(self):
        for i in range(PositionMatrix.nRow):
            for j in range(PositionMatrix.nCol):
                if self.matrix[i, j] == PositionMatrix.nRow * PositionMatrix.nCol:
                    return (i, j)

        raise Exception("Tidak terdapat elemen kosong pada matrix!")

    def getPerbedaanUbin(self):
        N = 0
        
        for i in range(PositionMatrix.nRow):
            for j in range(PositionMatrix.nCol):
                if self.matrix[i, j] != PositionMatrix.nRow * i + j + 1 and self.matrix[i, j] != PositionMatrix.nRow * PositionMatrix.nCol:
                    N += 1

        return N

    def getX(self):
        i, j = self.getIndexKosong()

        return (i + j) % 2

    def getStringMatrix(self):
        return self.matrix.astype(str)

    def getTotalCost(self):
        return self.currentCost + self.currentLength

    def isReachable(self):
        return (self.getSumKurang() + self.getX()) % 2 == 0

    # OPERATOR OVERLOADING
    def __eq__(self, other):
        return self.matrix.tobytes() == other.matrix.tobytes()

    def __lt__(self, other):
        return self.getTotalCost() <= other.getTotalCost()

    def __lshift__(self, move):
        i, j = self.indexKosong
        deltaX, deltaY = PositionMatrix.moveDir[move]

        if i + deltaX < 0 or i + deltaX >= PositionMatrix.nRow or j + deltaY < 0 or j + deltaY >= PositionMatrix.nCol:
            raise IndexError("Invalid move.")
        
        else:
            # ADD matrix
            other = PositionMatrix(self.matrix.copy())

            isPrevValid = other.matrix[i + deltaX, j + deltaY] == PositionMatrix.nRow * (i + deltaX) + (j + deltaY) + 1
            other.matrix[i, j], other.matrix[i + deltaX, j + deltaY] = other.matrix[i + deltaX, j + deltaY], other.matrix[i, j]
            isFollowingValid = other.matrix[i, j] == PositionMatrix.nRow * i + j + 1

            if other.matrix.tobytes() in PositionMatrix.visitedNodes:
                return None

            else:
                # ADD prevPosition
                other.prevPosition = self

                # ADD currentCost
                if isPrevValid and not isFollowingValid:
                    other.currentCost = self.currentCost + 1
                elif not isPrevValid and isFollowingValid:
                    other.currentCost = self.currentCost - 1
                else:
                    other.currentCost = self.currentCost

                # ADD currentLength
                other.currentLength = self.currentLength + 1

                # ADD indexKosong
                other.indexKosong = (i + deltaX, j + deltaY)

                # ADD visitedNodes
                PositionMatrix.visitedNodes[other.matrix.tobytes()] = other

                return other

class PositionTree:
    # CONSTANT ATTRIBUTE
    move = ["UP", "RIGHT", "DOWN", "LEFT"]
    targetPosition = PositionMatrix(np.array([[PositionMatrix.nRow * i + j + 1 for j in range(PositionMatrix.nCol)] for i in range(PositionMatrix.nRow)]))

    # CONSTRUCTOR
    def __init__(self, first):
        if not first.isReachable():
            raise Exception(f"Puzzle tidak dapat diselesaikan! (SUM KURANG + X = {first.getSumKurang() + first.getX()})")

        else:
            self.first = first
            self.first.currentCost = self.first.getPerbedaanUbin()
            self.first.indexKosong = self.first.getIndexKosong()

    # OPERATION
    def branchAndBound(self):
        rootNode = self.first
    
        Q = PriorityQueue()

        Q.put(rootNode)
        PositionMatrix.visitedNodes[rootNode.matrix.tobytes()] = rootNode
        
        # print(len(PositionMatrix.visitedNodes), "-") # REMOVE THIS

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
                            # print(len(PositionMatrix.visitedNodes), childNode.getTotalCost()) # REMOVE THIS

                            Q.put(childNode)

                    except IndexError:
                        pass

        result = []
        while currentNode is not None:
            result.insert(0, currentNode)
            currentNode = currentNode.prevPosition

        return result

    def calculate(self):
        PositionMatrix.visitedNodes = {}

        sumKurangPlusX = self.first.getSumKurang() + self.first.getX()

        startTime = time()
        rawPath = self.branchAndBound()
        endTime = time()

        pathOfStringMatrix = map(lambda T : T.getStringMatrix(), rawPath)

        numOfNodes = len(PositionMatrix.visitedNodes)
        PositionMatrix.visitedNodes = {}

        executionTime = endTime - startTime

        return (sumKurangPlusX, pathOfStringMatrix, numOfNodes, executionTime)

if __name__ == "__main__":
    try:
        file = open("test/lama3.txt", "rb")
        PM = PositionMatrix.fromFile(file.read().decode("ASCII"))
        file.close()

        T = PositionTree(PM)
        sumKurangPlusX, listOfNode, N, time = T.calculate()
        
        print()
        jumlahSolusi = 0
        for node in listOfNode:
            print(node)
            jumlahSolusi += 1

        print()
        print(f"Panjang solusi : {jumlahSolusi}")
        print(f"Jumlah simpul yang dibangkitkan : {N}")
        print(f"Lama eksekusi : {time} s")

    except Exception as e:
        print(e)