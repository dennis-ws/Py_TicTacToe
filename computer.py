from typing import List, Union
import math
import random

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