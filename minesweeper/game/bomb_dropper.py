class BombDropper():
    """

    """
    DEFAULT_SIZE = 10

    def __init__(self, height=DEFAULT_SIZE, width=DEFAULT_SIZE):
        assert height > 0
        assert width > 0
        self.height = height
        self.width = width

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width
