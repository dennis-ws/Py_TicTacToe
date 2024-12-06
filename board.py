import tkinter as tk
from tkinter import messagebox
import pygame # type: ignore
from typing import Union

# Colours
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
# Size
CELL_SIZE = 100

# Board (serves as GUI mostly)
class Board():
    def __init__(self, screen: pygame):
        self._screen = screen
        self.font = pygame.font.Font(None, 100)

    def draw_grid(self):
        alt = True
        for row in range(3):
            for col in range(3):
                if alt:
                    pygame.draw.rect(self._screen, WHITE, [col * 100, row * 100, CELL_SIZE, CELL_SIZE])
                else:
                    pygame.draw.rect(self._screen, GRAY, [col * 100, row * 100, CELL_SIZE, CELL_SIZE])
                alt = not alt

    def draw_symbol(self, board: tuple[Union[None, str]]):
        i = 0
        for row in range(3):
            for col in range(3):
                area = board[i]
                if area != None:
                    text = self.font.render(area, True, BLACK)
                    # Get the center of the cell
                    text_rect = text.get_rect(center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))
                    self._screen.blit(text, text_rect)
                i += 1

    def draw_winner(self, winner: str) -> bool:
        root = tk.Tk()
        root.withdraw()

        response = messagebox.askyesno("Winner!", "Player {player} won!\nDo you want to play again?".format(player=winner))
        root.quit()
        
        if response:
            return True
        else:
            return False
        

    def draw_draw(self) -> bool:
        root = tk.Tk()
        root.withdraw()

        response = messagebox.askyesno("Draw!", "Draw!\nDo you want to play again?")
        root.quit()
        
        if response:
            return True
        else:
            return False
