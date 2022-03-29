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
                self.currentCost = self.currentCost + 1 if self.matrix[i][j] != N and self.matrix[i][j] != PositionMatrix.nRow * PositionMatrix.nCol else self.currentCost
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

    def getTotalLength(self):
        if self.prevPosition is None:
            return 0
        
        else:
            return 1 + self.prevPosition.getTotalLength()

    def getTotalCost(self):
        return self.currentCost + self.getTotalLength()

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
        return self.getTotalCost() < other.getTotalCost()

class PositionTree:
    # STATIC ATTRIBUTE
    moveDirection = {"UP" : (-1, 0), "RIGHT" : (0, 1), "DOWN" : (1, 0), "LEFT" : (0, -1)}

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
            visitedNodes = []

            Q.put(rootNode)
            visitedNodes.append(rootNode)

            # print(("ROOT", rootNode.getTotalCost(), rootNode.getStringMatrix())) # REMOVE THIS

            currentNode = None

            while not Q.empty():
                currentNode = Q.get()

                if currentNode == PositionTree.getTargetPosition():
                    Q.queue.clear() # BUG ANTARA CLEAR SEMUA LIVE NODE ATAU KILL NODE YANG MEMILIKI TOTAL COST > CURRENTNODE

                else:
                    for move in PositionTree.moveDirection.keys():
                        try:
                            i, j = currentNode.getIndexKosong()
                            deltaX, deltaY = PositionTree.moveDirection[move]

                            newMatrixString = currentNode.getStringMatrix()
                            newMatrixString[i][j], newMatrixString[i + deltaX][j + deltaY] = newMatrixString[i + deltaX][j + deltaY], newMatrixString[i][j]

                            newData = ""

                            for k in range(PositionMatrix.nRow):
                                if k != PositionMatrix.nRow - 1:
                                    newData = newData + " ".join(newMatrixString[k]) + "\n"
                                else:
                                    newData = newData + " ".join(newMatrixString[k])

                            childNode = PositionMatrix(newData)

                            childNode.prevPosition = currentNode
                            currentNode.nextPosition[move] = childNode

                            if childNode not in visitedNodes:
                                # print((move, childNode.getTotalCost(), childNode.getStringMatrix())) # REMOVE THIS

                                visitedNodes.append(childNode)
                                Q.put(childNode)

                        except IndexError:
                            pass

            if currentNode is None:
                raise Exception("Puzzle tidak dapat diselesaikan!")

            else:
                result = []

                while currentNode is not None:
                    result.append(currentNode)
                    currentNode = currentNode.prevPosition

                return result

if __name__ == "__main__":
    try:
        file = open("test/bisa2.txt")
        data = file.read()
        file.close()

        PM = PositionMatrix(data)
        print(PM.getSumKurang() + PM.getX())
        print()

        T = PositionTree(PM)
        result = T.branchAndBound()
        result.reverse()
        
        for node in result:
            print(node.getStringMatrix())

    except Exception as e:
        print(e)