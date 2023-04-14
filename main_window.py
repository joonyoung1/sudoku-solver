from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.Qt import QWidget, QApplication, Qt
from custom_widgets import ClickLabel, ControlButton, HLine
from sudoku_solver import SudokuSolver
import sys


class MainWindow(QWidget):
    RED = '#FF6961'
    GREEN = '#E5EBDD'
    BLUE = '#AEC6CF'
    DARK_BLUE = '#0F52BA'
    WHITE = '#FFFFFF'
    NUM_KEY = [Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4, Qt.Key_5, Qt.Key_6, Qt.Key_7, Qt.Key_8, Qt.Key_9]

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Sudoku Solver')
        self.sudoku_solver = SudokuSolver()
        self.selected_cell = None
        self.faulty_cell = set()
        self.state = 'normal'

        self.sudoku_cell = [[QWidget()] * 9 for _ in range(9)]
        for row in range(9):
            for col in range(9):
                cell_color = self.GREEN if (row//3 + col//3) % 2 == 0 else self.WHITE
                cell = ClickLabel(cell_color)
                cell.clicked.connect(self.cell_clicked)
                self.sudoku_cell[row][col] = cell

        partial_grid = [[QWidget()] * 3 for _ in range(3)]
        for row in range(3):
            for col in range(3):
                frame = QFrame()
                frame.setFrameShape(QFrame.Panel)
                frame.setFrameShadow(QFrame.Raised)
                frame.setLineWidth(2)
                grid = QGridLayout()
                grid.setSpacing(0)
                grid.setContentsMargins(0, 0, 0, 0)
                frame.setLayout(grid)
                for r in range(3):
                    for c in range(3):
                        grid.addWidget(self.sudoku_cell[row*3 + r][col*3 + c], r, c)
                partial_grid[row][col] = frame

        sudoku_layout = QGridLayout()
        sudoku_layout.setSpacing(0)
        for row in range(3):
            for col in range(3):
                sudoku_layout.addWidget(partial_grid[row][col], row, col)

        control_pad = QHBoxLayout()
        control_button_map = [{'text': 'Solve', 'callback': self.solve_clicked},
                              {'text': 'Initialize', 'callback': self.initialize_clicked}]
        for information in control_button_map:
            button = ControlButton(information['text'])
            button.clicked.connect(information['callback'])
            control_pad.addWidget(button)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.addLayout(sudoku_layout)
        main_layout.addWidget(HLine(1))
        main_layout.addLayout(control_pad)
        self.setLayout(main_layout)

        self.adjustSize()
        self.setMinimumSize(self.size())
        self.setMaximumSize(self.size())

    def clear(self):
        if self.selected_cell is not None:
            self.selected_cell.set_background_color(self.selected_cell.base_color)
            self.selected_cell = None

    def find(self):
        for r, row in enumerate(self.sudoku_cell):
            if self.selected_cell in row:
                return r, row.index(self.selected_cell)

    def update(self):
        for row in self.sudoku_cell:
            for cell in row:
                cell.set_background_color(cell.base_color)

        if self.selected_cell is not None:
            self.selected_cell.set_background_color(self.BLUE)

        for row, col in self.faulty_cell:
            cell = self.sudoku_cell[row][col]
            cell.set_background_color(self.RED)

    def impossible(self):
        self.state = 'error'
        for row in range(9):
            for col in range(9):
                self.sudoku_cell[row][col].set_background_color(self.RED)

    def cell_clicked(self):
        if self.state != 'solved':
            if self.selected_cell is not None:
                self.selected_cell.set_background_color(self.selected_cell.base_color)
            self.selected_cell = self.sender()
            self.update()

    def solve_clicked(self):
        if self.state == 'normal':
            result = self.sudoku_solver.solve()
            if not result:
                self.impossible()
                return
            answer_board, modified_cell = result
            for row in range(9):
                for col in range(9):
                    self.sudoku_cell[row][col].setText(answer_board[row][col])
            for row, col in modified_cell:
                self.sudoku_cell[row][col].set_font_color(self.DARK_BLUE)
            self.clear()
            self.state = 'solved'

    def initialize_clicked(self):
        for row in self.sudoku_cell:
            for cell in row:
                cell.clear()
        self.faulty_cell = set()
        self.sudoku_solver.initialize()
        self.update()
        self.clear()
        self.state = 'normal'

    def keyPressEvent(self, event):
        if self.selected_cell is not None:
            if event.key() in self.NUM_KEY:
                for num, key in enumerate(self.NUM_KEY, start=1):
                    if event.key() == key:
                        self.selected_cell.setText(str(num))
                        self.faulty_cell = self.sudoku_solver.set_value(str(num), self.find())
                        self.update()
            elif event.key() == Qt.Key_Backspace:
                self.selected_cell.clear()
                self.faulty_cell = self.sudoku_solver.set_value('', self.find())
                self.update()
            elif event.key() in [Qt.Key_Return, Qt.Key_Enter]:
                self.solve_clicked()

            if len(self.faulty_cell) > 0:
                self.state = 'error'
            else:
                self.state = 'normal'


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
