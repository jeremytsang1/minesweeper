# Filename    : main.py
# Author      : Jeremy Tsang
# Date        : 2020-11-22
# Description : Driver for minesweeper game. Currently only running text based
#               version.

from minesweeper.ui.tui.terminal_ui import TUI


def main():
    ui = TUI()
    ui.start_main_menu()


if __name__ == '__main__':
    main()
