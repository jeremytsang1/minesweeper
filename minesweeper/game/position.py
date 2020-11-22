class Position():
    """Documentation for Position

    """
    def __init__(self, row, col):
        if row < 0 or col < 0:
            raise NegativeCoordsError((row, col))
        self.coord = (row, col)

    def get_row(self):
        return self.coord[0]

    def get_col(self):
        return self.coord[1]

    def get_coord(self):
        return self.coord


class PositionError(Exception):
    def __init__(self, pos):
        pass

class NegativeCoordsError(PositionError):
    """Error for when one or more coord is negative.

    """
    def __init__(self, pos):
        super().__init__(f"(pos[0],  pos[1]) has a negative component.")
