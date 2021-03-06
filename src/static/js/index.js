let board, zx, zy

const getPossibles = (nRow, nCol) => {
    let ii, jj, cx = [-1, 0, 1, 0], cy = [0, -1, 0, 1]
    possibles = []

    for (let i = 0; i < 4; i++) {
        ii = zx + cx[i]
        jj = zy + cy[i]

        if (ii >= 0 && ii < nRow && jj >= 0 && jj < nCol) {
            possibles.push({ x: ii, y: jj })
        }
    }

    return possibles
}

const updateBtns = (nRow, nCol) => {
    for (let i = 0; i < nRow; i++) {
        for (let j = 0; j < nCol; j++) {
            const id = `btn${i * nCol + j}`

            if (board[i][j] < nRow * nCol) {
                $(`#${id}`).html(board[i][j])
                $(`#${id}`).attr("class", "button")

            } else {
                $(`#${id}`).html("")
                $(`#${id}`).attr("class", "empty")
            }
        }
    }
}

const btnHandle = (event) => {
    let p = -1

    const c = event.target.i, r = event.target.j, nRow = event.target.nRow, nCol = event.target.nCol
    const possibles = getPossibles(nRow, nCol)

    for (let i = 0; i < possibles.length; i++) {
        if (possibles[i].x == c && possibles[i].y == r) {
            p = i
            break
        }
    }

    if (p > -1) {
        const t = possibles[p]

        board[zx][zy] = board[t.x][t.y]
        zx = t.x
        zy = t.y
        board[zx][zy] = nRow * nCol
        
        updateBtns(nRow, nCol)
    }
}

const createBoard = (newBoard, nRow, nCol) => {
    board = new Array(nRow)

    for (let i = 0; i < nRow; i++) {
        board[i] = new Array(nCol)
        for (let j = 0; j < nCol; j++) {
            if (newBoard[i][j] == nRow * nCol) {
                zx = i
                zy = j
            }

            board[i][j] = newBoard[i][j]
        }
    }
}

const createBtns = (nRow, nCol) => {
    for (let i = 0; i < nRow; i++) {
        for (let j = 0; j < nCol; j++) {
            const b = document.createElement("button")
            
            b.id = `btn${i * nCol + j}`
            b.i = i
            b.j = j
            b.nRow = nRow
            b.nCol = nCol

            $(b).click((event) => {
                btnHandle(event)
            })

            $(b).appendTo(".board")
        }
    }
}

$(document).ready(() => {
    $.ajax({
        type: "GET",
        url: "/display",
        contentType:"application/json; charset=utf-8",
        async: true,
        error: (jqXHR) => {
            alert(jqXHR.responseText)
        },
        success: (data) => {
            createBtns(data.nRow, data.nCol)
            createBoard(data.matrix, data.nRow, data.nCol)
            updateBtns(data.nRow, data.nCol)
        }
    })

    $(".submission-form").submit((event) => {
        const formData = new FormData(event.target)

        $.ajax({
            data: formData,
            type: "POST",
            url: "/upload_txt",
            contentType: false,
            processData: false,
            async: true,
            error: (jqXHR) => {
                alert(jqXHR.responseText)
            },
            success: () => {
                window.location.reload()
            }
        })
    })

    $(".calculate-button").click(() => {
        $.ajax({
            type: "POST",
            url: "/upload_json",
            async: true,
            data: JSON.stringify(board),
            contentType: "application/json",
            error: (jqXHR) => {
                alert(jqXHR.responseText)
            },
            success: () => {
                window.location.replace("/view")
            }
        })
    })
})