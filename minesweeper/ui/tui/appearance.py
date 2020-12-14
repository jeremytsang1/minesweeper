from minesweeper.game.cell import Cell

class AppearanceTranslator():
    """Symbols to print for each Cell.Appearance.

    """
    {
        Cell.Appearance.FLAG: 'F',
        Cell.Appearance.EMPTY: ' ',
        Cell.Appearance.UNOPENED: '?',
        Cell.Appearance.FLAG_INCORRECT: '#',
        Cell.Appearance.UNENCOUNTERED_BOMB: '*',
        Cell.Appearance.OPENED_BOMB: '!',

     }
