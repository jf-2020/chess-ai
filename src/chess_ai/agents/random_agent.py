import random
from chess_ai.core.player import Player

class RandomAgent(Player):
    def choose_move(self, game):
        moves = game.legal_moves()
        return random.choice(moves) if moves else None