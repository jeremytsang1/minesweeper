import unittest
from minesweeper.ui.tui.grid_printing.table_printer import TablePrinter
from minesweeper.ui.tui.grid_printing.table_printer import CommandLineGrid

class TestTablePrinter(unittest.TestCase):

    def test_diagonal_matrices(self):
        expected = [
            "|---+---+---|\n"
            "|   | 0 | 1 |\n"
            "|---+---+---|\n"
            "| 0 | 2 | 2 |\n"
            "|---+---+---|\n"
            "| 1 | 2 | 2 |\n"
            "|---+---+---|",
            "|---+---+---+---|\n"
            "|   | 0 | 1 | 2 |\n"
            "|---+---+---+---|\n"
            "| 0 | 3 | 3 | 3 |\n"
            "|---+---+---+---|\n"
            "| 1 | 3 | 3 | 3 |\n"
            "|---+---+---+---|\n"
            "| 2 | 3 | 3 | 3 |\n"
            "|---+---+---+---|",
        ]
        for k in range(2, 4):
            matrix = [[k for j in range(k)] for i in range(k)]
            actual = TablePrinter.makeTable(matrix)
            # print("\n", TablePrinter.makeTable(matrix), sep="")
            self.assertEqual(actual, expected[k - 2])


if __name__ == '__main__':
    unittest.main()
