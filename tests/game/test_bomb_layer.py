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



if __name__ == '__main__':
    unittest.main()
