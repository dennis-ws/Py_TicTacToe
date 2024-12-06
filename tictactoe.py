import pygame # type: ignore
from typing import Union, List
import random
import math

from board import Board
from computer import Computer

# Size and Flags
SIZE = (300, 300)
FLAGS = 0
CELL_SIZE = 100
# Colour
WHITE = (255, 255, 255)
# Winning Triad
winning_triad = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),    # Rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),    # Columns
    (0, 4, 8), (2, 4, 6)                # Diagonals
]

class Computer():
    def __init__(self, difficulty=None):
        self.difficulty = difficulty

    def easy(self, board: List[Union[str, None]]) -> int:
        # Random AI
        available_moves = [i for i, spot in enumerate(board) if spot == None]
        choice = random.choice(available_moves)
        return choice

    def medium(self, board: List[Union[str, None]]):
        # Recursive AI
        choice = self.find_best_move(board)
        return choice

    def minimax(self, board: List[Union[str, None]], depth, maximizing):
        if self.check_winner(board, 'X'):
            return 10 - depth
        if self.check_winner(board, 'O'):
            return depth - 10
        if self.check_draw(board):
            return 0

        if maximizing:
            # AI TURN
            best_score = -math.inf
            for index in range(len(board)):
                if board[index] == None:
                    # Simulate the move
                    board[index] = 'X'
                    score = self.minimax(board, depth + 1, False)
                    # Undo the move
                    board[index] = None
                    best_score = max(best_score, score)
            return best_score
        else:
            # OPPOSING PLAYER TURN
            best_score = math.inf
            for index in range(len(board)):
                if board[index] == None:
                    # Simulate the move
                    board[index] = 'O'
                    score = self.minimax(board, depth + 1, True)
                    # Undo the move
                    board[index] = None
                    best_score = min(best_score, score)
            return best_score

    def find_best_move(self, board: List[Union[str, None]]):
        best_move = -1
        best_value = -math.inf
        for index in range(len(board)):
            if board[index] == None:
                # Simulate move for AI
                board[index] = 'X'
                move_value = self.minimax(board, 0, False)
                # Undo the move
                board[index] = None
                if move_value > best_value:
                    best_value = move_value
                    best_move = index
        return best_move



    def check_winner(self, board: List[Union[str, None]], player: str) -> bool:
        for triad in winning_triad:
            if board[triad[0]] == board[triad[1]] == board[triad[2]] and board[triad[0]] != None and board[triad[0]] == player:
                return True
        return False 

    def check_draw(self, board: List[Union[str, None]]) -> bool:
        if None not in board:
            return True
        return False

    def get_difficulty(self) -> Union[int, None]:
        return self.difficulty

# Controller
class Game():
    def __init__(self, difficulty=None):
        # Initialise pygames
        pygame.init()
        self.board_state = [None] * 9
        self.turn = 'O'
        self.draw = False
        self.winner = False
        self.again = False
        self.computer = Computer(difficulty)
        try:
            self.screen = pygame.display.set_mode(SIZE, FLAGS)
            self.timer = pygame.time.Clock()
            self.fps = 60
            self._run = True
            pygame.display.set_caption("TicTacToe")
            self.board = Board(self.screen)
        except Exception:
            pygame.quit()
            raise

    def playFriends(self):
        while self._run:

            for event in pygame.event.get():
                # If user has clicked mouse 1
                if (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1) and not (self.has_winner() or self.has_draw()):
                    x, y = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE # Convert to between 0 and 2
                    index = x + y * 3 # Calculating the cell index from mouse position
                    if self.add_input(index):
                        # Check for winner
                        self.check_winner()
                        # Check for draw
                        self.check_draw()
                        # Check if we have drawn or won, if not then pass the turn over
                        if self.has_draw():
                            # Announce draw
                            self.GUI() # We are drawing here such that the last move is rendered in before the tkinter box pops up
                            self.announce_draw()
                        elif self.has_winner():
                            # Announce winner
                            self.GUI() # We are drawing here such that the last move is rendered in before the tkinter box pops up
                            self.announce_winner()
                        else:
                            # Pass the turn over
                            self.pass_turn()
                if event.type == pygame.QUIT:
                    self._run = False
            
            # Play Again?
            if self.again:
                self.setup()


            # GUI Shenanigans
            self.GUI()
    
    def playComputer(self):
        while self._run:
            # Check if it is AI turn
            if self.get_turn() == 'X':
                self.do_move()
                # Check for winner
                self.check_winner()
                # Check for draw
                self.check_draw()
                # Check if we have drawn or won, if not then pass the turn over
                if self.has_draw():
                    # Announce draw
                    self.GUI() # We are drawing here such that the last move is rendered in before the tkinter box pops up
                    self.announce_draw()
                elif self.has_winner():
                    # Announce winner
                    self.GUI() # We are drawing here such that the last move is rendered in before the tkinter box pops up
                    self.announce_winner()
                else:
                    # Pass the turn over
                    self.pass_turn()

            for event in pygame.event.get():
                # If user has clicked mouse 1
                if (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1) and not (self.has_winner() or self.has_draw()) and (self.get_turn() == 'O'):
                    x, y = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE # Convert to between 0 and 2
                    index = x + y * 3 # Calculating the cell index from mouse position
                    if self.add_input(index):
                        # Check for winner
                        self.check_winner()
                        # Check for draw
                        self.check_draw()
                        # Check if we have drawn or won, if not then pass the turn over
                        if self.has_draw():
                            # Announce draw
                            self.GUI() # We are drawing here such that the last move is rendered in before the tkinter box pops up
                            self.announce_draw()
                        elif self.has_winner():
                            # Announce winner
                            self.GUI() # We are drawing here such that the last move is rendered in before the tkinter box pops up
                            self.announce_winner()
                        else:
                            # Pass the turn over
                            self.pass_turn()
                if event.type == pygame.QUIT:
                    self._run = False
            
            # Play Again?
            if self.again:
                self.setup()


            # GUI Shenanigans
            self.GUI()
    
    def GUI(self):
        self.timer.tick(self.fps)
        self.screen.fill(WHITE)
        # Draw the board
        self.board.draw_grid()
        self.board.draw_symbol(self.get_board())
        pygame.display.update()

    def do_move(self):
        if self.computer.get_difficulty() == 0:
            choice = self.computer.easy(self.get_board())
            self.add_input(choice)
        elif self.computer.get_difficulty() == 1:
            choice = self.computer.medium(self.get_board())
            self.add_input(choice)

    def setup(self):
        self.board_state = [None] * 9
        self.turn = 'O'
        self.draw = False
        self.winner = False
        self.again = False

    def has_draw(self) -> bool:
        return self.draw

    def has_winner(self) -> bool:
        return self.winner

    def check_draw(self):
        if None not in self.get_board() and not self.has_winner():
            self.draw = True
        return None

    def announce_draw(self):
        self.again = self.board.draw_draw()

    def announce_winner(self):
        self.again = self.board.draw_winner(self.get_turn())
    
    def pass_turn(self):
        if self.get_turn() == 'O':
            self.turn = 'X'
        else:
            self.turn = 'O'

    def check_winner(self):
        # Get the current turn player's board
        board = self.get_board()
        for triad in winning_triad:
            if board[triad[0]] == board[triad[1]] == board[triad[2]] and board[triad[0]] != None:
                self.winner = True
        return None

    def add_input(self, user_input: int) -> bool:
        # Attempt to add the input in, return True if it succeeds else False
        if self.board_state[user_input] == None:
            self.board_state[user_input] = self.get_turn()
            return True
        return False

    def get_turn(self) -> str:
        return self.turn
    
    def get_board(self) -> tuple[Union[None, str]]:
        return self.board_state

if __name__ == "__main__":
    try:
        friends = int(input("0: AI\nNon-Zero: Friends\nInput: "))
        if friends:
            game = Game()
            game.playFriends()
        else:
            difficulty = int(input("0: Easy\n1: Medium\n2: Impossible\nInput: "))
            game = Game(difficulty)
            game.playComputer()

    except ValueError:
        print("Input 0 or 1 pls")