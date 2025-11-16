import builtins
import sys

from chess_ai.cli.app import main


def test_main_menu_quit(monkeypatch, capsys):
    """No args -> menu; choose 'q' to exit."""
    # Simulate: python -m chess_ai
    monkeypatch.setattr(sys, "argv", ["python", "-m", "chess_ai"])

    # User immediately chooses 'q' to quit
    inputs = iter(["q"])
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs))

    main()
    out, err = capsys.readouterr()

    assert "chess-ai menu:" in out


def test_main_play_no_save(monkeypatch, capsys):
    """'play' command -> starts a game and exits when user quits."""
    # Simulate: python -m chess_ai play
    monkeypatch.setattr(sys, "argv", ["python", "-m", "chess_ai", "play"])

    # Human player quits immediately by entering 'q'
    monkeypatch.setattr(builtins, "input", lambda prompt="": "q")

    main()
    out, err = capsys.readouterr()

    assert "Game over" in out