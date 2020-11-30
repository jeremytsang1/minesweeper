class BombDropper():
    """

    """
    DEFAULT_SIZE = 10

    def __init__(self, height=DEFAULT_SIZE, width=DEFAULT_SIZE):
        BombDropper.validate_components(height, width)
        self.height = height
        self.width = width
        self.bombs = self.drop_bombs()

    @staticmethod
    def validate_components(height, width):
        if height <= 0:
            raise InvalidComponent(height, "height")
        if width <= 0:
            raise InvalidComponent(width, "width")

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def get_bombs(self):
        return self.bombs

    def initialize_empty_bomb_field(self):
        return [[False for _ in range(self.width)] for _ in range(self.height)]

    def drop_bombs(self):
        bombs = self.initialize_empty_bomb_field()
        return bombs


class BombDropperError(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidComponent(BombDropperError):
    def __init__(self, component, name):
        super().__init__(
            f'BombDropper\'s {name} is non-positive and has value {component}.'
        )
