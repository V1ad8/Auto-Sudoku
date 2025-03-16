import keyboard
import pyautogui
import auto_script as auto
import variables_script as var
import possible_script as fill

board = auto.board
possibilities = [[[] for _ in range(9)] for _ in range(9)]

def print_board():
    for row in board:
        print(row)

def is_valid(row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

def update_possible(i, j, num, except_i = -1, except_j = -1):
    for k in range(9):
        if k != j and k != except_j and num in possibilities[i][k]:
            possibilities[i][k].remove(num)
        if k != i and k != except_i and num in possibilities[k][j]:
            possibilities[k][j].remove(num)

    start_row, start_col = 3 * (i // 3), 3 * (j // 3)
    for m in range(3):
        for n in range(3):
            if ((start_row + m != i or start_col + n != j)
                    and (start_row + m != except_i or start_col + n != except_j)
                    and num in possibilities[start_row + m][start_col + n]):
                possibilities[start_row + m][start_col + n].remove(num)

def find_perfect_twin(i, j, num1, num2):
    if len(possibilities[i][j]) != 2:
        return -1, -1

    for k in range(9):
        if k != j and num1 in possibilities[i][k] and num2 in possibilities[i][k] and len(possibilities[i][k]) == 2:
            return i, k
        if k != i and num1 in possibilities[k][j] and num2 in possibilities[k][j] and len(possibilities[k][j]) == 2:
            return k, j

    start_row, start_col = 3 * (i // 3), 3 * (j // 3)
    for m in range(3):
        for n in range(3):
            if (start_row + m != i or start_col + n != j) and num1 in possibilities[start_row + m][start_col + n] and num2 in possibilities[start_row + m][start_col + n] and len(possibilities[start_row + m][start_col + n]) == 2:
                return start_row + m, start_col + n

    return -1, -1

def lone_possible(i, j, num):
    p1, p2, p3 = True, True, True

    for k in range(9):
        if k != j and num in possibilities[i][k]:
            p1 = False
        if k != i and num in possibilities[k][j]:
            p2 = False

    if p1 or p2:
        return True

    start_row, start_col = 3 * (i // 3), 3 * (j // 3)
    for m in range(3):
        for n in range(3):
            if (m != i or n != j) and num in possibilities[start_row + m][start_col + n]:
                p3 = False
                return p1 or p2
            
    return p1 or p2 or p3

def set_cell(i, j, num):
    board[i][j] = num
    update_possible(i, j, num)

    possibilities[i][j] = []

    pyautogui.moveTo(var.get_cords(j) + (var.cell_size // 2) + var.left_start, var.get_cords(i) + (var.cell_size // 2) + var.top_start)
    pyautogui.click()

    pyautogui.write(str(num))

def find_and_update_twins():
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for num1 in possibilities[i][j]:
                    for num2 in possibilities[i][j]:
                        if num1 < num2:
                            i_t, j_t = find_perfect_twin(i, j, num1, num2)
                            if i_t != -1 and (i < i_t or (i == i_t and j < j_t)):
                                print(i, j, "and", i_t, j_t, ":", num1, num2)
                                update_possible(i, j, num1, i_t, j_t)
                                update_possible(i, j, num2, i_t, j_t)

def solve():
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                possibilities[i][j] = [num for num in range(1, 10) if is_valid(i, j, num)]

                if len(possibilities[i][j]) == 1:
                    set_cell(i, j, possibilities[i][j][0])

    while True:
        updated = False

        for i in range(9):
            for j in range(9):
                if keyboard.is_pressed(auto.KILL_SWITCH):
                    print("Stopping solver...")
                    break

                if board[i][j] == 0:
                    if len(possibilities[i][j]) == 1:
                        set_cell(i, j, possibilities[i][j][0])
                        updated = True

                    for num in possibilities[i][j]:
                        if lone_possible(i, j, num):
                            set_cell(i, j, num)
                            updated = True

        if not updated:
            break

    find_and_update_twins()

    if fill.has_empty(board):
        fill.fill_possible(possibilities)

    return board  # Returns updated board