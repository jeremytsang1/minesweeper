import pygame
from minesweeper.ui.gui.gui_cell import GUICell
from minesweeper.game.cell import Cell


appearances = [key for key in GUICell.IMAGES.keys()]
appearance_idx = 0

# Import and initialize the pygame library

pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([1000, 1000])


# Make the cell
cell = GUICell(0, 0)
all_sprites = pygame.sprite.Group()
all_sprites.add(cell)

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_n:
                appearance_idx = (appearance_idx + 1) % len(appearances)
                cell.load_image(appearances[appearance_idx])
                GUICell.IMAGES[appearances[appearance_idx]]['filename']
            elif event.key == pygame.K_p:
                appearance_idx = (appearance_idx - 1) % len(appearances)
                cell.load_image(appearances[appearance_idx])


    # Fill the background with white
    screen.fill("#fdfdfd")

    # Draw the cells
    all_sprites.draw(screen)


    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
