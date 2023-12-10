import pygame
import sys
from cell import Cell
from calcs import measure_distance

""" This is the main file you work on for the project"""

pygame.init()

SCREEN_MIN_SIZE = 750  # Can be made to autoadjust after % of ur screen
amount_of_cells = 16  # The amount of cells is equal in rows and columns, 16x16 (LOCKED)
bomb_chance = 0.25  # Change to prefered value or use default 0.25

CELL_SIZE = SCREEN_MIN_SIZE // amount_of_cells  # how large can each cell be?
READJUSTED_SIZE = CELL_SIZE * amount_of_cells
CELL_WIDTH = CELL_HEIGHT = CELL_SIZE  # Probably not needed, just use cell_size

SCREEN_WIDTH, SCREEN_HEIGHT = READJUSTED_SIZE, READJUSTED_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("MineSweeper")

cells = []


def create_cells():
    for a_row in range(amount_of_cells):
        row = []
        for a_column in range(amount_of_cells):
            x = a_column * CELL_SIZE
            y = a_row * CELL_SIZE
            cell = Cell(x, y, CELL_SIZE, CELL_SIZE, bomb_chance)
            row.append(cell)
        cells.append(row)
        


def draw_cells():
    for row in cells:
        for cell in row:
            cell.draw(screen)


def draw():
    draw_cells()


def event_handler(event):
    if event.type == pygame.QUIT:
        terminate_program()
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  # Left mouse button
            x, y = event.pos
            column = x // CELL_SIZE
            row = y // CELL_SIZE

            if not cells[row][column].selected: # Mark as a clicked cell
                cells[row][column].reveal()

                if cells[row][column].is_bomb():  # When a bomb is clicked
                    print("You clicked on a bomb.")
                    #terminate_program()
        elif event.button == 3:  # Right mouse button to add a flag (3 for pygame)
            x, y = event.pos
            column = x // CELL_SIZE
            row = y // CELL_SIZE

            if not cells[row][column].selected: # Disable flag adding on clicked cells
                cells[row][column].flag = not cells[row][column].flag


def find_neighbouring_bombs():
    for row in range(amount_of_cells):
        for column in range(amount_of_cells):
            count = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= row + i < amount_of_cells and 0 <= column + j < amount_of_cells:
                        count += cells[row + i][column + j].is_bomb()
            cells[row][column].set_neighbouring_bombs(count)


def run_setup():
    create_cells()
    find_neighbouring_bombs()


def terminate_program():
    pygame.quit()
    sys.exit()


def main():
    run_setup()

    while True:
        for event in pygame.event.get():
            event_handler(event)

        draw()
        pygame.display.flip()

    terminate_program()


if __name__ == "__main__":
    main()
