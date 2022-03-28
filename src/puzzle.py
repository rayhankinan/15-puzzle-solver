class PositionMatrix:
    def __init__(self, data):
        self.matrix = []

        listOfRow = data.split('\n')

        if len(listOfRow) != 4:
            raise Exception(f"Jumlah baris pada file txt harus berjumlah 4! Jumlah baris pada file adalah {len(listOfRow)}.")

        else:
            for row in listOfRow:
                if len(row) != 4:
                    raise Exception(f"Jumlah kolom pada file txt harus berjumlah 4! Terdapat kolom pada file dengan jumlah {len(row)}.")

                else:
                    temp = []
                    for element in row.split(" "):
                        temp.append(int(element) if element.isnumeric() else None)
                    self.matrix.append(temp)

if __name__ == "__main__":
    data = "1 2 3 4\n5 6 7 8\n9 10 11 12\n13 14 15 -\n"

    PM = PositionMatrix(data)

    print(PM.matrix)