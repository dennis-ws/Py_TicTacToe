winning_triad = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],    # Rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8],    # Columns
    [0, 4, 8], [2, 4, 6]                # Diagonals
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
        self.winner = None

    def play(self):
        while not self.has_winner():
            # We do something
            break

    def has_winner(self) -> bool:
        if self.winner:
            return True
        return False

if __name__ == "__main__":
    game = Game()
    game.play()