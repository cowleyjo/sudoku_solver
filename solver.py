from api_call import api_call
import random
import os
import time
import copy

start_time = time.time()

def update_timer():
    """Prints elapsed time at the bottom of the grid."""
    elapsed = time.time() - start_time
    # Move cursor to bottom of grid (after 9 rows + 2 separators)
    term_row = 6 * 2 + 1
    print(f"\033[{term_row};0HTime Elapsed: {elapsed:6.2f}s", end="")
    sys.stdout.flush()

def check_sudoku(x, y, puzzle):
    value = puzzle[x][y]

    for i in range(0, 9):
        if (i != x):
            if (puzzle[i][y] == value):
                # print(f"Failed Vertical Test at ({i}, {y})")
                return False
    
    for j in range(0, 9):
        if (j != y):
            if (puzzle[x][j] == value):
                # print(f"Failed Horizontal Test at ({x}, {j})")
                return False
    
    box = get_box(x, y)
    # print(f"Box: {box}")
    # time.sleep(1)


    indices = []
    match(box):
        case 1:
            indices = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
        case 2:
            indices = [[0, 3], [0, 4], [0, 5], [1, 3], [1, 4], [1, 5], [2, 3], [2, 4], [2, 5]]
        case 3:
            indices = [[0, 6], [0, 7], [0, 8], [1, 6], [1, 7], [1, 8], [2, 6], [2, 7], [2, 8]]
        case 4:
            indices = [[3, 0], [3, 1], [3, 2], [4, 0], [4, 1], [4, 2], [5, 0], [5, 1], [5, 2]]
        case 5:
            indices = [[3, 3], [3, 4], [3, 5], [4, 3], [4, 4], [4, 5], [5, 3], [5, 4], [5, 5]]
        case 6:
            indices = [[3, 6], [3, 7], [3, 8], [4, 6], [4, 7], [4, 8], [5, 6], [5, 7], [5, 8]]
        case 7:
            indices = [[6, 0], [6, 1], [6, 2], [7, 0], [7, 1], [7, 2], [8, 0], [8, 1], [8, 2]]
        case 8:
            indices = [[6, 3], [6, 4], [6, 5], [7, 3], [7, 4], [7, 5], [8, 3], [8, 4], [8, 5]]
        case 9:
            indices = [[6, 6], [6, 7], [6, 8], [7, 6], [7, 7], [7, 8], [8, 6], [8, 7], [8, 8]]


    for pair in indices:
        # print(f"Pair: {pair}")
        # time.sleep(1)
        # print(f"Pair Value: {puzzle[pair[0]][pair[1]]}")
        # time.sleep(1)
        if (puzzle[pair[0]][pair[1]] == value and (pair[0] != x and pair[1] != y)):
            # print("Failed Box Check")
            return False
    
    return True

'''
Order of boxes,
1 | 2 | 3
---------
4 | 5 | 6
---------
7 | 8 | 9
'''
def get_box(x_index, y_index):
    row = None
    column = None

    match(x_index):
        case _ if x_index < 3:
            row = "top"
        case _ if x_index >= 3 and x_index < 6:
            row = "middle"
        case _ if x_index >= 6:
            row = "bottom"
    
    match(y_index):
        case _ if y_index < 3:
            column = "left"
        case _ if y_index >= 3 and y_index < 6:
            column = "middle"
        case _ if y_index >= 6:
            column = "right"
    
    match(row, column):
        case ("top", "left"):
            return 1
        case ("top", "middle"):
            return 2
        case ("top", "right"):
            return 3
        case ("middle", "left"):
            return 4
        case ("middle", "middle"):
            return 5
        case ("middle", "right"):
            return 6
        case ("bottom", "left"):
            return 7
        case ("bottom", "middle"):
            return 8
        case ("bottom", "right"):
            return 9

def print_sudoku(x = 0, y = 0, puzzle = list[list]):
    time.sleep(0.1)
    # clear()
    row_num = 0
    for row in puzzle:
        num_num = 0
        for num in row:
            if (row_num == x and num_num == y):
                print(f" [{num}]", end="")
            else: 
                print(f"  {num} ", end="")
            num_num += 1
            if (num_num % 3 == 0 and num_num != 9):
                print(" | ", end="")
        print()
        print()
        row_num += 1
        if (row_num % 3 == 0 and row_num != 9):
            print("--------------------------------------------")

def print_sudoku_initial(puzzle):
    """Print the whole grid once; keep it static in terminal."""
    for row_num, row in enumerate(puzzle):
        for col_num, num in enumerate(row):
            if col_num % 3 == 0 and col_num != 0:
                print(" |", end="")
            print(f" {num} " if num != "0" else " . ", end="")
        print()
        if (row_num + 1) % 3 == 0 and row_num != 8:
            print("------------------------------")


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def preprocess(puzzle: list[list]):
    allowed = []
    for i in range(0, 9):
        for j in range(0, 9):
            if puzzle[i][j] == "0":
                allowed.append([i, j])
    
    return allowed

import sys

def update_cell(x, y, val, highlight=False):
    """
    Overwrite one cell at row x, column y in the terminal.
    Keeps the existing grid and spacing intact.
    """
    # Each row is one line plus horizontal separators every 3 rows
    term_row = x + 1 + (x // 3)  # 1-indexed for ANSI codes

    # Each number takes 3 chars, plus vertical separators " |" every 3 columns
    term_col = y * 3 + (y // 3) * 2 + 1  # 1-indexed

    # Move cursor to the cell
    print(f"\033[{term_row};{term_col}H", end="")

    # Print the number (highlight with brackets if needed)
    if highlight:
        display = f"[{val}]" if val != "0" else "[0]"
    else:
        display = f" {val} " if val != "0" else " 0 "
    print(display, end="")

    # Flush immediately so terminal updates in real time
    sys.stdout.flush()


def attempt_box(x, y, val, puzzle):
    puzzle[x][y] = str(val)
    update_cell(x, y, str(val), True)
    # time.sleep(0.01)
    return check_sudoku(x, y, puzzle)


def unique_solve(puzzle):
    clear()
    print_sudoku_initial(puzzle)
    allowed_indices = preprocess(puzzle)
    first_solution = None

    curr = 0

    solution_count = 0

    while True:
        if (curr < 0):
            break

        if (curr == len(allowed_indices)):
            solution_count += 1

            if solution_count == 1:
                first_solution = copy.deepcopy(puzzle)
            
            if solution_count > 1:
                return [False, first_solution]

            curr -= 1
            while curr >= 0 and int(puzzle[allowed_indices[curr][0]][allowed_indices[curr][1]]) == 9:
                puzzle[allowed_indices[curr][0]][allowed_indices[curr][1]] = "0"
                update_cell(allowed_indices[curr][0], allowed_indices[curr][1], ".", False)
                curr -= 1
            if curr < 0:
                break
        
        index = allowed_indices[curr]

        starting_num = int(puzzle[index[0]][index[1]])

        if starting_num == 9:
            starting_num = 0

        attempt = False

        for i in range(starting_num + 1, 10):
            attempt = attempt_box(index[0], index[1], i, puzzle)
            update_timer()
            # time.sleep(0.5)
            if (attempt == True):
                # print("Valid Position, Leave Current Loop")
                # time.sleep(0.5)
                update_cell(index[0], index[1], i, False)
                curr += 1
                break

        if not attempt:
            # Reset current cell
            puzzle[index[0]][index[1]] = "0"
            update_cell(index[0], index[1], ".", False)
            curr -= 1

            # Backtrack repeatedly until we find a cell that can increment
            while curr >= 0 and int(puzzle[allowed_indices[curr][0]][allowed_indices[curr][1]]) == 9:
                puzzle[allowed_indices[curr][0]][allowed_indices[curr][1]] = "0"
                update_cell(allowed_indices[curr][0], allowed_indices[curr][1], ".", False)
                curr -= 1

    # clear()
    return [True, first_solution]
