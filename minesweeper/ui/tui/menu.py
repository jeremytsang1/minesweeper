from minesweeper.ui.tui.io import IO


class Menu():
    """Defines simple text based Menu that allows user to enter an integer value
    for options. Is able to grab the user's choice as an int.

    """
    PROMPT_CHAR = "> "

    def __init__(self, option_descriptions):
        """Creates a text based menu.

        Parameters
        ----------
        option_descriptions: iterable of str
            Lines to display to the user for each option.

        """
        self.option_descriptions = option_descriptions
        self.count = len(option_descriptions)

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
        concatenated_menu_options = "\n"

        for raw_num, option_description in enumerate(self.option_descriptions):
            option_num = self.format_option_number(raw_num, offset)
            concatenated_menu_options += f'\n{option_num} {option_description}'

        return f'{concatenated_menu_options}\n{self.PROMPT_CHAR} '

    @staticmethod
    def format_option_number(option_num, offset):
        """Determine formatting for the numbering for each menu option.

        Parameters
        ----------
        option_num: int
            Menu option number starting at (start counting at 0).
        offset: int
            Number to start the menu options at.

        Returns
        -------
        str
            Formatted number, in this case of the form "1.", "2.", etc.
        """
        return f'{option_num + offset}.'

    def ask_use_option(self, offset=1):
        """Ask the user for input and perform the selected action once a valid choice
        has been given.

        Parameters
        ----------
        offset: int
            Number to start options from.

        Returns
        -------
        int
            The option number of the option the user chose.

        """
        menu_str = self.format_prompts(offset)
        menu_option = IO.read_int(menu_str, offset, self.count + offset)
        return menu_option


if __name__ == '__main__':
    menu = Menu(['a', 'b', 'c'])
    usr_choice = menu.ask_use_option()
    print(f'usr_choice: {usr_choice}')
