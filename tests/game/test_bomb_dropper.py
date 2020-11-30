import unittest
from minesweeper.game.bomb_dropper import (
    BombDropper,
    InvalidComponent,
    InvalidBombCount,
    InvalidInitialClick
)


class TestBombDropper(unittest.TestCase):
    def setUp(self):
        self.bd = BombDropper()

    def test_validation_neg_height(self):
        with self.assertRaises(InvalidComponent):
            self.bd = BombDropper(-18, 29)

    def test_validation_neg_width(self):
        with self.assertRaises(InvalidComponent):
            self.bd = BombDropper(86, -38)

    def test_validation_zero_height(self):
        with self.assertRaises(InvalidComponent):
            self.bd = BombDropper(0, 8)

    def test_validation_zero_width(self):
        with self.assertRaises(InvalidComponent):
            self.bd = BombDropper(8, 0)

    def test_validate_bomb_count_negative(self):
        with self.assertRaises(InvalidBombCount):
            self.bd = BombDropper(45, 23, 34, 5, -6)

    def test_validate_bomb_count_zero(self):
        with self.assertRaises(InvalidBombCount):
            self.bd = BombDropper(45, 23, 34, 5, 0)

    def test_validate_bomb_count_entirely_filled(self):
        with self.assertRaises(InvalidBombCount):
            self.bd = BombDropper(45, 23, 34, 5, 1035)

    def test_validate_initial_click_negative(self):
        with self.assertRaises(InvalidInitialClick):
            self.bd = BombDropper(10, 4, -3, -2)

    def test_validate_initial_click_positive(self):
        with self.assertRaises(InvalidInitialClick):
            self.bd = BombDropper(10, 4, 32, 2)

    def test_default_init(self):
        self.assertEqual(self.bd.get_height(), 10)
        self.assertEqual(self.bd.get_width(), 10)

    def test_init(self):
        self.bd = BombDropper(35, 29)
        self.assertEqual(self.bd.get_height(), 35)
        self.assertEqual(self.bd.get_width(), 29)

    def test_initialize_empty_bomb_field(self):
        self.bd = BombDropper(2, 5)
        expected = [
            [False, False, False, False, False],
            [False, False, False, False, False],
        ]
        actual = self.bd.initialize_empty_bomb_field()
        self.assertEqual(actual, expected)

    def test_initialize_empty_bomb_field_1_row(self):
        self.bd = BombDropper(1, 10)
        expected = [
            [False, False, False, False, False, False, False, False, False, False]
        ]
        actual = self.bd.initialize_empty_bomb_field()
        self.assertEqual(actual, expected)

    def test_initialize_empty_bomb_field_1_col(self):
        self.bd = BombDropper(10, 1)
        expected = [
            [False],
            [False],
            [False],
            [False],
            [False],
            [False],
            [False],
            [False],
            [False],
            [False],
        ]
        actual = self.bd.initialize_empty_bomb_field()
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
