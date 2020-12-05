import pygame
import pygame_menu

pygame.init()
screen = pygame.display.set_mode((625, 300))


def set_difficulty(value, difficulty):
    pass


def start_the_game():
    pass


theme = pygame_menu.themes.THEME_SOLARIZED
theme.menubar_close_button = False

menu = pygame_menu.Menu(
    height=300,
    width=625,
    title='CS 325 Fall 2020: Minesweeper',
    theme=theme,
)

menu.add_selector(
    title='Difficulty: ',
    items=[
        ("EASY", 1),
        ("MEDIUM", 2),
        ("HARD", 3),
        ("CUSTOM", 4),
    ],
    onchange=set_difficulty
)
menu.add_button(title='Play', action=start_the_game)
menu.add_button(title='Quit', action=pygame_menu.events.EXIT)


menu.mainloop(screen)