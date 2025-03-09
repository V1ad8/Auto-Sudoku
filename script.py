from time import sleep
import mss
import numpy as np
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\2004u\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
import pyautogui

top_start = 217
left_start = 370
big_border = 2
small_border = 1
cell_size = 54

error = 3

def capture_screen():
    width = 9 * cell_size + 4 * big_border + 6 * small_border

    with mss.mss() as sct:
        monitor = {"top": top_start, "left": left_start, "width": width, "height": width}
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # Convert to BGR format

def get_cords(i):
    coords = [3, 58, 113, 168, 223, 279, 334, 388, 444]
    return coords[i]
    # return i * (cell_size + small_border) + 3

def load_templates():
    templates = {}
    for num in range(10):
        path = f"templates/{num}.png"
        templates[num] = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    return templates

# Compare a cell against all templates and return the best-matching digit
def match_digit(cell, templates):
    best_match = 0
    best_score = float("inf")

    for num, template in templates.items():
        diff = cv2.absdiff(cell, template)  # Get absolute difference
        score = np.sum(diff)  # Sum of pixel differences (lower is better)

        if score < best_score:
            best_score = score
            best_match = num

    return best_match

def extract_digits_from_board(board_img):
    templates = load_templates()
    board = [[0 for _ in range(9)] for _ in range(9)]

    for i in range(9):
        for j in range(9):
            x = get_cords(j) + error
            y = get_cords(i) + error

            cell = board_img[y:y + cell_size - 2 * error, x:x + cell_size - 2 * error]

            gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

            board[i][j] = match_digit(thresh, templates)

                # cv2.imshow("Cell", thresh)
                # cv2.waitKey(0)
    return board

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

    pyautogui.moveTo(get_cords(j) + (cell_size // 2) + left_start, get_cords(i) + (cell_size // 2) + top_start)
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

sleep(1)
frame = capture_screen()
# cv2.imshow("Captured Sudoku", frame)
# cv2.waitKey(0)

board = extract_digits_from_board(frame)
print_board(board)

solve(board)

print("\nSolution:")
print_board(board)