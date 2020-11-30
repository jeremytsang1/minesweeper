class PositionUtil():
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

class PositionError(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidComponent(PositionError):
    def __init__(self, component, name):
        super().__init__(
            f'Position\'s {name} is non-positive and has value {component}.'
        )
