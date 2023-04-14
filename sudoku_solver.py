class SudokuSolver:
    def __init__(self):
        self.board = []
        self.initialize()
        self.modified_cell = set()

    def set_value(self, value, pos):
        row, col = pos
        self.board[row][col] = value
        faulty_cell = set()
        for row in range(9):
            for col in range(9):
                num = self.board[row][col]
                if num != '':
                    if self.horizontal(row).count(num) > 1:
                        for index, candidate in enumerate(self.horizontal(row)):
                            if candidate == num:
                                faulty_cell.add((row, index))
                    if self.vertical(col).count(num) > 1:
                        for index, candidate in enumerate(self.vertical(col)):
                            if candidate == num:
                                faulty_cell.add((index, col))
                    if self.box(row, col).count(num) > 1:
                        for index, candidate in enumerate(self.box(row, col)):
                            if candidate == num:
                                faulty_cell.add((row//3*3 + index//3, col//3*3 + index%3))
        return faulty_cell

    def initialize(self):
        self.board = [[''] * 9 for _ in range(9)]
        self.modified_cell = set()

    def horizontal(self, row):
        return self.board[row]

    def vertical(self, col):
        return [self.board[r][col] for r in range(9)]

    def box(self, row, col):
        return [self.board[row//3*3 + r][col//3*3 + c] for r in range(3) for c in range(3)]

    def solve(self):
        if self._solve():
            return self.board, self.modified_cell
        else:
            return False

    def _solve(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == '':
                    self.modified_cell.add((row, col))
                    for num in range(1, 10):
                        num = str(num)
                        if num not in self.horizontal(row) and num not in self.vertical(col)\
                                and num not in self.box(row, col):
                            self.board[row][col] = num
                            success = self.solve()
                            if not success:
                                self.board[row][col] = ''
                            else:
                                return True
                    return False
        return True
