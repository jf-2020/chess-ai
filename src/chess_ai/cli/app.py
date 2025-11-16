import chess
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

def play_human_vs_random():
    game = ChessGame()
    human = HumanPlayer()
    ai = RandomAgent()

    session = GameSession(white_player=human, black_player=ai)
    session.run()
    print("Game over:", game.result())

if __name__ == "__main__":
    play_human_vs_random()