import sys
from pathlib import Path
from datetime import datetime

import chess
import chess.pgn

from chess_ai.core.game import ChessGame, GameSession
from chess_ai.core.player import Player
from chess_ai.agents.random_agent import RandomAgent

class HumanPlayer(Player):
    def choose_move(self, game: ChessGame):
        # render board, list legal moves, parse user input, return chess.Move
        while True:
            render_board(game)

            color = "White" if game.board.turn else "Black"
            print(f"{color} to move. Enter your move in UCI (e.g., e2e4), or 'q' to quit:")

            user_input = input("> ").strip()

            if user_input.lower() == "q":
                return None # triggers resignation in GameSession
            
            try:
                move = chess.Move.from_uci(user_input)
            except ValueError:
                print("Could not parse that move. Try again.")
                continue

            if move in game.legal_moves():
                return move
            else:
                print("Illegal move in this position. Try again.")

def render_board(game: ChessGame) -> None:
    # ASCII board printing
    print(game.board)
    print()

def save_game_to_pgn(game: ChessGame, directory: str | Path = "games") -> Path:
    """
    Save the full game (from the starting position) to a PGN file.

    Uses the move stack on game.board and writes a standard PGN file
    into the given directory (default: 'games/).

    Returns:
        Path to the PGN file that was written.
    """
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)

    # Build a PGN Game from the current board and its move stack
    game_pgn = chess.pgn.Game.from_board(game.board)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_game.pgn"
    path = directory / filename

    with path.open("w", encoding = "utf-8") as f:
        print(game_pgn, file = f)

    return path

def play_human_vs_random():
    game = ChessGame()
    human = HumanPlayer()
    ai = RandomAgent()

    session = GameSession(white_player=human, black_player=ai)
    session.run()
    print("Game over:", game.result())

    # Save PGN
    pgn_path = save_game_to_pgn(game)
    print(f"Saved game to {pgn_path}")

def replay_game_from_pgn(path: str | Path) -> None:
    """
    Replay a saved PGN game in the terminal using ASCII boards.
    
    For each move, it waits for the user to press Enter before showing the next position.
    """
    path = Path(path)
    if not path.exists():
        print(f"PGN file not found: {path}")
        return

    with path.open("r", encoding="utf-8") as f:
        game_pgn = chess.pgn.read_game(f)

    if game_pgn is None:
        print(f"Could not read a game from PGN file: {path}")
        return
    
    board = game_pgn.board()
    game = ChessGame(board)

    headers = game_pgn.headers
    white_name = headers.get("White", "?")
    black_name = headers.get("Black", "?")
    result = headers.get("Result", "*")

    print(f"Replaying game: {path}")
    print(f"White: {white_name} | Black: {black_name} | Result: {result}")
    print()

    # Show initial position
    render_board(game)

    for move in game_pgn.mainline_moves():
        _ = input("Press Enter for next move (or 'q' to quit replay)...").strip()
        if _ == "q":
            print("Replay aborted by user.")
            return
        game.apply_move(move)
        render_board(game)

    print("End of game.")

def main():
    """
    Simple CLI entrypoint.
    
    Usage:
        python -m chess_ai.cli.app              # play human vs random
        python -m chess_ai.cli.app play         # same as above
        python -m chess_ai.cli.app replay PATH  # replay a PGN game
    """
    args = sys.argv[1:]

    if not args or args[0] == "play":
        play_human_vs_random()
    elif args[0] == "replay":
        if len(args) < 2:
            print("Usage: python -m chess_ai.cli.app replay PATH_TO_PGN")
            return
        replay_game_from_pgn(args[1])
    else:
        print("Unknown command.")
        print("Usage:")
        print("    python -m chess_ai.cli.app              # play human vs random")
        print("    python -m chess_ai.cli.app play         # play human vs random")
        print("    python -m chess_ai.cli.app replay PATH  # replay a PGN game")

if __name__ == "__main__":
    main()