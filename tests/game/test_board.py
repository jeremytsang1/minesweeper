import unittest
from minesweeper.game.board import (
    Board,
    JaggedMinePositionsError,
)
from minesweeper.game.cell import (
    Cell
)


class TestBoard(unittest.TestCase):
    DEFAULT_SHAPE = (10, 10)
    DEFAULT_HEIGHT = DEFAULT_SHAPE[0]
    DEFAULT_WIDTH = DEFAULT_SHAPE[1]

    F = Cell.Appearance.FLAG
    E = Cell.Appearance.EMPTY
    U = Cell.Appearance.UNOPENED
    Y = Cell.Appearance.FLAG_INCORRECT
    B = Cell.Appearance.UNENCOUNTERED_BOMB
    X = Cell.Appearance.OPENED_BOMB

    def make_aliases(self):
        return (True, False, self.F, self.E, self.U, self.Y, self.B, self.X)

    def setUp(self):
        self.t = True
        self.f = False
        self.bombs = self.create_all_bombs(self.DEFAULT_HEIGHT,
                                           self.DEFAULT_WIDTH)
        self.board = Board(self.bombs)

    def check_cell_predicate(self, predicate):
        grid = self.board.get_grid()
        for row in grid:
            for cell in row:
                self.assertTrue(predicate(cell))

    def create_all_bombs(self, height, width):
        return [[True for _ in range(height)] for _ in range(width)]

    def check_all_unopened_at_start(self):
        shape = self.board.get_shape()
        actual = self.board.get_appearance()
        expected = [[self.U for _ in range(shape[1])] for _ in range(shape[0])]
        self.assertEqual(actual, expected)

    def print_appearance(appearance):
        symbols = {
            TestBoard.F: "F",
            TestBoard.E: "E",
            TestBoard.U: "U",
            TestBoard.Y: "Y",
            TestBoard.B: "B",
            TestBoard.X: "X",
        }
        rendered = [[symbols[app] if app in symbols else str(app) for app in row]
                    for row in appearance]
        print(
            "\n".join(str(row) for row in rendered)
        )

    def check_moves(self, display=False):
        self.check_all_unopened_at_start()
        for idx, move in enumerate(self.moves):
            self.compare_state(idx, move, display)

    def compare_state(self, idx, move, display=False):

        actual_validity = move['act'](*move['pos'])
        expected_validity = move['val']
        self.assertEqual(actual_validity, expected_validity)

        expected_appearance = move['board']
        actual_appearance = self.board.get_appearance()
        if display:
            self.dis(actual_appearance, expected_appearance, idx)
        self.assertEqual(actual_appearance, expected_appearance)

        expected_opened_cell_count = move['o_cnt']
        actual_opened_cell_count = self.board.get_opened_cell_count()
        self.assertEqual(actual_opened_cell_count, expected_opened_cell_count)

        expected_opened_bomb_count = move['b_cnt']
        actual_opened_bomb_count = self.board.get_opened_bomb_count()
        self.assertEqual(actual_opened_bomb_count, expected_opened_bomb_count)

    def dis(self, actual_appearance, expected_appearance, idx):
        print(79 * "-")
        print(f'idx: {idx}')
        print("Actual")
        TestBoard.print_appearance(actual_appearance)
        print("Expected")
        print(40 * "-")
        TestBoard.print_appearance(expected_appearance)

    # -------------------------------------------------------------------------

    def test_initial_shape(self):
        self.board = Board(self.bombs)
        grid = self.board.get_grid()
        self.assertEqual(len(grid), self.DEFAULT_HEIGHT)
        self.assertEqual(len(grid[0]), self.DEFAULT_WIDTH)

    def test_initial_grid_types(self):
        self.bombs = self.create_all_bombs(32, 48)
        self.board = Board(self.bombs)
        self.check_cell_predicate(lambda cell: type(cell) == Cell)

    def test_initial_cell_appearance(self):
        self.bombs = self.create_all_bombs(35, 67)
        self.board = Board(self.bombs)
        self.check_cell_predicate(
            lambda cell: cell.get_appearance() == Cell.Appearance.UNOPENED
        )

    def test_repr_10_10(self):
        expected = (
            "? ? ? ? ? ? ? ? ? ?\n"
            "? ? ? ? ? ? ? ? ? ?\n"
            "? ? ? ? ? ? ? ? ? ?\n"
            "? ? ? ? ? ? ? ? ? ?\n"
            "? ? ? ? ? ? ? ? ? ?\n"
            "? ? ? ? ? ? ? ? ? ?\n"
            "? ? ? ? ? ? ? ? ? ?\n"
            "? ? ? ? ? ? ? ? ? ?\n"
            "? ? ? ? ? ? ? ? ? ?\n"
            "? ? ? ? ? ? ? ? ? ?"
        )
        self.assertEqual(repr(self.board), expected)

    def test_repr_1_1(self):
        self.bombs = self.create_all_bombs(1, 1)
        self.board = Board(self.bombs)
        expected = (
            "?"
        )
        self.assertEqual(repr(self.board), expected)

    # -----------------------------------------------------------------------------
    # Toggling tests

    def test_toggle_each_cell_to_flag(self):
        self.board.iterate(lambda cell: self.board.toggle_flag(cell.get_row(),
                                                               cell.get_col()))
        self.board.iterate(lambda cell: self.assertEqual(cell.get_appearance(),
                                                         Cell.Appearance.FLAG))

    # -----------------------------------------------------------------------------
    def test_3_by_3_lose_center(self):
        self.bombs = [
            [self.f, self.f, self.f],
            [self.f, self.t, self.f],
            [self.f, self.f, self.f],
        ]
        expected_apperances = [
            [self.U, self.U, self.U],
            [self.U, self.X, self.U],
            [self.U, self.U, self.U],
        ]
        self.board = Board(self.bombs)
        self.check_all_unopened_at_start()
        self.board.open_cell(1, 1)
        self.assertEqual(self.board.get_opened_bomb_count(), 1)
        self.assertEqual(self.board.get_opened_cell_count(), 0)
        actual_appearance = self.board.get_appearance()
        self.assertEqual(actual_appearance, expected_apperances)

    def test_3_by_3_win_center(self):
        t, f, F, E, U, Y, B, X = self.make_aliases()
        self.bomb_count = 1
        self.bombs = [
            [self.f, self.f, self.f],
            [self.f, self.t, self.f],
            [self.f, self.f, self.f],
        ]
        self.board = Board(self.bombs)
        self.moves = (
            {'board': [[U, U, U],
                       [U, U, U],
                       [U, U, 1]],
             'pos': (2, 2),
             'val': True,
             'o_cnt': 1,
             'b_cnt': 0,
             'act': self.board.open_cell},
            {'board': [[U, U, U],
                       [U, U, U],
                       [1, U, 1]],
             'pos': (2, 0),
             'val': True,
             'o_cnt': 2,
             'b_cnt': 0,
             'act': self.board.open_cell},
            {'board': [[1, U, U],
                       [U, U, U],
                       [1, U, 1]],
             'pos': (0, 0),
             'val': True,
             'o_cnt': 3,
             'b_cnt': 0,
             'act': self.board.open_cell},
            {'board': [[1, U, U],
                       [U, U, U],
                       [1, U,1]],
             'pos': (0, 0),
             'val': False,
             'o_cnt': 3,
             'b_cnt': 0,
             'act': self.board.open_cell},
            {'board': [[1, 1, U],
                       [U, U, U],
                       [1, U, 1]],
             'pos': (0, 1),
             'val': True,
             'o_cnt': 4,
             'b_cnt': 0,
             'act': self.board.open_cell},
            {'board': [[1, 1, U],
                       [U, U, U],
                       [1, 1, 1]],
             'pos': (2, 1),
             'val': True,
             'o_cnt': 5,
             'b_cnt': 0,
             'act': self.board.open_cell},
            {'board': [[1, 1, 1],
                       [U, U, U],
                       [1, 1, 1]],
             'pos': (0, 2),
             'val': True,
             'o_cnt': 6,
             'b_cnt': 0,
             'act': self.board.open_cell},
            {'board': [[1, 1, 1],
                       [1, U, U],
                       [1, 1, 1]],
             'pos': (1, 0),
             'val': True,
             'o_cnt': 7,
             'b_cnt': 0,
             'act': self.board.open_cell},
            {'board': [[1, 1, 1],
                       [1, U, U],
                       [1, 1, 1]],
             'pos': (1, 0),
             'val': False,
             'o_cnt': 7,
             'b_cnt': 0,
             'act': self.board.toggle_flag},
            {'board': [[1, 1, 1],
                       [1, U, F],
                       [1, 1, 1]],
             'pos': (1, 2),
             'val': True,
             'o_cnt': 7,
             'b_cnt': 0,
             'act': self.board.toggle_flag},
            {'board': [[1, 1, 1],
                       [1, U, F],
                       [1, 1, 1]],
             'pos': (1, 2),
             'val': False,
             'o_cnt': 7,
             'b_cnt': 0,
             'act': self.board.open_cell},
            {'board': [[1, 1, 1],
                       [1, U, U],
                       [1, 1, 1]],
             'pos': (1, 2),
             'val': True,
             'o_cnt': 7,
             'b_cnt': 0,
             'act': self.board.toggle_flag},
            {'board': [[1, 1, 1],
                       [1, U, 1],
                       [1, 1, 1]],
             'pos': (1, 2),
             'val': True,
             'o_cnt': 8,
             'b_cnt': 0,
             'act': self.board.open_cell},
        )
        self.check_moves()
        total_cell_count = len(self.bombs) * len(self.bombs[0])
        self.assertEqual(total_cell_count - self.board.get_opened_cell_count(),
                         self.bomb_count)

    def test_10_by_10_win_center(self):
        t, f, F, E, U, Y, B, X = self.make_aliases()
        self.bomb_count = 1
        self.bombs = [
            [f, f, f, f, f, f, f, f, f, f],
            [f, f, f, f, f, f, f, t, f, f],
            [f, f, f, t, f, f, t, f, f, f],
            [f, f, f, t, f, f, f, f, f, f],
            [f, f, t, f, f, f, f, f, f, f],
            [f, t, f, f, f, t, f, f, f, f],
            [f, f, f, f, f, f, f, t, f, f],
            [f, f, f, t, f, f, f, f, f, f],
            [f, f, f, f, f, f, f, t, f, f],
            [f, f, f, f, f, f, f, f, f, f],
        ]
        self.board = Board(self.bombs)
        self.moves = (
            {'board': [
                [U, U, U, U, U, U, U, U, 1, E],
                [U, U, U, U, U, U, U, U, 1, E],
                [U, U, U, U, U, U, U, 2, 1, E],
                [U, U, U, U, U, U, 1, 1, E, E],
                [U, U, U, U, U, U, 1, E, E, E],
                [U, U, U, U, U, U, 2, 1, 1, E],
                [U, U, U, U, U, U, U, U, 1, E],
                [U, U, U, U, U, U, U, U, 2, E],
                [U, U, U, U, U, U, U, U, 1, E],
                [U, U, U, U, U, U, U, U, 1, E],
            ],
             'pos': (9, 9),
             'val': True,
             'o_cnt': 27,
             'b_cnt': 0,
             'act': self.board.open_cell},
            {'board': [
                [U, U, U, U, U, U, U, U, 1, E],
                [U, U, U, U, U, U, U, U, 1, E],
                [U, U, U, U, U, U, U, 2, 1, E],
                [U, U, U, U, U, U, 1, 1, E, E],
                [U, U, U, U, U, U, 1, E, E, E],
                [U, U, U, U, U, U, 2, 1, 1, E],
                [U, U, U, U, U, U, U, U, 1, E],
                [U, U, U, U, U, U, U, U, 2, E],
                [U, U, U, U, U, U, U, U, 1, E],
                [U, U, U, U, U, U, U, U, 1, E],
            ],
             'pos': (3, 6),
             'val': False,
             'o_cnt': 27,
             'b_cnt': 0,
             'act': self.board.open_cell},
            {'board': [
                [U, U, U, U, U, U, U, U, 1, E],
                [U, U, U, U, U, U, U, U, 1, E],
                [U, U, U, U, U, U, U, 2, 1, E],
                [U, U, U, U, U, U, 1, 1, E, E],
                [U, U, U, U, U, U, 1, E, E, E],
                [U, U, U, U, U, U, 2, 1, 1, E],
                [U, U, U, U, U, U, U, U, 1, E],
                [U, U, U, U, U, U, U, 2, 2, E],
                [U, U, U, U, U, U, U, U, 1, E],
                [U, U, U, U, U, U, U, U, 1, E],
            ],
             'pos': (7, 7),
             'val': True,
             'o_cnt': 28,
             'b_cnt': 0,
             'act': self.board.open_cell},
            {'board': [
                [U, U, U, U, U, U, U, U, 1, E],
                [U, U, U, U, U, U, U, U, 1, E],
                [U, U, U, U, U, U, U, 2, 1, E],
                [U, U, U, U, U, U, 1, 1, E, E],
                [U, U, U, U, U, U, 1, E, E, E],
                [U, U, U, U, U, U, 2, 1, 1, E],
                [1, 1, 2, U, 2, 1, 2, U, 1, E],
                [E, E, 1, U, 1, E, 2, 2, 2, E],
                [E, E, 1, 1, 1, E, 1, U, 1, E],
                [E, E, E, E, E, E, 1, U, 1, E],
            ],
             'pos': (9, 0),
             'val': True,
             'o_cnt': 54,
             'b_cnt': 0,
             'act': self.board.open_cell},
            {'board': [
                [E, E, E, E, E, E, 1, U, 1, E],
                [E, E, 1, 1, 1, 1, 2, U, 1, E],
                [E, E, 2, U, U, U, U, 2, 1, E],
                [E, 1, 3, U, U, U, 1, 1, E, E],
                [1, 2, U, U, U, U, 1, E, E, E],
                [U, U, U, U, U, U, 2, 1, 1, E],
                [1, 1, 2, U, 2, 1, 2, U, 1, E],
                [E, E, 1, U, 1, E, 2, 2, 2, E],
                [E, E, 1, 1, 1, E, 1, U, 1, E],
                [E, E, E, E, E, E, 1, U, 1, E],
            ],
             'pos': (0, 2),
             'val': True,
             'o_cnt': 76,
             'b_cnt': 0,
             'act': self.board.open_cell},
            {'board': [
                [E, E, E, E, E, E, 1, 1, 1, E],
                [E, E, 1, 1, 1, 1, 2, U, 1, E],
                [E, E, 2, U, U, U, U, 2, 1, E],
                [E, 1, 3, U, U, U, 1, 1, E, E],
                [1, 2, U, U, U, U, 1, E, E, E],
                [U, U, U, U, U, U, 2, 1, 1, E],
                [1, 1, 2, U, 2, 1, 2, U, 1, E],
                [E, E, 1, U, 1, E, 2, 2, 2, E],
                [E, E, 1, 1, 1, E, 1, U, 1, E],
                [E, E, E, E, E, E, 1, U, 1, E],
            ],
             'pos': (0, 7),
             'val': True,
             'o_cnt': 77,
             'b_cnt': 0,
             'act': self.board.open_cell},
            {'board': [
                [E, E, E, E, E, E, 1, 1, 1, E],
                [E, E, 1, 1, 1, 1, 2, U, 1, E],
                [E, E, 2, U, U, U, U, 2, 1, E],
                [E, 1, 3, U, U, U, 1, 1, E, E],
                [1, 2, U, U, U, U, 1, E, E, E],
                [1, U, U, U, U, U, 2, 1, 1, E],
                [1, 1, 2, U, 2, 1, 2, U, 1, E],
                [E, E, 1, U, 1, E, 2, 2, 2, E],
                [E, E, 1, 1, 1, E, 1, U, 1, E],
                [E, E, E, E, E, E, 1, U, 1, E],
            ],
             'pos': (5, 0),
             'val': True,
             'o_cnt': 78,
             'b_cnt': 0,
             'act': self.board.open_cell},
            {'board': [
                [E, E, E, E, E, E, 1, 1, 1, E],
                [E, E, 1, 1, 1, 1, 2, U, 1, E],
                [E, E, 2, U, U, U, U, 2, 1, E],
                [E, 1, 3, U, U, U, 1, 1, E, E],
                [1, 2, U, U, U, U, 1, E, E, E],
                [1, U, U, U, U, U, 2, 1, 1, E],
                [1, 1, 2, U, 2, 1, 2, U, 1, E],
                [E, E, 1, U, 1, E, 2, 2, 2, E],
                [E, E, 1, 1, 1, E, 1, U, 1, E],
                [E, E, E, E, E, E, 1, 1, 1, E],
            ],
             'pos': (9, 7),
             'val': True,
             'o_cnt': 79,
             'b_cnt': 0,
             'act': self.board.open_cell},
            {'board': [
                [E, E, E, E, E, E, 1, 1, 1, E],
                [E, E, 1, 1, 1, 1, 2, U, 1, E],
                [E, E, 2, U, U, U, U, 2, 1, E],
                [E, 1, 3, U, U, U, 1, 1, E, E],
                [1, 2, U, U, 2, U, 1, E, E, E],
                [1, U, U, U, U, U, 2, 1, 1, E],
                [1, 1, 2, U, 2, 1, 2, U, 1, E],
                [E, E, 1, U, 1, E, 2, 2, 2, E],
                [E, E, 1, 1, 1, E, 1, U, 1, E],
                [E, E, E, E, E, E, 1, 1, 1, E],
            ],
             'pos': (4, 4),
             'val': True,
             'o_cnt': 80,
             'b_cnt': 0,
             'act': self.board.open_cell},
            # {'board': [
            #     [E, E, E, E, E, E, 1, 1, 1, E],
            #     [E, E, 1, 1, 1, 1, 2, *, 1, E],
            #     [E, E, 2, *, U, U, *, 2, 1, E],
            #     [E, 1, 3, *, U, U, 1, 1, E, E],
            #     [1, 2, *, U, 2, U, 1, E, E, E],
            #     [1, *, U, U, U, *, 2, 1, 1, E],
            #     [1, 1, 2, U, 2, 1, 2, *, 1, E],
            #     [E, E, 1, *, 1, E, 2, 2, 2, E],
            #     [E, E, 1, 1, 1, E, 1, *, 1, E],
            #     [E, E, E, E, E, E, 1, 1, 1, E],
            # ],
            #  'pos': (4, 4),
            #  'val': True,
            #  'o_cnt': 80,
            #  'b_cnt': 0,
            #  'act': self.board.open_cell},
        )
        self.check_moves()
        total_cell_count = len(self.bombs) * len(self.bombs[0])






if __name__ == '__main__':
    unittest.main()
