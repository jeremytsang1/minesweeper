import pygame
import pygame_menu
from minesweeper.ui.gui.difficulty import Difficulty


class CustomLevelMenu():
    MENU_TITLE = 'Custom Game'
    WIDTH = 625
    HEIGHT = 300

    def __init__(self, difficulty, run_game):
        self.difficulty = difficulty
        self.run_game = run_game
        self.theme = self.create_theme()
        self.menu = self.create_menu()
        self.configure_menu()

    def create_theme(self):
        theme = pygame_menu.themes.THEME_SOLARIZED
        theme.menubar_close_button = False
        return theme

    def create_menu(self):
        return pygame_menu.Menu(
            width=CustomLevelMenu.WIDTH,
            height=CustomLevelMenu.HEIGHT,
            title=CustomLevelMenu.MENU_TITLE,
            theme=self.theme,
        )

    def configure_menu(self):
        self.menu.add_text_input('Rows: ', default='10', textinput_id='rows')
        self.menu.add_text_input('Cols: ', default='10', textinput_id='cols')
        self.menu.add_text_input('Bomb Count: ', default='10', textinput_id='bomb_count')
        self.menu.add_button(title='Submit', action=self.submit)

    def show_menu(self, screen):
        self.menu.mainloop(screen)

    def submit(self):
        input_data = self.menu.get_input_data()
        valid, msg = self.validate_input_data(input_data)
        if valid:
            self.difficulty.configure_game_params(self.cast_input(input_data))
            self.run_game()
        else:
            self.show_error_page()

    def validate_input_data(self, input_data):
        pass


if __name__ == '__main__':
    def run_game():
        print("hello")

    pygame.init()
    screen = pygame.display.set_mode((CustomLevelMenu.WIDTH,
                                      CustomLevelMenu.HEIGHT))
    diff = Difficulty()
    menu = CustomLevelMenu(diff, run_game)
    menu.show_menu(screen)
