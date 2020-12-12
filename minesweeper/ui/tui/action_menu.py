from minesweeper.ui.tui.menu import Menu


class ActionMenu(Menu):
    """Menu that can call functions for each of its options.

    """
    def __init__(self, option_descriptions, actions):
        """Creates new object of type ActionMenu.

        Parameters
        ----------
        option_descriptions: iterable of str
            Lines to display to the user for each option.
        actions: iterable of callable
            Actions to perform for each of the menu options. Must be same
            length as `option_descriptions`.

        """
        super().__init__(option_descriptions)
        self.actions = actions


if __name__ == '__main__':
    menu = ActionMenu(['foo', 'bar', 'baz'], [])
    usr = menu.ask_use_option()
    print(f'usr: {usr}')
