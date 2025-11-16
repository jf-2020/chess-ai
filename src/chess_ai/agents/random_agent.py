import random
from chess import Move
from chess_ai.core.game import ChessGame
from chess_ai.core.player import Player

class RandomAgent(Player):
    def choose_move(self, game: ChessGame) -> Move | None:
        moves = game.legal_moves()
        return random.choice(moves) if moves else None