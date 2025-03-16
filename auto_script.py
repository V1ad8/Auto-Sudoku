import mss
import numpy as np
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\2004u\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
import variables_script as var

KILL_SWITCH = 'q'
board = [[0 for _ in range(9)] for _ in range(9)]

def capture_screen():
    width = 9 * var.cell_size + 4 * var.big_border + 6 * var.small_border

    with mss.mss() as sct:
        monitor = {"top": var.top_start, "left": var.left_start, "width": width, "height": width}
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # Convert to BGR format

def load_templates():
    templates = {}
    for num in range(10):
        path = f"templates/{num}.png"
        templates[num] = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    return templates

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

    for i in range(9):
        for j in range(9):
            x = var.get_cords(j) + var.error
            y = var.get_cords(i) + var.error

            cell = board_img[y:y + var.cell_size - 2 * var.error, x:x + var.cell_size - 2 * var.error]

            gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

            board[i][j] = match_digit(thresh, templates)

                # cv2.imshow("Cell", thresh)
                # cv2.waitKey(0)
    return board