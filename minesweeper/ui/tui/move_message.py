from minesweeper.game.move import Move


class MoveMessage():
    """Messages to show user if they made an illegal move."""
    MOVE_MESSAGE = {
        Move.Invalid.CANT_OPEN_FLAGGED:
        "\nCan't open a FLAGGED cell! Unflag it first!",
        Move.Invalid.CANT_OPEN_NUMBER:
        "\nCan't open a NUMBER cell!",
        Move.Invalid.CANT_OPEN_EMPTY:
        "\nCan't open an EMPTY cell!",
        Move.Invalid.CANT_TOGGLE_NUMBER:
        "\nCan't toggle flag of a NUMBER cell!",
        Move.Invalid.CANT_TOGGLE_EMPTY:
        "\nCan't toggle flag of an EMPTY cell!",
        Move.Invalid.CAN_ONLY_CHORD_NUMBER_CELLS:
        "\nCan only chord NUMBER cells.",
        Move.Invalid.CANT_CHORD_WITH_INVALID_FLAG_ADJ:
        "\nCan only chord when the number of adjacent flags is equal to the " +
        "number.",
    }
