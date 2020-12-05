import pygame
import pygame_menu


class MainMenu():
    """Menu GUI.
    """
    MENU_TITLE = 'CS 325 Fall 2020: Minesweeper'

    def __init__(self, difficulties, start_game, width=625, height=300):
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
        self.WIDTH = width
        self.HEIGHT = height
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.theme = self.create_theme()
        self.menu = self.create_menu()
        self.configure_menu()

    def create_theme(self):
        theme = pygame_menu.themes.THEME_SOLARIZED
        theme.menubar_close_button = False
        return theme

    def create_menu(self):
        return pygame_menu.Menu(
            width=self.WIDTH,
            height=self.HEIGHT,
            title=MainMenu.MENU_TITLE,
            theme=self.theme,
        )

    def configure_menu(self):
        self.menu.add_selector(
            title='Difficulty: ',
            items=[
                ("EASY", 1),
                ("MEDIUM", 2),
                ("HARD", 3),
                ("CUSTOM", 4),
            ],
            onchange=self.difficulties
        )
        self.menu.add_button(title='Play', action=self.start_game)
        self.menu.add_button(title='Quit', action=pygame_menu.events.EXIT)

    def show_menu(self):
        self.menu.mainloop(self.screen)


if __name__ == '__main__':
    def set_difficulty(description, difficulty):
        print(f'{description}: {difficulty}')

    def start_the_game():
        print("Starting the game!")

    pygame.init()
    menu = MainMenu(set_difficulty, start_the_game)
    menu.show_menu()
