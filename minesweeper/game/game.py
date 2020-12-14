from minesweeper.game.board import Board
from minesweeper.game.cell import Cell
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
        self.flags_left_to_place = bomb_count
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

    def get_actions(self):
        return self.open_cell, self.toggle_flag, self.chord_cell

    def open_cell(self, row, col):
        print("\nOpening!")
        self.board.reset_affected_positions()

        valid = self.board.open_cell(row, col)
        move = Move(valid=valid,
                    cell=self.board.get_cell(row, col),
                    move_type=Move.MoveType.OPEN,
                    affected_positions=self.board.get_affected_positions())
        self.increment_turn(move)
        if valid:
            self.update_end_game()

        self.board.reset_affected_positions()
        return move

    def toggle_flag(self, row, col):
        print("\nToggling flag!")
        self.board.reset_affected_positions()

        valid = self.board.toggle_flag(row, col)
        move = Move(valid=valid,
                    cell=self.board.get_cell(row, col),
                    move_type=Move.MoveType.TOGGLE_FLAG,
                    affected_positions=self.board.get_affected_positions())
        self.flags_left_to_place += self.change_flag_count(move, row, col)
        self.increment_turn(move)

        self.board.reset_affected_positions()
        return move

    def chord_cell(self, row, col):
        print("\nChording!")
        self.board.reset_affected_positions()

        valid, flag_count = self.board.chord_cell(row, col)
        move = Move(valid=valid,
                    cell=self.board.get_cell(row, col),
                    move_type=Move.MoveType.CHORD,
                    affected_positions=self.board.get_affected_positions(),
                    adjFlagCount=flag_count)
        self.increment_turn(move)
        if valid:
            self.update_end_game()

        self.board.reset_affected_positions()
        return move

    def change_flag_count(self, move, row, col):
        if move.is_valid():
            appearance = self.board.get_single_appearance(row, col)
            return -1 if appearance == Cell.Appearance.FLAG else 1
        else:
            return 0

    def increment_turn(self, move):
        if move.is_valid():
            self.turn += 1

    def update_end_game(self):
        if self.cell_count - self.board.get_opened_cell_count() == self.bomb_count:
            self.won = True
            self.board.convert_all_bombs_to_flags()
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

    def get_flags_left_to_place(self):
        return self.flags_left_to_place

    def get_single_appearance(self, row, col):
        return self.board.get_single_appearance(row, col)

    def get_all_appearances(self):
        return self.board.get_all_appearances()


class GameError(Exception):
    def __init__(self, message):
        super().__init__(message)
