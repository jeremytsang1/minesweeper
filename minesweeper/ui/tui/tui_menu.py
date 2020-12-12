class TUIMenu():
    """Menu for Terminal User Interface.

    """
    PROMPT_APPEARANCE = "\n{}\n> "

    def __init__(self, prompts, actions):
        self.prompts = prompts
        self.actions = actions

    def format_prompts(self, offset=1):
        """Concatenate menu options into a single multiline string.

        Parameters
        ----------
        descriptions: iterable of str
            Descriptions for individual menu options.
        offset: int
            Number to start menu options on.

        Returns
        -------
        str
            One description per line with an extra line for the prompt for the
            user to enter their choice.

        """

        return "\n" + '\n'.join(
            [f'{i + offset}. {line}' for i, line in enumerate(self.prompts)]
            + ["> "]
        )

    @staticmethod
    def read_menu_option(menu):
        return TUIMenu.read_int(TUIMenu.make_menu_str(menu), 1, len(menu) + 1)

    @staticmethod
    def read_int(self, msg, min_val, max_val):
        usr_input = None
        while usr_input is None:
            try:
                usr_input = int(input(TUIMenu.PROMPT_APPEARANCE.format(msg)))
                usr_input = TUIMenu.validate_range(usr_input, min_val, max_val)
            except ValueError:
                print("\nPlease enter an integer!")
                usr_input = None
        return usr_input

    @staticmethod
    def validate_range(val, min_val, max_val):
        if val in range(min_val, max_val):
            return val
        else:
            print(
                "\nPlease enter an int in the interval",
                TUIMenu.make_range_string(min_val, max_val)
            )

            return None

    @staticmethod
    def make_range_string(min_val, max_val):
        return f"[{min_val} (inclusive) ... {max_val} (exclusive)]"
