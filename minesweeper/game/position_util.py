class PositionUtil():
    SHIFTS = (-1, 0, 1)

    def __init__(self, height, width):
        PositionUtil.validate_components(height, width)
        self.height = height
        self.width = width
        self.valid_positions = {(i, j) for j in range(width) for i in range(height)}

    def validate_components(height, width):
        if height <= 0:
            raise InvalidComponent(height, "height")
        if width <= 0:
            raise InvalidComponent(width, "width")

    def validate_pos(self, row, col):
        if row not in range(self.height) or col not in range(self.width):
            raise OutOfBoundsError(self.height, self.width, row, col)

    def adj(self, row, col):
        self.validate_pos(row, col)

        return {(row + i, col + j) for j in self.SHIFTS for i in self.SHIFTS
                if (not (j == 0 and i == 0))
                and (row + i, col + j) in self.valid_positions}


class PositionError(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidComponent(PositionError):
    def __init__(self, component, name):
        super().__init__(
            f'Position\'s {name} is non-positive and has value {component}.'
        )


class OutOfBoundsError(PositionError):
    def __init__(self, height, width, row, col):
        super().__init__(
            f'({row}, {col}) is out of bounds on a {height} x {width} grid'
        )
