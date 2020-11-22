from minesweeper.ui.tui.command_line_grid import CommandLineGrid


class TablePrinter():
    """Class to print 2D tables

    """
    @staticmethod
    def makeTable(itr_2d):
        shape = CommandLineGrid.get_shape(itr_2d, 0)

        grid = CommandLineGrid(*shape, TablePrinter.get_longest_len(itr_2d))
        return grid.make_table_from_itr_2d(itr_2d)

    @staticmethod
    def get_longest_len(itr_2d):
        longest = len(str(itr_2d[0][0]))
        for row in itr_2d:
            for elt in itr_2d:
                if longest < len(str(elt)):
                    longest = len(str(elt))
        return longest
