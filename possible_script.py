import keyboard
import pyautogui
import variables_script as var
import auto_script as auto
import solver_script as solver

board = auto.board
possibilities = solver.possibilities

def has_empty():
    for row in board:
        if 0 in row:
            return True
    return False

def fill_possible():
    pyautogui.moveTo(1100, 300)
    pyautogui.click()

    for i in range(9):
        for j in range(9):
            if not possibilities[i][j]:
                 continue

            if keyboard.is_pressed(auto.KILL_SWITCH):
                print("Stopping solver...")
                break

            pyautogui.moveTo(var.get_cords(j) + (var.cell_size // 2) + var.left_start, var.get_cords(i) + (var.cell_size // 2) + var.top_start)
            pyautogui.click()

            pyautogui.press("delete")
            for num in possibilities[i][j]:
                pyautogui.write(str(num))

    pyautogui.moveTo(1100, 300)
    pyautogui.click()

def clear():
    pyautogui.moveTo(1100, 300)
    pyautogui.click()

    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                continue

            if keyboard.is_pressed(auto.KILL_SWITCH):
                print("Stopping solver...")
                break

            pyautogui.moveTo(var.get_cords(j) + (var.cell_size // 2) + var.left_start,
                             var.get_cords(i) + (var.cell_size // 2) + var.top_start)
            pyautogui.click()

            pyautogui.press("delete")

    pyautogui.moveTo(1100, 300)
    pyautogui.click()