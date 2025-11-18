"""
Minimal Flask web wrapper around the chess-ai CLI engine.

Initial Goals:
- Reuse the existing board rendering (board_to_ascii).
- Expose a simple web page where a user can:
  - see the current board,
  - submit a UCI move (e.g. "e2e4"),
  - get an agent reply.
"""

from __future__ import annotations

import os
import uuid

import chess
import chess.pgn

from flask import (
    Flask,
    request,
    render_template_string,
    redirect,
    url_for,
    session,
)

from chess_ai.core.game import ChessGame
from chess_ai.agents.registry import get_agent
from chess_ai.cli.app import board_to_ascii

# Global app + single game/agent (for now). Later on, we'll replace this
# with per-session game state.

app = Flask(
    __name__,
    static_folder="static",        # relative to this file's package dir (chess_ai/web)
    static_url_path="/static",     # URL prefix
)

# Secret key for sessions (override in production via env var)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-change-me")

##########################
# Per-session game store #
##########################

# In-memory mapping: session "game_id" -> ChessGame instance
games: dict[str, ChessGame] = {}

# Choose which agent to use via env var.
# Defaults to "random" so the app works even if MinimaxAgent is not wired yet.
AGENT_NAME = os.environ.get("CHESS_AI_AGENT", "random")

# You can pass kwargs for certain agents if you like, e.g. for minimax:
AGENT_KWARGS: dict[str, object] = {}
if AGENT_NAME == "minimax":
    # Adjust depth, pruning, etc. as you wish
    AGENT_KWARGS = {"depth": 2, "use_alpha_beta": True, "use_quiescence": False}

ai = get_agent(AGENT_NAME, **AGENT_KWARGS)

def get_or_create_game() -> ChessGame:
    """
    Look up the ChessGame for the current user session.
    If none exists yet, create one and remember its ID on the session.
    """
    game_id = session.get("game_id")
    if game_id is None or game_id not in games:
        game_id = str(uuid.uuid4())
        session["game_id"] = game_id
        games[game_id] = ChessGame()
    return games[game_id]

def game_to_pgn(game: ChessGame) -> str:
    """
    Convert the current game position (move stack) into a PGN string.

    Uses python-chess PGN helpers and the underlying board's move stack.
    """
    board = game.board

    game_pgn = chess.pgn.Game()

    # Basic headers (you can expand later)
    game_pgn.headers["Event"] = "chess-ai web app"
    game_pgn.headers["Site"] = "Local"
    # "*" for unfinished games, otherwise the actual result, e.g. "1-0"
    game_pgn.headers["Result"] = board.result() if board.is_game_over() else "*"

    node = game_pgn
    for move in board.move_stack:
        node = node.add_variation(move)

    exporter = chess.pgn.StringExporter(
        headers=True,
        variations=False,
        comments=False,
    )
    pgn_str = game_pgn.accept(exporter)
    return pgn_str

#############
# TEMPLATES #
#############

PAGE_TEMPLATE = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>chess-ai!</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
  </head>
  <body>
    <div class="wrapper">
      <div class="panel">
        <div class="panel-inner">
          <h1>chess-ai! // demo</h1>
          <p class="subtitle">
            Human vs random agent > ASCII board, AoC-inspired chrome.
          </p>

          <div class="board-wrapper">
            <pre class="board">{{ board_ascii }}</pre>
          </div>

          {% if message %}
          <div class="message {% if is_error %}error{% else %}info{% endif %}">
            {{ message }}
          </div>
          {% endif %}

          <form class="move-form" action="{{ url_for('make_move') }}" method="post">
            <div class="field-group">
              <label for="move">Move (UCI notation)</label>
              <input type="text" id="move" name="move" placeholder="e2e4, g1f3, a7a5" autofocus>
            </div>
            <div class="button-group">
              <button type="submit">Submit move</button>
            </div>
          </form>

          <p class="small-note">
            Tip: Enter <code>q</code> to resign and start a new game.
          </p>

          <p class="small-note">
            <a href="{{ url_for('show_pgn') }}" style="color: #9effa8; text-decoration: none;">
              View current game as PGN
            </a>
          </p>
        </div>
      </div>
    </div>
  </body>
</html>
"""

PGN_TEMPLATE = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>chess-ai // PGN export</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
  </head>
  <body>
    <div class="wrapper">
      <div class="panel">
        <div class="panel-inner">
          <h1>chess-ai // PGN export</h1>
          <p class="subtitle">
            Current game as PGN. Copy and save locally as needed.
          </p>

          <textarea
            readonly
            rows="14"
            class="pgn-textarea"
          >{{ pgn_text }}</textarea>

          <p class="small-note">
            Result: {{ result }}
          </p>

          <p class="small-note">
            <a href="{{ url_for('index') }}" style="color: #9effa8; text-decoration: none;">
              &larr; Back to game
            </a>
          </p>
        </div>
      </div>
    </div>
  </body>
</html>
"""

######################
# ACCESS KEY GATING  #
######################

ACCESS_KEY = os.environ.get("ACCESS_KEY")  # set this in Render later

ACCESS_TEMPLATE = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>chess-ai // access</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {% if css_href %}
    <link rel="stylesheet" href="{{ css_href }}">
    {% endif %}
  </head>
  <body>
    <div class="wrapper">
      <div class="panel">
        <div class="panel-inner">
          <h1>chess-ai // access</h1>
          <p class="subtitle">
            This app is gated by a shared access key.
          </p>

          {% if message %}
          <div class="message error">
            {{ message }}
          </div>
          {% endif %}

          <form class="move-form" action="{{ url_for('access') }}" method="post">
            <div class="field-group">
              <label for="access_key">Access key</label>
              <input type="text" id="access_key" name="access_key" placeholder="enter access key">
            </div>
            <div class="button-group">
              <button type="submit">Enter</button>
            </div>
          </form>

          <p class="small-note">
            If you don't have the access key, contact the project owner.
          </p>
        </div>
      </div>
    </div>
  </body>
</html>
"""

##########
# ROUTES #
##########

@app.get("/access")
def access():
    """
    Simple access-key form. If ACCESS_KEY is unset, we just auto-grant access.
    """
    # If no access key is configured, don't gate anything.
    if not ACCESS_KEY:
        session["access_granted"] = True
        return redirect(url_for("index"))

    css_href = url_for("static", filename="css/style.css")
    return render_template_string(
        ACCESS_TEMPLATE,
        message=None,
        css_href=css_href,
    )

@app.post("/access")
def access_post():
    """
    Handle access-key submission.
    """
    # If access key isn't configured, just skip gating.
    if not ACCESS_KEY:
        session["access_granted"] = True
        return redirect(url_for("index"))

    submitted = (request.form.get("access_key") or "").strip()

    if submitted == ACCESS_KEY:
        session["access_granted"] = True
        return redirect(url_for("index"))

    css_href = url_for("static", filename="css/style.css")
    return render_template_string(
        ACCESS_TEMPLATE,
        message="Invalid access key.",
        css_href=css_href,
    )

@app.get("/")
def index():
    # Access-gate check
    if ACCESS_KEY and not session.get("access_granted"):
        return redirect(url_for("access"))

    game = get_or_create_game()
    board_ascii = board_to_ascii(game)

    return render_template_string(
        PAGE_TEMPLATE,
        board_ascii=board_ascii,
        message=None,
        is_error=False,
    )

@app.post("/move")
def make_move():
    """
    Handle a move submitted from the form.

    Behavior:
    - Empty input -> ask user to enter something.
    - 'q'         -> treat as resign, reset the game.
    - Invalid UCI -> show error.
    - Illegal move-> show error.
    - Legal move  -> apply human move, then let AI respond (if game not over),
                    then redirect back to index.
    """
    # Access-gate check
    if ACCESS_KEY and not session.get("access_granted"):
        return redirect(url_for("access"))

    game = get_or_create_game()
    board = game.board

    move_str = (request.form.get("move") or "").strip()

    # 1. No input
    if not move_str:
        msg = "Please enter a move."
        board_ascii = board_to_ascii(game)
        return render_template_string(
            PAGE_TEMPLATE,
            board_ascii=board_ascii,
            message=msg,
            is_error=True,
        )

    # 2. Resign / reset on 'q'
    if move_str.lower() == "q":
        msg = "You resigned. Starting a new game."
        board.reset()
        if hasattr(game, "move_history"):
            game.move_history = []

        board_ascii = board_to_ascii(game)
        return render_template_string(
            PAGE_TEMPLATE,
            board_ascii=board_ascii,
            message=msg,
            is_error=False,
        )

    # 3. Parse UCI move
    try:
        move = chess.Move.from_uci(move_str)
    except ValueError:
        msg = f"Invalid UCI move: {move_str}"
        board_ascii = board_to_ascii(game)
        return render_template_string(
            PAGE_TEMPLATE,
            board_ascii=board_ascii,
            message=msg,
            is_error=True,
        )

    # 4. Check legality
    if move not in board.legal_moves:
        msg = f"Illegal move: {move_str}"
        board_ascii = board_to_ascii(game)
        return render_template_string(
            PAGE_TEMPLATE,
            board_ascii=board_ascii,
            message=msg,
            is_error=True,
        )

    # 5. Apply human move
    board.push(move)

    # 6. Let the AI respond if the game is not over
    if not board.is_game_over():
        ai_move = ai.choose_move(game)
        if ai_move is not None:
            board.push(ai_move)

    # 7. Redirect back to main page (Post/Redirect/Get pattern)
    return redirect(url_for("index"))

@app.get("/pgn")
def show_pgn():
    """
    Show the current session's game as PGN inside a textarea.
    Respects the access gate and per-session game state.
    """
    if ACCESS_KEY and not session.get("access_granted"):
        return redirect(url_for("access"))

    game = get_or_create_game()
    pgn_text = game_to_pgn(game)
    board = game.board
    result = board.result() if board.is_game_over() else "*"

    return render_template_string(
        PGN_TEMPLATE,
        pgn_text=pgn_text,
        result=result,
    )

####################
# Local Entrypoint #
####################

if __name__ == "__main__":
    # When run directly:
    #   python -m chess_ai.web.app

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)