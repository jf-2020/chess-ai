import pytest
import chess

from chess_ai.web import app as web_app
from chess_ai.core.game import ChessGame

@pytest.fixture
def client(monkeypatch):
    web_app.app.config["TESTING"] = True
    # Disable access gate for simplicity in this test
    monkeypatch.setattr(web_app, "ACCESS_KEY", None)
    return web_app.app.test_client()

def test_pgn_viewer_shows_moves(client):
    # Create a session-scoped game id
    with client.session_transaction() as sess:
        sess["game_id"] = "test-game-id"

    # Attach a game manually to the in-memory store
    game = ChessGame()
    board = game.board
    board.push_san("e4")
    board.push_san("e5")
    board.push_san("Nf3")

    web_app.games["test-game-id"] = game

    resp = client.get("/pgn")
    assert resp.status_code == 200
    body = resp.data.decode("utf-8")

    # PGN should include these moves
    assert "e4" in body
    assert "e5" in body
    assert "Nf3" in body

    # Sanity check: should mention PGN or export somewhere
    assert "PGN" in body or "export" in body