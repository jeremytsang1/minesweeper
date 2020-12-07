# Filename    : main.py
# Author      : Jeremy Tsang
# Date        : 2020-11-22
# Description : Driver for minesweeper game. Currently only running text based
#               version.

from minesweeper.ui.tui.terminal_ui import TUI
from minesweeper.ui.gui.graphical_ui import GUI


def main():
    play_mode_menu()


def play_mode_menu():
    menu_options = {
        1: run_tui,
        2: run_gui,
        3: quit_game,
    }
    usr_input = None

    while usr_input not in menu_options:
        usr_input = input(get_menu_options())
        try:
            usr_input = int(usr_input)
            if usr_input not in menu_options:
                print("\nPlease choose an appropriate menu option!")
        except ValueError:
            print("\nPlease enter an integer!")

    menu_options[usr_input]()


def get_menu_options():
    return (
        "\n1. Play in TUI (text mode) "
        "\n2. Play in GUI (graphical mode)"
        "\n3. Quit"
        "\n> "
    )


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
