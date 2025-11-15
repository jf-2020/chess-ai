import chess
from typing import Optional
from .player import Player

class ChessGame:
    """Owns the current game state (python-chess Board)."""

    def __init__(self, board: chess.Board | None = None):
        # allow optional injection of an existing board (e.g., for tests or PGN replay)
        self.board = board or chess.Board()

    def legal_moves(self) -> list[chess.Move]:
        """Return a list of legal moves from the current position."""
        return list(self.board.legal_moves)
    
    def apply_move(self, move: chess.Move) - > None:
        """Apply a move to the current board."""
        self.board.push(move)

    def undo_move(self) -> None:
        """Undo the last move."""
        self.board.pop()

    def is_game_over(self) -> bool:
        """Check if the game is over according to chess rules."""
        return self.board.is_game_over()
    
    def result(self) -> str:
        """
        Return the game result in standard notation:
        - '1-0'  : White wins
        - '0-1'  : Black wins
        - '1/2-1/2' : draw
        If the game is not over, python-chess returns '*'.
        """
        return self.board.result()
    
class GameSession:
    """Orchestrates a full game between two players."""

    def __init__(
        self, white_player: Player,
        black_player: Player,
        game: Optional[ChessGame] = None,
    ):
        self.game = game or ChessGame()
        self.white_player = white_player
        self.black_player = black_player

    def current_player(self):
        """
        Determine whose turn it is based on the python-chess board:
        - True  -> White
        - False -> Black
        """
        return self.white_player if self.game.board.turn else self.black_player
    
    def run(self):
        """
        Run a complete game until termination.
        
        Loop:
          - ask a current player for a move
          - apply move
          - stop if game is over or a player returns None
          
        Returns:
          Game result notation: '1-0', '0-1', '1/2-1/2', or '*' if unfinished.
        """
        while not self.game.is_game_over():
            player = self.current_player()
            move = player.choose_move(self.game)

            # Convention: returning None means "I resign / quit"
            if move is None:
                # Optional: decide what result to record for a resignation
                # If current player resigns, opponent wins.
                if player is self.white_player:
                    return "0-1" # White resigns, Black wins
                else:
                    return "1-0" # Black resigns, White wins
                
            # One *could* assert legality here to catch bugs in Player logic:
            # assert move in self.game.legal_moves(), "Illegal move from player"

            self.game.apply_move(move)

        # Normal termination according to chess rules
        return self.game.result()