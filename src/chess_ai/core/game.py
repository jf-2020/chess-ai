import chess

class ChessGame:
    """Owns the current game state (python-chess Board)."""

    def __init__(self):
        self.board = chess.Board()

    def legal_moves(self):
        return list(self.board.legal_moves)
    
    def apply_move(self, move):
        self.board.push(move)

    def undo_move(self):
        self.board.pop()

    def is_game_over(self):
        return self.board.is_game_over()
    
    def result(self):
        return self.board.result()
    
    class GameSession:
        """Orchestrates a full game between two players."""

        def __init__(self, white_player, black_player, game=None):
            self.game = game or ChessGame()
            self.white_player = white_player
            self.black_player = black_player

        def current_player(self):
            return self.white_player if self.game.board.turn else self.black_player
        
        def run(self):
            # loop until game over, calling player.choose_move(self.game)
            pass