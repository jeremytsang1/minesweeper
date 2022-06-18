#!/usr/bin/env python3

# Filename    : main.py
# Author      : Jeremy Tsang
# Date        : 2020-11-22
# Description : Driver for minesweeper game. Currently only running text based
#               version.
from minesweeper.ui.tui.menus.action_menu import ActionMenu
from minesweeper.ui.tui.terminal_ui import TUI
from minesweeper.ui.gui.graphical_ui import GUI


def main():
    play_mode_menu()


def play_mode_menu():
    action_menu = ActionMenu(("Play in TUI (text mode) ",
                              "Play in GUI (graphical mode)",
                              "Quit"),
                             (run_tui,
                              run_gui,
                              quit_game))

    action_menu.run_action_for_user_option()


def run_tui():
    print("\nStarting in TUI mode.")
    tui = TUI()
    tui.start()


def run_gui():
    def choose_settings(sound_on):
        def run_with_specific_settings():
            gui = GUI(sound_on)
            gui.run_main_menu()

        return run_with_specific_settings

    print("\nStarting in GUI mode.")

    action_menu = ActionMenu(("sound on",
                              "Sound off (required for repl.it)"),
                             (choose_settings(sound_on=True),
                              choose_settings(sound_on=False)))

    action_menu.run_action_for_user_option()


def quit_game():
    print("\nBye! Have a nice day!")


if __name__ == '__main__':
    main()
