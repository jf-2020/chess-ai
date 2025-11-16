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

import chess
from flask import Flask, request, render_template_string, redirect, url_for

from chess_ai.core.game import ChessGame
from chess_ai.agents.random_agent import RandomAgent
from chess_ai.cli.app import board_to_ascii

# Global app + single game/agent (for now). Later on, we'll replace this
# with per-session game state.

app = Flask(__name__)

# Again, single global game and agent for now
game = ChessGame()
ai = RandomAgent()

PAGE_TEMPLATE = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>chess-ai!</title>
  </head>
  <body>
    <h1>chess-ai!</h1>

    <pre>{{ board_ascii }}</pre>

    {% if message %}
    <p>{{ message }}</p>
    {% endif %}

    <form action="{{ url_for('make_move') }}" method="post">
      <label for="move">Enter move (in UCI, e.g., e2e4, g1f3):</label><br>
      <input type="text" id="move" name="move" autofocus>
      <button type="submit">Submit</button>
    </form>

  </body>
</html>
"""

##########
# ROUTES #
##########

@app.get("/")
def index():
    """
    Show the current board and a simple move input form.
    """
    board_ascii = board_to_ascii(game)
    return render_template_string(PAGE_TEMPLATE, board_ascii=board_ascii, message=None)

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
    move_str = (request.form.get("move") or "").strip()

    # 1. No input
    if not move_str:
        msg = "Please enter a move."
        board_ascii = board_to_ascii(game)
        return render_template_string(PAGE_TEMPLATE, board_ascii=board_ascii, message=msg)

    # 2. Resign / reset on 'q'
    if move_str.lower() == "q":
        msg = "You resigned. Starting a new game."
        # Reset the existing game object in-place instead of reassigning the global.
        game.board.reset()
        # For a later time, note that here would be a good place to store extra
        # state (e.g. move history).
        if hasattr(game, "move_history"):
            game.move_history = []

        board_ascii = board_to_ascii(game)
        return render_template_string(PAGE_TEMPLATE, board_ascii=board_ascii, message=msg)

    board = game.board

    # 3. Parse UCI move
    try:
        move = chess.Move.from_uci(move_str)
    except ValueError:
        msg = f"Invalid UCI move: {move_str}"
        board_ascii = board_to_ascii(game)
        return render_template_string(PAGE_TEMPLATE, board_ascii=board_ascii, message=msg)

    # 4. Check legality
    if move not in board.legal_moves:
        msg = f"Illegal move: {move_str}"
        board_ascii = board_to_ascii(game)
        return render_template_string(PAGE_TEMPLATE, board_ascii=board_ascii, message=msg)

    # 5. Apply human move
    board.push(move)

    # 6. Let the AI respond if the game is not over
    if not board.is_game_over():
        ai_move = ai.choose_move(game)
        if ai_move is not None:
            board.push(ai_move)

    # 7. Redirect back to main page
    return redirect(url_for("index"))

####################
# Local Entrypoint #
####################

if __name__ == "__main__":
    # When run directly:
    #   python -m chess_ai.web.app

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)