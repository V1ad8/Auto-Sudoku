from time import sleep

import cv2
import auto_script as auto
import solver_script as solver
import possible_script as possible
import possible_script as fill
from solver_script import board

sleep(1)
frame = auto.capture_screen()
cv2.imshow("Captured Sudoku", frame)
cv2.waitKey(0)

auto.extract_digits_from_board(frame)

auto.show_matrix(board)

solver.print_board()

# --- Code get the game board ---

# fill.clear()

solver.initialise_possible()
auto.board = solver.solve()
# auto.board = solver.solve()

if fill.has_empty():
    fill.fill_possible()

print("\nSolution:")
solver.print_board()