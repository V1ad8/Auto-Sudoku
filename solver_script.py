import pyautogui
import auto_script as auto
import variables_script as var
import possible_script as fill

board = [[6, 9, 0, 1, 0, 0, 3, 0, 0],
[0, 0, 0, 0, 7, 0, 0, 0, 0],
[0, 3, 0, 2, 0, 8, 5, 0, 0],
[0, 4, 6, 0, 0, 0, 8, 3, 2],
[1, 2, 8, 0, 3, 6, 0, 0, 0],
[0, 0, 0, 0, 2, 0, 1, 0, 6],
[0, 5, 1, 7, 6, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 2, 5, 0],
[2, 8, 0, 0, 0, 9, 6, 1, 3]]

def print_board(board):
    for row in board:
        print(row)

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

def update_possible(possible, i, j, num):
    for k in range(9):
        if num in possible[i][k]:
            possible[i][k].remove(num)
        if num in possible[k][j]:
            possible[k][j].remove(num)

    start_row, start_col = 3 * (i // 3), 3 * (j // 3)
    for m in range(3):
        for n in range(3):
            if num in possible[start_row + m][start_col + n]:
                possible[start_row + m][start_col + n].remove(num)

def lone_possible(possible, i, j, num):
    p1, p2, p3 = True, True, True

    for k in range(9):
        if k != j and num in possible[i][k]:
            p1 = False
        if k != i and num in possible[k][j]:
            p2 = False

    if p1 or p2:
        return True

    start_row, start_col = 3 * (i // 3), 3 * (j // 3)
    for m in range(3):
        for n in range(3):
            if (m != i or n != j) and num in possible[start_row + m][start_col + n]:
                p3 = False
                return p1 or p2
            
    return p1 or p2 or p3

def set_cell(board, possible, i, j, num):
    board[i][j] = num
    update_possible(possible, i, j, num)

    possible[i][j] = []

    pyautogui.moveTo(var.get_cords(j) + (var.cell_size // 2) + var.left_start, var.get_cords(i) + (var.cell_size // 2) + var.top_start)
    pyautogui.click()

    pyautogui.write(str(num))

def solve(board):
    possibilities = [[[] for _ in range(9)] for _ in range(9)]

    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                possibilities[i][j] = [num for num in range(1, 10) if is_valid(board, i, j, num)]

                if len(possibilities[i][j]) == 1:
                    set_cell(board, possibilities, i, j, possibilities[i][j][0])

                
    while True:
        updated = False

        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    if len(possibilities[i][j]) == 1:
                        set_cell(board, possibilities, i, j, possibilities[i][j][0])
                        updated = True

                    for num in possibilities[i][j]:
                        if lone_possible(possibilities, i, j, num):
                            set_cell(board, possibilities, i, j, num)
                            updated = True

        if not updated:
            break

    print(possibilities)

    if fill.has_empty(board):
        fill.fill_possible(possibilities)

    return board  # Returns updated board