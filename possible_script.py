import pyautogui
import variables_script as var

def has_empty(board):
    for row in board:
        if 0 in row:
            return True
    return False

def fill_possible(possible):

    pyautogui.moveTo(1100, 300)
    pyautogui.click()

    for i in range(9):
            for j in range(9):
                pyautogui.moveTo(var.get_cords(j) + (var.cell_size // 2) + var.left_start, var.get_cords(i) + (var.cell_size // 2) + var.top_start)
                pyautogui.click()

                for num in possible[i][j]:
                    pyautogui.write(str(num))

    pyautogui.moveTo(1100, 300)
    pyautogui.click()