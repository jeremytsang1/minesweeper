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
        self._validate_actions(option_descriptions, actions)
        self.actions = actions

    @staticmethod
    def _validate_actions(options_descriptions, actions):
        if len(options_descriptions) != len(actions):
            raise ValueError(
                "`options_descriptions` and `actions` length mismatch"
            )

        for action in actions:
            if not callable(action):
                raise ValueError("`actions` contains a non-callable element")

    def run_action_for_user_option(self, offset=1):
        """Call the action function specified by the user's menu choice.

        Parameters
        ----------
        offset: int
            Number to start displaying menu options from.

        Returns
        -------
        Dependent on the function for the option the user calls.

        """
        # Subtract offset to account for difference in prentation option number
        # and index that lists start counting from (i.e. index 0).
        user_option = self.ask_user_option(offset) - offset
        return self.actions[user_option]()


if __name__ == '__main__':
    menu = ActionMenu(['foo', 'bar', 'baz'], [
        lambda: print('A'),
        lambda: print('B'),
        lambda: print('C'),
    ])
    menu.run_action_for_user_option()
