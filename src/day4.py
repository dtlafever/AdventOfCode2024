# Problem: https://adventofcode.com/2024/day/4#part2
import numpy as np
import re

XMAS_STR = "XMAS"
REVERSE_XMAS_STR = "SAMX"
CROSS_REG_EXP = r'M.M.A.S.S|M.S.A.M.S|S.S.A.M.M|S.M.A.S.M'

def calculate_xmas_count(puzzle_grid: np.array) -> int:
    xmas_count = 0

    for row in puzzle_grid:
        row_str = ''.join(row)

        # Left to Right
        xmas_count += row_str.count(XMAS_STR)
        # Right to Left
        xmas_count += row_str.count(REVERSE_XMAS_STR)

    for col in puzzle_grid.T:
        col_str = ''.join(col)

        # Top to Bottom
        xmas_count += col_str.count(XMAS_STR)
        # Bottom to Top
        xmas_count += col_str.count(REVERSE_XMAS_STR)


    for i in range(-puzzle_grid.shape[0] + 1, puzzle_grid.shape[1]):
        # Diagonal Top Left to Bottom Right
        diag_str = ''.join(puzzle_grid.diagonal(i))
        xmas_count += diag_str.count(XMAS_STR)

        # Diagonal Bottom Right to Top Left
        # diag_str = ''.join(np.flip(puzzle_grid).diagonal(i))
        xmas_count += diag_str.count(REVERSE_XMAS_STR)

        # Diagonal Top Right to Bottom Left
        diag_str = ''.join(np.fliplr(puzzle_grid).diagonal(i))
        xmas_count += diag_str.count(XMAS_STR)

        # Diagonal Bottom Left to Top Right
        # diag_str = ''.join(np.flipud(puzzle_grid).diagonal(-i))
        xmas_count += diag_str.count(REVERSE_XMAS_STR)

    return xmas_count

def puzzle1():
    puzzle_grid = []
    with open('../data/input4.txt') as f:
        for line in f:
            # break down the line into a list of characters and append it to the puzzle_grid
            row = list(line.strip())
            puzzle_grid.append(row)

    # convert the puzzle_grid to a numpy array
    puzzle_grid = np.array(puzzle_grid)

    xmas_count = calculate_xmas_count(puzzle_grid)

    print(f"Total XMAS Count: {xmas_count}")

def is_xmas_pattern(flattened_3_by_3_grid: str) -> bool:
    if re.search(CROSS_REG_EXP, flattened_3_by_3_grid):
        return True
    return False

def calculate_xmas_pattern_count(puzzle_grid):
    xmas_pattern_count = 0
    # NOTE: assumes square grid
    for row in range(len(puzzle_grid) - 2): # -2 to avoid out of bounds
        for col in range(len(puzzle_grid[0]) - 2): # -2 to avoid out of bounds
            flattened_3_by_3_grid =  (puzzle_grid[row][col:col+3])
            flattened_3_by_3_grid += (puzzle_grid[row+1][col:col + 3])
            flattened_3_by_3_grid += (puzzle_grid[row+2][col:col + 3])
            if is_xmas_pattern(flattened_3_by_3_grid):
                xmas_pattern_count += 1
    return xmas_pattern_count

def puzzle2():
    puzzle_grid = []
    with open('../data/input4.txt') as f:
        for line in f:
            row = line.strip() # leaving as a string to make it easier to search for the pattern
            puzzle_grid.append(row)

    xmas_pattern_count = calculate_xmas_pattern_count(puzzle_grid)

    print(f"Total X-MAS Pattern Count: {xmas_pattern_count}")

def main():
    puzzle1()
    puzzle2()

if __name__ == "__main__":
    main()