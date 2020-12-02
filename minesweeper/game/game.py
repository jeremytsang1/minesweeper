from minesweeper.game.board import Board
from minesweeper.game.bomb_dropper import BombDropper
from minesweeper.game.move import Move


class Game:
    MIN_WIDTH = 1
    MIN_HEIGHT = 1
    DEFAULT_SIZE = 10
    MIN_BOMB_COUNT = 1

    def __init__(self, height, width, bomb_count=1,
                 first_click_row=0, first_click_col=0):
        Game.validate_initial_conditions(height, width, bomb_count,
                                         first_click_row, first_click_col)
        self.bomb_count = bomb_count
        self.cell_count = height * width
        self.bomb_dropper = BombDropper(height, width, first_click_row,
                                        first_click_col, bomb_count)
        self.board = Board(self.bomb_dropper.drop_bombs())
        self.won = False
        self.loss = False
        self.turn = 0

    @staticmethod
    def validate_initial_conditions(height, width, bomb_count,
                                    first_click_row, first_click_col):
        if height < Game.MIN_HEIGHT or width < Game.MIN_WIDTH:
            raise ValueError(
                'Cannot create Game with negative dimensions '
                f'({height}, {width}).'
            )
        elif bomb_count not in range(Game.MIN_BOMB_COUNT, height * width):
            raise ValueError(
                'bomb_count  must be positive and less than total number of '
                f'cells ({height * width}) but was {bomb_count}'
            )
        elif first_click_row not in range(0, height):
            raise ValueError(
                f'first_click_row must be in range(0, {height}) but was '
                f'{first_click_row}'
            )
        elif first_click_col not in range(0, width):
            raise ValueError(
                f'first_click_col must be in range(0, {width}) but was '
                f'{first_click_col}'
            )
        else:
            pass  # Input valid

    # -----------------------------------------------------------------------------
    # PUBLIC # TODO rename since there is no privacy modifiers in python

    def open_cell(self, row, col):
        print("\nOpening!")
        valid = self.board.open_cell(row, col)
        move = Move(valid, self.board.get_cell(row, col), Move.MoveType.OPEN)
        self.increment_turn(move)
        if valid:
            self.update_end_game()
        return move

    def toggle_flag(self, row, col):
        print("\nToggling flag!")
        valid = self.board.toggle_flag(row, col)
        move = Move(valid, self.board.get_cell(row, col), Move.MoveType.TOGGLE_FLAG)
        self.increment_turn(move)
        return move

    def chord_cell(self, row, col):
        print("\nChording!")
        valid, flag_count = self.board.chord_cell(row, col)
        move = Move(valid, self.board.get_cell(row, col),
                    Move.MoveType.CHORD, flag_count)
        self.increment_turn(move)
        if valid:
            self.update_end_game()
        return move

    def increment_turn(self, move):
        if move.is_valid():
            self.turn += 1

    def update_end_game(self):
        if self.cell_count - self.board.get_opened_cell_count() == self.bomb_count:
            self.won = True
            return
        if self.board.get_opened_bomb_count() > 0:
            self.loss = True
            self.board.reveal_board()
            return

    def check_end_game(self):
        assert not (self.won and self.loss)
        return self.won, self.loss

    def get_turn(self):
        return self.turn

    def get_grid(self):
        return self.board.get_grid()


class GameError(Exception):
    def __init__(self, message):
        super().__init__(message)
