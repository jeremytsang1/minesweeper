import pygame
import pygame_menu
from minesweeper.ui.gui.main_menu import MainMenu
from minesweeper.ui.gui.custom_level_menu import CustomLevelMenu
from minesweeper.game.difficulty import Difficulty
from minesweeper.ui.gui.status_icon import StatusIcon
from minesweeper.ui.gui.gui_board import GUIBoard
from minesweeper.game.game import Game
import os


class GUI():
    # Mouse event buttons
    MOUSE_LEFT = 1
    MOUSE_MIDDLE = 2
    MOUSE_RIGHT = 3
    SCREEN_FILL_COLOR = '#21516a'

    # Directories and paths
    DIR_SOUND = os.path.join('assets', 'sound')
    DIR_END_GAME = os.path.join(DIR_SOUND, 'end_game')
    SOUNDS = {
        'explosion': os.path.join(DIR_END_GAME, 'rumble.ogg'),
        'win': os.path.join(DIR_END_GAME, 'win_sound.ogg'),
    }

    # Component Heights
    STATUS_HEIGHT = 100

    # Spacings between components
    ABOVE_STATUS = 10
    BETWEEN_STATUS_AND_BOARD = 10

    def __init__(self, sound_on=False):
        pygame.init()
        self.sound_on = sound_on
        self.sounds = self.load_sounds() if self.sound_on else None
        self.difficulty = Difficulty()
        self.game = None
        self.status_icon = None
        self.gui_board = None
        self.screen = pygame.display.set_mode((MainMenu.WIDTH,
                                               MainMenu.HEIGHT))
        self.theme = self.create_theme()
        self.main_menu = MainMenu(self.set_difficulty, self.press_play_button, self.theme)
        self.custom_level_menu = None
        self.preset = True  # Starts off as EASY which is one of the presets.
        self.all_sprites = pygame.sprite.Group()

    def load_sounds(self):
        return {
            name: pygame.mixer.Sound(self.SOUNDS[name]) for name in self.SOUNDS
        }

    @staticmethod
    def create_theme():
        theme = pygame_menu.themes.THEME_BLUE
        theme.menubar_close_button = False
        return theme

    def set_difficulty(self, description, level):
        self.preset = self.difficulty.set_difficulty(level)

    def run_main_menu(self):
        self.screen = pygame.display.set_mode((MainMenu.WIDTH,
                                               MainMenu.HEIGHT))
        self.main_menu.show_menu(self.screen)

    def press_play_button(self):
        if not self.preset:
            self.ask_user_for_custom_settings()
        else:
            self.run_game()

    def run_game(self):
        self.game = None
        dimensions = self.determine_screen_size()
        self.screen = pygame.display.set_mode(dimensions)
        self.create_components()
        self.main_game_loop()

    def determine_screen_size(self):
        board_width, board_height = GUIBoard.compute_dimensions(*self.difficulty.get_shape())
        return [board_width,
                self.ABOVE_STATUS
                + self.STATUS_HEIGHT
                + self.BETWEEN_STATUS_AND_BOARD
                + board_height]

    def create_components(self):
        """Needs to be run after creating self.screen."""
        screen_size = self.screen.get_size()

        self.status_icon = StatusIcon(
            # NOTE: Since status icon is a square it's height and width are
            # EQUAL
            x=(screen_size[0] // 2) - self.STATUS_HEIGHT // 2,  # center the icon
            y=self.ABOVE_STATUS,
            width=self.STATUS_HEIGHT,
            height=self.STATUS_HEIGHT)   # Make it a square.
        self.all_sprites.add(self.status_icon)

        self.gui_board = GUIBoard(
            *self.difficulty.get_shape(),
            offset_x=0,
            offset_y=self.ABOVE_STATUS + self.STATUS_HEIGHT + self.BETWEEN_STATUS_AND_BOARD,
        )
        self.add_sprites(self.gui_board.get_sprites())

    def main_game_loop(self):
        running = True

        while running:
            for event in pygame.event.get():
                if self.is_game_active() and event.type == pygame.MOUSEBUTTONUP:
                    self.process_click(event)
                if self.is_game_active() and event.type == pygame.MOUSEBUTTONDOWN:
                    self.status_icon.load_image(StatusIcon.Status.MOUSE_DOWN)
                if event.type == pygame.QUIT:  # Go back to main menu
                    self.end_game()
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # Go back to main menu
                        self.end_game()
                        running = False

            # Fill the background color (and thus opened cells since they are
            # clear)
            self.screen.fill(self.SCREEN_FILL_COLOR)

            # Draw all the sprites
            self.all_sprites.draw(self.screen)

            # Use to GUICell.draw() to draw borders around each cell.
            for sprite in self.gui_board.get_sprites():
                sprite.draw(self.screen)

            pygame.display.flip()

    def is_game_active(self):
        """Predicate to check if the game has not been won or lost.

        Returns
        -------
        bool
        """
        if self.game is None:
            return True
        else:
            won, loss = self.game.check_end_game()
            return not won and not loss

    def process_click(self, event):
        for gui_cell in self.gui_board.get_sprites():
            if gui_cell.is_mouse_up(event.pos):
                self.process_mouse_button(event.button, gui_cell)
                break  # don't bother searching other cells if found click

    def process_mouse_button(self, button, gui_cell):
        row_col_pos = gui_cell.get_row_col_pos()
        if button == self.MOUSE_LEFT:
            print(f"{row_col_pos}: attempting to open")
            if self.game is None:
                self.create_game(gui_cell)

            self.open_cell(gui_cell)
        elif button == self.MOUSE_RIGHT:
            print(f"{row_col_pos}: attempting to toggle flag")
            self.toggle_flag(gui_cell)
        elif button == self.MOUSE_MIDDLE:
            print(f"{row_col_pos}: attempting to chord")
            self.chord_cell(gui_cell)
        else:
            print('Irrelevant mouse click')

        if not self.is_game_active():
            self.handle_game_over()
        else:
            self.status_icon.load_image(StatusIcon.Status.ALIVE)

    def handle_game_over(self):
        # Reveal/flag all bombs and reveal incorrect flags.
        self.update_all_cell_appearances()

        won, loss = self.game.check_end_game()

        if won:
            self.status_icon.load_image(StatusIcon.Status.WIN)
            if self.sound_on:
                self.sounds['win'].play()
        elif loss:
            self.status_icon.load_image(StatusIcon.Status.LOSS)
            if self.sound_on:
                self.sounds['explosion'].play()

    def open_cell(self, gui_cell):
        move = self.game.open_cell(*gui_cell.get_row_col_pos())

        if move.is_valid():
            self.update_affected_cell_appearances(move)

    def toggle_flag(self, gui_cell):
        if self.game is None:
            print("No flagging on the first turn!")
        else:
            pos = gui_cell.get_row_col_pos()
            move = self.game.toggle_flag(*pos)
            if move.is_valid():
                self.update_affected_cell_appearances(move)

    def chord_cell(self, gui_cell):
        if self.game is None:
            print("No number cells to chord yet!")
        else:
            pos = gui_cell.get_row_col_pos()
            move = self.game.chord_cell(*pos)
            if move.is_valid():
                self.update_affected_cell_appearances(move)

    def update_affected_cell_appearances(self, move):
        affected_positions = move.get_affected_positions()
        appearances = self.game.get_all_appearances()
        gui_cells_2D = self.gui_board.get_gui_cells_2D()

        for pos in affected_positions:
            row, col = pos
            appearance = appearances[row][col]
            gui_cells_2D[row][col].load_image(appearance)

    def update_all_cell_appearances(self):
        appearances = self.game.get_all_appearances()
        for gui_cell in self.gui_board.get_sprites():
            row, col = gui_cell.get_row_col_pos()
            gui_cell.load_image(appearances[row][col])

    def create_game(self, gui_cell):
        self.game = Game(
            *self.difficulty.get_shape(),
            self.difficulty.get_bomb_count(),
            *gui_cell.get_row_col_pos()
        )

    def add_sprites(self, sprites):
        for sprite in sprites:
            self.all_sprites.add(sprite)

    def ask_user_for_custom_settings(self):
        self.custom_level_menu = CustomLevelMenu(
            self.difficulty,
            self.run_game,
            self.theme,
            self.screen
        )
        self.custom_level_menu.show_menu()
        del self.custom_level_menu
        self.custom_level_menu = None

    def end_game(self):
        self.game = None

        self.status_icon.kill()
        self.status_icon = None

        self.gui_board.kill_gui_board()
        self.gui_board = None

        # Make sure correct difficulty is selected if user does not
        # alter the selector.
        self.preset = self.main_menu.is_on_a_preset_difficulty()

        self.run_main_menu()


if __name__ == '__main__':
    gui = GUI(True)
    gui.run_main_menu()
