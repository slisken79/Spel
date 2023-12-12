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
    for a_row in range(amount_of_cells):  # Iterate through each row in the game board
        row = [] # Initialize an empty list to represent a row of cells
        for a_column in range(amount_of_cells):  # Iterate through each column in the current row
            x = a_column * CELL_SIZE   # Calculate the x, y coordinates for the current cell based on CELL_SIZE
            y = a_row * CELL_SIZE
            cell = Cell(x, y, CELL_SIZE, CELL_SIZE, bomb_chance)  # Create a new Cell instance
            row.append(cell)  # Append the newly created cell to the current row
        cells.append(row)   # Append the row to the cells list
        


def draw_cells():
    for row in cells:  # Iterate through each row in the game board
        for cell in row:  # Iterate through each cell in the current row
            cell.draw(screen)   # Call the draw method from the Cell class to render it on the screen


def draw():
    draw_cells()   # Call the draw_cells function to render the game board on the screen


def event_handler(event):
    if event.type == pygame.QUIT:  # Check if the quit event is triggered
        terminate_program()
    elif event.type == pygame.MOUSEBUTTONDOWN:  # Check if a mouse button is pressed down
        if event.button == 1:  # Left mouse button
            x, y = event.pos   # Get the x, y coordinates of the mouse click
            column = x // CELL_SIZE    # Determine the column and row of the clicked cell based on the CELL_SIZE
            row = y // CELL_SIZE

            if not cells[row][column].selected: # Check if the cell has not been clicked before
                cells[row][column].reveal()

                if cells[row][column].is_bomb():  # When a bomb is clicked
                    print("You clicked on a bomb.")
                    #terminate_program()
        elif event.button == 3:  # Right mouse button to add a flag (3 for pygame)
            x, y = event.pos  # Get the x, y coordinates of the mouse right-click
            column = x // CELL_SIZE
            row = y // CELL_SIZE

            if not cells[row][column].selected: # Check if the cell has not been clicked before
                cells[row][column].flag = not cells[row][column].flag # Enable flag adding on right-click


def is_valid_position(row, column):
    return 0 <= row < amount_of_cells and 0 <= column < amount_of_cells

def count_bombs_around(row, column):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue  # Skip the current cell
            new_row, new_column = row + i, column + j
            if is_valid_position(new_row, new_column):
                count += cells[new_row][new_column].is_bomb()
    return count

def find_neighbouring_bombs():
    for row in range(amount_of_cells):
        for column in range(amount_of_cells):
            count = count_bombs_around(row, column)
            cells[row][column].set_neighbouring_bombs(count)


def run_setup():
    create_cells()   # Create the game board cells
    find_neighbouring_bombs()  # Find and set the count of neighbouring bombs for each cell


def terminate_program():
    pygame.quit()   # Quit the Pygame module
    sys.exit()      # Exit the program


def main():
    run_setup()   # Run the initial setup for the game

    while True:  # Main game loop
        for event in pygame.event.get():   # Process events
            event_handler(event)

        draw()   # Draw the game state on the screen
        pygame.display.flip()  # Update the display

    terminate_program()   


if __name__ == "__main__":
    main()
