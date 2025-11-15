from chess_ai.core.game import ChessGame, GameSession
from chess_ai.agents.random_agent import RandomAgent

def test_random_vs_random_runs_to_completion():
    game = ChessGame()
    white = RandomAgent()
    black = RandomAgent()
    session = GameSession(white, black, game)

    result = session.run()

    assert result in {"1-0", "0-1", "1/2-1/2", "*"}