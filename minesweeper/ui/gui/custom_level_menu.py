import pygame
import pygame_menu
from minesweeper.ui.gui.difficulty import Difficulty


class CustomLevelMenu():
    MENU_TITLE = 'Custom Game'
    WIDTH = 625
    HEIGHT = 300

    KEYS = ['rows', 'cols', 'bomb_count']

    MINIMUMS = {
        'rows': 10,
        'cols': 10,
        'bomb_count':,
    }

    LABELS = {
        'rows': 'Rows',
        'cols': 'Cols',
        'bomb_count': 'Bomb Count',
    }

    def __init__(self, difficulty, run_game, theme, screen):
        self.difficulty = difficulty
        self.run_game = run_game
        self.theme = theme
        self.screen = screen
        self.menu = self.create_menu()
        self.error_menu = None
        self.configure_menu()

    def create_menu(self):
        return pygame_menu.Menu(
            width=CustomLevelMenu.WIDTH,
            height=CustomLevelMenu.HEIGHT,
            title=CustomLevelMenu.MENU_TITLE,
            theme=self.theme,
        )

    def configure_menu(self):
        keys = ['rows', 'cols', 'bomb_count']
        for key in keys:
            self.menu.add_text_input(
                title=f"{self.LABELS[key]}: ",
                default=10,
                textinput_id=key
            )

        self.menu.add_button(title='Submit', action=self.submit)

    def configure_error_menu(self, msg):
        error_menu = pygame_menu.Menu(
            width=CustomLevelMenu.WIDTH,
            height=CustomLevelMenu.HEIGHT,
            title="Invalid Input!",
            theme=self.theme,
        )
        error_menu.add_label(msg)
        error_menu.add_button(title='OK', action=self.show_menu)
        return error_menu

    def show_menu(self):
        self.menu.mainloop(self.screen)

    def submit(self):
        input_data = self.menu.get_input_data()
        valid, msg = self.validate_input_data(input_data)
        if valid:
            self.difficulty.configure_game_params(self.cast_input(input_data))
            self.run_game()
        else:
            self.error_menu = self.configure_error_menu(msg)
            self.error_menu.mainloop(self.screen)
            del self.error_menu
            self.error_menu = None

    def validate_input_data(self, input_data):
        for key in input_data:
            try:
                int(input_data[key])
            except ValueError:
                return False, "All input must be integers!"

        casted = {key: int(input_data[key]) for key in input_data}

        # Check minimums
        for key in casted:
            if casted[key] < self.MINIMUMS[key]:
                return (False,
                        f'{self.LABELS[key]} must be'
                        f' greater than {self.MINIMUMS[key]}')

        # Check maximum
        max_bomb_count = casted['rows'] * casted['cols']
        if casted['bomb_count'] >= max_bomb_count:
            return (False,
                    f'{self.LABELS["bomb_count"]} cannot be more '
                    f'than {max_bomb_count - 1}')

        return True, None

    def cast_input(self, input_data):
        return [int(input_data[key]) for key in self.KEYS]


if __name__ == '__main__':
    def run_game():
        print("hello")

    def create_theme():
        theme = pygame_menu.themes.THEME_SOLARIZED
        theme.menubar_close_button = False
        return theme

    pygame.init()
    screen = pygame.display.set_mode((CustomLevelMenu.WIDTH,
                                      CustomLevelMenu.HEIGHT))
    diff = Difficulty()
    menu = CustomLevelMenu(diff, run_game, create_theme(), screen)
    menu.show_menu()
