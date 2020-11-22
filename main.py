# Filename    : main.py
# Author      : Jeremy Tsang
# Date        : 2020-11-22
# Description : Driver for minesweeper game. Currently only running text based
#               version.

from minesweeper.ui.tui.terminal_ui import TerminalUI


def main():
    ui = TerminalUI()
    ui.start_game()


if __name__ == '__main__':
    main()
