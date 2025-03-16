import keyboard
import pyautogui
import auto_script as auto
import variables_script as var

board = auto.board
possibilities = [[[] for _ in range(9)] for _ in range(9)]

def print_board():
    for row in board:
        print(row)

def same_cell(i1, j1, i2, j2):
    return i1 // 3 == i2 // 3 and j1 // 3 == j2 // 3

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

def update_possible(i, j, num):
    for k in range(9):
        if k != j and num in possibilities[i][k]:
            possibilities[i][k].remove(num)
        if k != i and num in possibilities[k][j]:
            possibilities[k][j].remove(num)

    start_row, start_col = 3 * (i // 3), 3 * (j // 3)
    for m in range(3):
        for n in range(3):
            if ((start_row + m != i or start_col + n != j)
                    and num in possibilities[start_row + m][start_col + n]):
                possibilities[start_row + m][start_col + n].remove(num)

def update_twin(i1, j1, i2, j2, num1, num2, type_t):
    possibilities[i1][j1] = [num1, num2]
    possibilities[i2][j2] = [num1, num2]

    if type_t == 1:
        for k in range(9):
            if k != j1 and k != j2 and num1 in possibilities[i1][k]:
                possibilities[i1][k].remove(num1)
            if k != j1 and k != j2 and num2 in possibilities[i1][k]:
                possibilities[i1][k].remove(num2)

    if type_t == 2:
        for k in range(9):
            if k != i1 and k != i2 and num1 in possibilities[k][j1]:
                possibilities[k][j1].remove(num1)
            if k != i1 and k != i2 and num2 in possibilities[k][j1]:
                possibilities[k][j1].remove(num2)

    if same_cell(i1, j1, i2, j2):
        start_row, start_col = 3 * (i1 // 3), 3 * (j1 // 3)
        for m in range(3):
            for n in range(3):
                if (start_row + m != i1 or start_col + n != j1) and (start_row + m != i2 or start_col + n != j2):
                    if num1 in possibilities[start_row + m][start_col + n]:
                        possibilities[start_row + m][start_col + n].remove(num1)
                    if num2 in possibilities[start_row + m][start_col + n]:
                        possibilities[start_row + m][start_col + n].remove(num2)

def find_twin(i, j, num1, num2):
    s1, s2, s3 = True, True, True
    f1, f2, f3 = False, False, False
    i_t, j_t = -1, -1

    for k in range(9):
        if k != j and ((num1 in possibilities[i][k] and not num2 in possibilities[i][k])
                       or (num2 in possibilities[i][k] and not num1 in possibilities[i][k])
                       or (num1 in possibilities[i][k] and num2 in possibilities[i][k] and f1)):
            s1 = False

        if k != i and ((num1 in possibilities[k][j] and not num2 in possibilities[k][j])
                       or (num2 in possibilities[k][j] and not num1 in possibilities[k][j])
                       or (num1 in possibilities[k][j] and num2 in possibilities[k][j] and f2)):
            s2 = False

        if k != j and num1 in possibilities[i][k] and num2 in possibilities[i][k]:
            f1 = True
            i_t = i
            j_t = k

        if k != i and num1 in possibilities[k][j] and num2 in possibilities[k][j]:
            f2 = True
            i_t = k
            j_t = j

    start_row, start_col = 3 * (i // 3), 3 * (j // 3)
    for m in range(3):
        for n in range(3):
            if (start_row + m == i and start_col + n == j) or board[start_row + m][start_col + n] != 0:
                continue

            if ((num1 in possibilities[start_row + m][start_col + n] and not num2 in possibilities[start_row + m][start_col + n])
                    or (num2 in possibilities[start_row + m][start_col + n] and not num1 in possibilities[start_row + m][start_col + n])
                    or (num1 in possibilities[start_row + m][start_col + n] and num2 in possibilities[start_row + m][start_col + n] and f3)):
                s3 = False
                break

            if num1 in possibilities[start_row + m][start_col + n] and num2 in possibilities[start_row + m][start_col + n]:
                i_t = start_row + m
                j_t = start_col + n
                f3 = True

    type_t = 0
    if f1 and s1:
        type_t = 1

    if f2 and s2:
        type_t = 2

    if (f1 and s1) or (f2 and s2) or (f3 and s3):
        return i_t, j_t, type_t

    return -1, -1, -1

def find_perfect_twin(i, j, num1, num2):
    if len(possibilities[i][j]) != 2:
        return -1, -1, -1

    for k in range(9):
        if k != j and num1 in possibilities[i][k] and num2 in possibilities[i][k] and len(possibilities[i][k]) == 2:
            return i, k, 1
        if k != i and num1 in possibilities[k][j] and num2 in possibilities[k][j] and len(possibilities[k][j]) == 2:
            return k, j, 2

    start_row, start_col = 3 * (i // 3), 3 * (j // 3)
    for m in range(3):
        for n in range(3):
            if (start_row + m != i or start_col + n != j) and num1 in possibilities[start_row + m][start_col + n] and num2 in possibilities[start_row + m][start_col + n] and len(possibilities[start_row + m][start_col + n]) == 2:
                return start_row + m, start_col + n, 0

    return -1, -1, -1

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
                            i_t, j_t, t_t = find_perfect_twin(i, j, num1, num2)
                            if i_t != -1 and (i < i_t or (i == i_t and j < j_t)):
                                # print("perf: ", i, j, "and", i_t, j_t, ":", num1, num2, t_t)
                                update_twin(i, j, i_t, j_t, num1, num2, t_t)

                            i_t, j_t, t_t = find_twin(i, j, num1, num2)
                            if i_t != -1 and (i < i_t or (i == i_t and j < j_t)):
                                print(i, j, "and", i_t, j_t, ":", num1, num2, t_t)
                                update_twin(i, j, i_t, j_t, num1, num2, t_t)

def initialise_possible():
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                possibilities[i][j] = [num for num in range(1, 10) if is_valid(i, j, num)]

                if len(possibilities[i][j]) == 1:
                    set_cell(i, j, possibilities[i][j][0])

def solve():
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

    return board  # Returns updated board