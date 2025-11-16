from pathlib import Path

import chess.pgn

from chess_ai.core.game import ChessGame, GameSession
from chess_ai.agents.random_agent import RandomAgent
from chess_ai.cli.app import save_game_to_pgn, replay_game_from_pgn

def test_save_game_to_pgn_creates_valid_file(tmp_path):
    # Play a random vs random game
    game = ChessGame()
    white = RandomAgent()
    black = RandomAgent()
    session = GameSession(white, black, game)
    result = session.run()
    assert result in {"1-0", "0-1", "1/2-1/2", "*"}

    # Save to PGN under a temporary directory
    pgn_path = save_game_to_pgn(game, directory=tmp_path)
    assert pgn_path.exists()
    assert pgn_path.suffix == ".pgn"

    # Check that the PGN file contains a valid game
    with pgn_path.open("r", encoding="utf-8") as f:
        loaded_game = chess.pgn.read_game(f)
    assert loaded_game is not None
    assert loaded_game.headers.get("Result") is not None

def test_replay_game_from_pgn_runs_through(tmp_path, monkeypatch, capsys):
    # First, create and save a random vs random game
    game = ChessGame()
    white = RandomAgent()
    black = RandomAgent()
    session = GameSession(white, black, game)
    _ = session.run()

    pgn_path = save_game_to_pgn(game, directory=tmp_path)

    # Monkeypatch input so replay doesn't block (always press Enter)
    monkeypatch.setattr("builtins.input", lambda prompt="": "")

    # Replay the game
    replay_game_from_pgn(pgn_path)

    out, err = capsys.readouterr()

    # Basic sanity checks that replay happened and printed something
    assert "Replaying game" in out
    assert "End of game." in out