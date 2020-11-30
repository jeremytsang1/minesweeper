import unittest
from minesweeper.game.bomb_dropper import BombDropper


class TestBombDropper(unittest.TestCase):
    def setUp(self):
        self.bd = BombDropper()

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
