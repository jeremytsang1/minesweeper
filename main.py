# Filename    : main.py
# Author      : Jeremy Tsang
# Date        : 2020-11-22
# Description : Driver for minesweeper game. Currently only running text based
#               version.

from minesweeper.ui.tui.terminal_ui import TUI
from minesweeper.ui.gui.graphical_ui import GUI


def main():
    play_mode_menu()


def get_input(prompts):
    """Given a list of prompts asks the user to input one of the them (by index).

    Parameters
    ----------
    prompts: iterable of str
        Descriptions of menu options to display to user.

    Returns
    -------
    int
        The user's choice.
    """
    usr_input = None
    option_numbers = range(len(prompts))
    menu_str = format_prompts(prompts)

    while usr_input not in option_numbers:
        usr_input = input(menu_str)
        try:
            usr_input = int(usr_input)
            if usr_input not in option_numbers:
                print("\nPlease choose an appropriate menu option!")
        except ValueError:
            print("\nPlease enter an integer!")

    return usr_input


def format_prompts(descriptions):
    """Concatenate menu options into a single multiline string.

    Parameters
    ----------
    descriptions: iterable of str
        Descriptions for individual menu options.

    Returns
    -------
    str
        One description per line with an extra line for the prompt for the user
        to enter their choice.

    """
    return '\n'.join(
        [f'{i}. {description}' for i, description in enumerate(descriptions)]
        + ["> "])


def play_mode_menu():
    ACTION = 'action'
    DESCRIPTION = 'description'
    menu_options = (
        {ACTION: run_tui,
         DESCRIPTION: "Play in TUI (text mode) "},
        {ACTION: run_gui,
         DESCRIPTION: "Play in GUI (graphical mode)"},
        {ACTION: quit_game,
         DESCRIPTION: "Quit"},
    )
    usr_input = get_input([option[DESCRIPTION] for option in menu_options])
    menu_options[usr_input][ACTION]()


def run_tui():
    print("\nStarting in TUI mode.")
    tui = TUI()
    tui.run_main_menu()


def run_gui():
    print("\nStarting in GUI mode.")
    gui = GUI()
    gui.run_main_menu()


def quit_game():
    print("\nBye! Have a nice day!")


if __name__ == '__main__':
    main()
