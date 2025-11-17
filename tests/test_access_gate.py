import pytest

from chess_ai.web import app as web_app

@pytest.fixture
def client():
    web_app.app.config["TESTING"] = True
    return web_app.app.test_client()

def test_access_gate_disabled_when_no_key(monkeypatch, client):
    # Gate off → direct access to main page
    monkeypatch.setattr(web_app, "ACCESS_KEY", None)

    resp = client.get("/")
    assert resp.status_code == 200
    # Looser check: just confirm we're on the main web demo page
    assert b"chess-ai" in resp.data  # matches <title>chess-ai!</title>, etc.

def test_access_gate_redirects_when_key_set(monkeypatch, client):
    # Gate on → redirect from / to /access
    monkeypatch.setattr(web_app, "ACCESS_KEY", "secret123")

    resp = client.get("/", follow_redirects=False)
    assert resp.status_code in (301, 302)
    assert "/access" in resp.headers["Location"]

def test_access_gate_allows_after_correct_key(monkeypatch, client):
    monkeypatch.setattr(web_app, "ACCESS_KEY", "secret123")

    # First hit: redirect
    resp = client.get("/", follow_redirects=False)
    assert resp.status_code in (301, 302)
    assert "/access" in resp.headers["Location"]

    # Post the correct key, following redirects back to /
    resp = client.post(
        "/access",
        data={"access_key": "secret123"},
        follow_redirects=True,
    )

    assert resp.status_code == 200
    # Again, check for main page marker text
    assert b"chess-ai" in resp.data