import pyautogui
import auto_script as auto
import variables_script as var

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
    for k in range(9):
        if k != j and num in possible[i][k]:
            return False
        if k != i and num in possible[k][j]:
            return False

    start_row, start_col = 3 * (i // 3), 3 * (j // 3)
    for m in range(3):
        for n in range(3):
            if (m != i or n != j) and num in possible[start_row + m][start_col + n]:
                return False
            
    return True

def set_cell(board, possible, i, j, num):
    board[i][j] = num
    update_possible(possible, i, j, num)

    pyautogui.moveTo(var.get_cords(j) + (var.cell_size // 2) + var.left_start, var.get_cords(i) + (var.cell_size // 2) + var.top_start)
    pyautogui.click()

    pyautogui.write(str(num))

def solve(board):
    possible = [[[] for _ in range(9)] for _ in range(9)]  # Use lists instead of integers

    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                possible[i][j] = [num for num in range(1, 10) if is_valid(board, i, j, num)]

                if len(possible[i][j]) == 1:
                    set_cell(board, possible, i, j, possible[i][j][0])

                
    while True:
        updated = False

        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    if len(possible[i][j]) == 1:
                        set_cell(board, possible, i, j, possible[i][j][0])
                        updated = True

                    for num in possible[i][j]:
                        if lone_possible(possible, i, j, num):
                            set_cell(board, possible, i, j, num)
                            updated = True

        if not updated:
            break

    return board  # Returns updated board