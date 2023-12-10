import pygame
import random


class Cell:
    """This file contains the cell class representing each square in the game"""

    def __init__(self, x, y, width, height, bomb_chance):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (0, 64, 0)  # RGB color
        self.cell_thickness = 2
        self.neighbouring_bombs = 0
        self.selected = False
        self.flag = False   # For flag adding on Right click
        self.cell_center = (
            self.x + self.width // 2,
            self.y + self.width // 2,
        )  # useful for drawing
        self.bomb = (
            random.random() < bomb_chance
        )  # each cell has a chance of being a bomb

    

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), self.cell_thickness)

        if self.selected:
            if not self.bomb:
                font = pygame.font.Font(None, 36)
                text = font.render(str(self.neighbouring_bombs), True, (0, 255, 0))
                text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
                screen.blit(text, text_rect)
            else:
                font = pygame.font.Font(None, 36)
                text = font.render("X", True, (255, 0, 0)) # Add X on cell if there is a bomb
                text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
                screen.blit(text, text_rect)

        if self.flag:
        # Draw a flag
            pygame.draw.polygon(screen, (255, 0, 0), [(self.x + self.width // 2, self.y), (self.x + self.width, self.y + self.height // 4), (self.x + self.width // 2, self.y + self.height // 2)])

                
    def reveal(self):
        self.selected = True

    def is_bomb(self):
        return self.bomb

    def set_neighbouring_bombs(self, count):
        self.neighbouring_bombs = count