class TerminalUI():
    """User interface for command line version of the game.

    """
    def __init__(self, board):
        self.height = board.get_height()
        self.width = board.get_width()
