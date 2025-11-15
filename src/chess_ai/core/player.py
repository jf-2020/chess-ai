from __future__ import annotations
from typing import Protocol
from chess import Move
from .game import ChessGame

class Player:
    """Base class for anything that can choose a move."""
    def choose_move(self, game: ChessGame) -> Move | None:
        raise NotImplementedError