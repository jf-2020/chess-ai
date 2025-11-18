import sys
from pathlib import Path
from datetime import datetime

import chess
import chess.pgn

from chess_ai.core.game import ChessGame, GameSession
from chess_ai.core.player import Player
from chess_ai.agents.random_agent import RandomAgent
from chess_ai.agents.registry import get_agent

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

def board_to_ascii(game: ChessGame) -> str:
    """Convert the current board to a browser appropriate str representation."""
    board = game.board
    files = "abcdefgh"
    ranks = range(7, -1, -1) # 7 -> 0 => ranks 8 -> 1

    last_move = board.move_stack[-1] if board.move_stack else None

    lines: list[str] = []

    lines.append("")
    lines.append("  +------------------------+")
    for r in ranks:
        row_pieces = []
        for f in range(8):
            square = chess.square(f, r)
            piece = board.piece_at(square)
            symbol = piece.symbol() if piece else "."
            row_pieces.append(symbol)
        rank_label = r + 1
        lines.append(f"  {rank_label} | {' '.join(row_pieces)} |")
    lines.append("  +------------------------+")
    lines.append("    " + " ".join(files))
    lines.append("")

    side = "White" if board.turn else "Black"
    lines.append(f"Side to move: {side}")
    if last_move is not None:
        lines.append(f"Last move: {last_move.uci()}")
    lines.append("")

    return "\n".join(lines)

def render_board(game: ChessGame) -> None:
    # ASCII board printing
    print(board_to_ascii(game))

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

def play_human_vs_agent(agent_name: str = "random", save_game: bool = False) -> None:
    """
    Play a human vs the specified agent by name.

    agent_name should be a key registered in chess_ai.agents.registry.AGENTS,
    e.g. "random" or "minimax".
    """
    game = ChessGame()
    human = HumanPlayer()
    ai = get_agent(agent_name)

    session = GameSession(white_player=human, black_player=ai, game=game)
    session.run()
    print("Game over:", game.result())

    if save_game:
        pgn_path = save_game_to_pgn(game)
        print(f"Saved game to {pgn_path}")

def play_human_vs_random(save_game: bool = False) -> None:
    """
    Backwards-compatible wrapper that always selects the random agent.
    """
    play_human_vs_agent(agent_name="random", save_game=save_game)

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

def main() -> None:
    """
    CLI for chess-ai.

    Usage:
        python -m chess_ai          # menu
        python -m chess_ai play [--save]
        python -m chess_ai replay PATH_TO_PGN
    """
    raw_args = sys.argv[1:]

    # Normalize for `python -m chess_ai ...`
    # Example sys.argv:
    #   ["python", "-m", "chess_ai"]                -> args = []
    #   ["python", "-m", "chess_ai", "play"]        -> args = ["play"]
    #   ["python", "-m", "chess_ai", "replay", ...] -> args = ["replay", ...]
    if len(raw_args) >= 2 and raw_args[0] == "-m" and raw_args[1] == "chess_ai":
        args = raw_args[2:]
    else:
        args = raw_args

    # No args -> interactive menu
    if len(args) == 0:
        print("chess-ai menu:")
        print("  1) Play human vs AI (random or minimax)")
        print("  2) Replay a PGN file")
        print("  q) Quit")
        choice = input("> ").strip().lower()

        if choice == "1":
            save_answer = input("Save game when finished? [y/N]: ").strip().lower()
            save = save_answer == "y"

            agent_choice = input(
                "Choose AI: [r]andom or [m]inimax (default: minimax): "
            ).strip().lower()

            if agent_choice == "r":
                agent_name = "random"
            else:
                agent_name = "minimax"

            play_human_vs_agent(agent_name=agent_name, save_game=save)
        elif choice == "2":
            path = input("Path to PGN file: ").strip()
            replay_game_from_pgn(path)
        else:
            print("Goodbye.")
        return

    cmd = args[0]

    if cmd == "play":
        save = False
        agent_name = "random"

        # Very simple arg parsing:
        #   python -m chess_ai play [--save] [--agent NAME]
        extra_args = args[1:]
        i = 0
        while i < len(extra_args):
            token = extra_args[i]
            if token == "--save":
                save = True
            elif token == "--agent" and i + 1 < len(extra_args):
                agent_name = extra_args[i + 1]
                i += 1  # skip the name we just consumed
            else:
                print("Usage: python -m chess_ai play [--save] [--agent NAME]")
                return
            i += 1

        play_human_vs_agent(agent_name=agent_name, save_game=save)

    elif cmd == "replay":
        if len(args) < 2:
            print("Usage: python -m chess_ai replay PATH_TO_PGN")
            return
        replay_game_from_pgn(args[1])

    else:
        print(f"Unknown command: {cmd}")
        print("Valid commands: play, replay")