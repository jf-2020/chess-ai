import builtins
import chess
from chess_ai.core.game import ChessGame
from chess_ai.cli.app import render_board, HumanPlayer, play_human_vs_random

def test_render_board_outputs_something(capsys):
    game = ChessGame()
    render_board(game)

    out, err = capsys.readouterr()

    # Just assert we printed *something*
    assert out.strip() != ""

def test_human_player_quit_returns_none(monkeypatch):
    game = ChessGame()
    human = HumanPlayer()

    # Simulate user typing "q" once
    inputs = iter(["q"])
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs))

    move = human.choose_move(game)

    assert move is None

def test_human_player_illegal_then_legal(monkeypatch, capsys):
    game = ChessGame()
    human = HumanPlayer()

    # First input: illegal move for White
    # Second input: legal move for White
    inputs = iter(["e7e5", "e2e4"])
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs))

    move = human.choose_move(game)

    # Should eventually accept the legal move e2e4
    assert isinstance(move, chess.Move)
    assert move == chess.Move.from_uci("e2e4")

    # Optional: check that we printed some "illegal" message
    out, err = capsys.readouterr()
    assert "Illegal move" in out or "illegal move" in out.lower()

def test_play_human_vs_random_quit_immediately(monkeypatch, capsys):
    # Simulate user entering "q" on the first prompt
    inputs = iter(["q"])
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs))

    play_human_vs_random()

    out, err = capsys.readouterr()
    assert "Game over" in out