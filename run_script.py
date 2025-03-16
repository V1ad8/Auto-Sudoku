from time import sleep

import cv2
import auto_script as auto
import solver_script as solver
import possible_script as possible

sleep(1)
frame = auto.capture_screen()
cv2.imshow("Captured Sudoku", frame)
cv2.waitKey(0)

auto.extract_digits_from_board(frame)
solver.print_board()

# --- Code get the game board ---

auto.board = solver.solve()

print("\nSolution:")
solver.print_board()