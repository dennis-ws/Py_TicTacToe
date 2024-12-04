# temp comment for now until the logic for the game is finished
#import pygame
from typing import Union

winning_triad = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),    # Rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),    # Columns
    (0, 4, 8), (2, 4, 6)                # Diagonals
]

# Board (serves as GUI mostly)
class Board():
    def __init__(self):
        pass

# Controller
class Game():
    def __init__(self):
        self.board_state = [None] * 9
        self.board = Board()
        self.turn = 'O'
        self.draw = False

    def play(self):
        while True:
            # Get valid user input
            user_input = self.get_input()
            self.add_input(user_input)
            # Check for winner
            if self.check_winner():
                break
            # Check for draw
            if self.check_draw():
                break
            # Pass the turn over
            self.pass_turn()
        # Check if we have drawn
        if self.has_draw():
            # Announce draw
            self.announce_draw()
        else:
            # Announce winner
            self.announce_winner()

    def has_draw(self) -> bool:
        return self.draw

    def check_draw(self ) -> bool:
        if None not in self.get_board():
            self.draw = True
            return True
        return False

    def announce_draw(self):
        print("DRAW")

    def announce_winner(self):
        print("WINNER:", self.get_turn())
    
    def pass_turn(self):
        if self.get_turn() == 'O':
            self.turn = 'X'
        else:
            self.turn = 'O'

    def check_winner(self) -> bool:
        # Get the current turn player's board
        board = self.get_board()
        for triad in winning_triad:
            if board[triad[0]] == board[triad[1]] == board[triad[2]] and board[triad[0]] != None:
                return True
        return False

    def add_input(self, user_input: int):
        # Add the user input into the board
        self.board_state[user_input] = self.get_turn()

    def get_turn(self) -> str:
        return self.turn
    
    def get_input(self) -> int:
        while True:
            # Get user input
            move = input("Enter move: ")
            # Check user input
            valid_tuple = self.valid_input(move)
            # If user input is not valid, continue
            if valid_tuple is None:
                print("Invalid Input! Type a valid integer between 0 and 8 inclusive")
            else:
                break

        return valid_tuple


    def valid_input(self, user_input: str) -> Union[None, int]:
        # Check the length of the inputs
        if len(user_input) != 1:
            return None
        
        try:
            # Attempt to convert parts into int
            num = int(user_input)
        except ValueError:
            return None # Conversion failed
        
        # Check the row and col
        if not (0 <= num <= 8):
            return None
    
        # Check if the row and col is taken
        if self.get_board()[num] is not None:
            return None
        return num
    
    def get_board(self) -> tuple[Union[None, str]]:
        return self.board_state

if __name__ == "__main__":
    game = Game()
    game.play()