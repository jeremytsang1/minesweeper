import unittest
from minesweeper.game.cell import Cell


class TestCell(unittest.TestCase):
    def setUp(self):
        self.cell = Cell(3, 6)

    def test_initial_state(self):
        self.assertTrue(self.cell.get_count() is None)
        self.assertEqual(self.cell.get_appearance(), Cell.Appearance.UNOPENED)

    def test_invalid_type_row(self):
        with self.assertRaises(TypeError):
            self.cell(None, 20)

    def test_invalid_type_col(self):
        with self.assertRaises(TypeError):
            self.cell(20, None)

    def test_out_of_range_row(self):
        with self.assertRaises(ValueError):
            self.cell = Cell(-5, 20)

    def test_out_of_range_col(self):
        with self.assertRaises(ValueError):
            self.cell = Cell(34, -2129)

    def test_invalid_type_count(self):
        with self.assertRaises(TypeError):
            self.cell.set_count(2.5)

    def test_cell_count_int_out_of_range_positive(self):
        with self.assertRaises(ValueError):
            self.cell.set_count(382)

    def test_cell_count_int_out_of_range_negative(self):
        with self.assertRaises(ValueError):
            self.cell.set_count(-5)

    def test_cell_count_in_range(self):
        for i in range(Cell.MIN_COUNT, Cell.MAX_COUNT + 1):
            self.cell.set_count(i)
            self.assertEqual(self.cell.get_count(), i)



if __name__ == '__main__':
    unittest.main()
