import pygame
import pygame_menu
from minesweeper.game.difficulty import Difficulty as diff


class MainMenu():
    """Menu GUI.
    """
    MENU_TITLE = 'CS 325 Fall 2020: Minesweeper'
    SELECTOR_KEY = 'difficulty'
    WIDTH = 625
    HEIGHT = 300

    def __init__(self, difficulties, start_game, theme):
        """Creates a new main menu window for starting a new game or quitting.

        Parameters
        ----------
        difficulty: function
            Function dictating how to change the difficulty of the game.
        start_game: function
            Function dictating how to start playing a new instance of the game.
        width: int
            Number of pixels for width of window.
        height: int
            Number of pixels for height of window.

        Returns
        -------
        MenuWindow()

        """
        self.difficulties = difficulties
        self.start_game = start_game
        self.theme = theme
        self.menu = self.create_menu()
        self.configure_menu()


    def create_menu(self):
        return pygame_menu.Menu(
            width=MainMenu.WIDTH,
            height=MainMenu.HEIGHT,
            title=MainMenu.MENU_TITLE,
            theme=self.theme,
        )

    def configure_menu(self):
        self.menu.add_selector(
            title='Difficulty: ',
            items=[
                ("EASY", diff.Level.EASY),
                ("MEDIUM", diff.Level.MEDIUM),
                ("HARD", diff.Level.HARD),
                ("CUSTOM", diff.Level.CUSTOM),
            ],
            onchange=self.difficulties,
            selector_id=self.SELECTOR_KEY,
        )
        self.menu.add_button(title='Play', action=self.start_game)
        self.menu.add_button(title='Quit', action=pygame_menu.events.EXIT)

    def show_menu(self, screen):
        self.menu.mainloop(screen)

    def is_on_a_preset_difficulty(self):
        difficulty_str, _ = self.menu.get_input_data()[self.SELECTOR_KEY]
        return difficulty_str != "CUSTOM"


if __name__ == '__main__':
    def set_difficulty(description, difficulty):
        print(f'{description}: {difficulty}')

    def start_the_game():
        print("Starting the game!")

    pygame.init()
    menu = MainMenu(set_difficulty, start_the_game)
    menu.show_menu()
