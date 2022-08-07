import MiniSys
import Object
import button
import panel


def print_grid(grid):
    print()
    for line in grid:
        print(line)


class SudokuSolver(Object.Object):
    def __init__(self, parent, puzzle):
        super().__init__(parent)

        self.int_puzzle = puzzle

        puzzle_panel = panel.Panel(parent, 20, 20, 280, 280)
        self.puzzle = []
        for i in range(9):
            row = []
            for j in range(9):
                x = i*30
                if (i+1)%3:
                    x += 4
                y = j*30
                if (j+1)%3:
                    y += 4

                cell = button.Button(puzzle_panel, y, x, 30, 30, str(self.int_puzzle[i][j]))
                cell.align('centre')
                row.append(cell)
            self.puzzle.append(row)

    def used_in_row(self, row, num):
        for col in range(9):
            if self.get_puzzle_value(row, col) == num:
                return True
        return False

    def used_in_col(self, col, num):
        for row in range(9):
            if self.get_puzzle_value(row, col) == num:
                return True
        return False

    def used_in_box(self, x, y, num):
        for row in range(3):
            for col in range(3):
                if self.get_puzzle_value(x*3+col, y*3+row) == num:
                    return True
        return False

    def is_safe(self, row, col, num):
        urow = self.used_in_row(row, num)
        ucol = self.used_in_col(col, num)
        ubox = self.used_in_box(row//3, col//3, num)
        return not urow and not ucol and not ubox

    def get_unassigned_location(self):
        for i in range(9):
            for j in range(9):
                if self.get_puzzle_value(i, j) == 0:
                    return i, j
        return 9, 9

    def get_puzzle_value(self, row, col):
        return int(self.puzzle[row][col].text)

    def set_puzzle_value(self, row, col, value):
        cell = self.puzzle[row][col]
        cell.set_text(str(value))
        cell.align('centre')

    def solve_sudoku(self):
        row, col = self.get_unassigned_location()
        if col == 0:
            self.panel.loop()

        if row == 9 and col == 9:
            return True

        for i in range(1, 10):
            if self.is_safe(row, col, i):
                self.set_puzzle_value(row, col, i)
                if self.solve_sudoku():
                    return True

        self.set_puzzle_value(row, col, 0)
        return False

    def get_puzzle(self):
        return self.int_puzzle


if __name__ == '__main__':
    puzzle = [
        [0, 0, 0, 0, 9, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 7, 0, 0],
        [0, 8, 0, 0, 3, 1, 0, 6, 0],
        [0, 0, 6, 9, 0, 8, 0, 0, 0],
        [8, 0, 4, 0, 0, 0, 5, 0, 3],
        [0, 0, 0, 3, 0, 2, 4, 0, 0],
        [0, 9, 0, 1, 6, 0, 0, 7, 0],
        [0, 0, 5, 0, 0, 0, 8, 0, 0],
        [0, 0, 0, 0, 7, 0, 0, 0, 0]
    ]

    puzzle = [
        [0, 4, 0, 2, 0, 1, 0, 6, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [9, 0, 5, 0, 0, 0, 3, 0, 7],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [5, 0, 7, 0, 8, 0, 1, 0, 4],
        [0, 1, 0, 0, 0, 0, 0, 9, 0],
        [0, 0, 1, 0, 0, 0, 6, 0, 0],
        [0, 0, 0, 7, 0, 5, 0, 0, 0],
        [6, 0, 8, 9, 0, 4, 5, 0, 3]
    ]

    sys = MiniSys.MiniRender(320, 320)

    solver = SudokuSolver(sys, puzzle)
    solver.solve_sudoku()
    sys.mainloop()
    solved = solver.get_puzzle()
    print_grid(solved)
