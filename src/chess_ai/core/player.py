from __future__ import annotations
from typing import Protocol, TYPE_CHECKING
from chess import Move

if TYPE_CHECKING:
    from .game import ChessGame # only imported for type checkers, not at runtime

class Player:
    """Base class for anything that can choose a move."""
    def choose_move(self, game: ChessGame) -> Move | None:
        raise NotImplementedError