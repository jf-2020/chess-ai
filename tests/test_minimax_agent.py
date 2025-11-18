import chess

from chess_ai.core.game import ChessGame
from chess_ai.agents.minimax_agent import MinimaxAgent

def test_minimax_returns_legal_move_from_start():
    """From the starting position, MinimaxAgent should return a legal move."""
    game = ChessGame()
    agent = MinimaxAgent(depth=2)

    move = agent.choose_move(game)

    assert move is not None
    assert move in game.legal_moves()

def test_minimax_prefers_simple_capture():
    """
    In a simple position where one move clearly wins material, MinimaxAgent
    should choose a capturing move.

    Position:
      - White: King a1, Queen c1
      - Black: Pawn c3
      - White to move

    Only capturing the pawn strictly improves the material balance.
    """
    fen = "8/8/8/8/8/2p5/8/K1Q5 w - - 0 1"
    board = chess.Board(fen)
    game = ChessGame(board=board)
    agent = MinimaxAgent(depth=1)

    move = agent.choose_move(game)

    assert move is not None
    # Still use the original board for is_capture (Minimax should not modify it)
    assert board.is_capture(move), f"Expected a capture move, got {move.uci()}"
    assert move in game.legal_moves()