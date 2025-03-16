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


def show_matrix(matrix, window_name="Matrix Display", cell_size=50):
    rows, cols = len(matrix), len(matrix[0])
    img_size = (cols * cell_size, rows * cell_size, 3)  # Create an image of size (width, height, channels)

    # Create a white background image
    img = np.ones(img_size, dtype=np.uint8) * 255

    # Draw grid
    for i in range(rows + 1):
        cv2.line(img, (0, i * cell_size), (cols * cell_size, i * cell_size), (0, 0, 0), 2)
    for j in range(cols + 1):
        cv2.line(img, (j * cell_size, 0), (j * cell_size, rows * cell_size), (0, 0, 0), 2)

    # Put numbers in the cells
    font = cv2.FONT_HERSHEY_SIMPLEX
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] != 0:  # Don't draw zeroes (empty cells)
                text = str(matrix[i][j])
                text_size = cv2.getTextSize(text, font, 1, 2)[0]
                text_x = j * cell_size + (cell_size - text_size[0]) // 2
                text_y = i * cell_size + (cell_size + text_size[1]) // 2
                cv2.putText(img, text, (text_x, text_y), font, 1, (0, 0, 0), 2)

    # Show the image
    cv2.imshow(window_name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()