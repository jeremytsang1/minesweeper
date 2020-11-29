from minesweeper.game.board import Board


class Game:
    MIN_WIDTH = 1
    MIN_HEIGHT = 1
    DEFAULT_SIZE = 10
    MIN_BOMB_COUNT = 1

    def __init__(self, height, width, bomb_count=1,
                 first_click_row=0, first_click_col=0):
        self.height = height
        self.width = width
        self.bomb_count = bomb_count

        if height < Game.MIN_HEIGHT or width < Game.MIN_WIDTH:
            raise GameNegativeDimsError(height, width)

        self.board = Board(Game.lay_bombs(first_click_row, first_click_col))

    def validate_init_input(self):
        self.validate_shape()
        self.validate_bomb_count()
        self.validate_first_move()

    def validate_shape(self):
        # TODO
        pass

    def validate_bomb_count(self):
        # TODO
        pass

    def validate_first_move(self):
        # TODO
        pass

    def open_cell(self, row, col):
        pass

    def sweep_region(self, row, col):
        pass

    def check_victory(self):
        pass

    def check_loss(self):
        pass

    @staticmethod
    def lay_bombs(first_click_row, first_click_col):
        pass


class GameError(Exception):
    def __init__(self, message):
        super().__init__(message)


class GameNegativeDimsError(GameError):
    def __init__(self, height, width):
        super().__init__('Cannot create Game with negative dimensions '
                         f'({height}, {width}).')


class GameInvalidBombCount(GameError):
    def __init__(self, bomb_count):
        super().__init__('Cannot create Game with less than '
                         f'{Game.MIN_BOMB_COUNT} bombs.')
