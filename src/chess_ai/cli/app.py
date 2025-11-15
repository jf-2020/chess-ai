from chess_ai.core.game import ChessGame, GameSession
from chess_ai.core.player import Player
from chess_ai.agents.random_agent import RandomAgent

class HumanPlayer(Player):
    def choose_move(self, game: ChessGame):
        # render board, list legal moves, parse user input, return chess.Move
        pass

def render_board(game: ChessGame):
    # ASCII board printing
    pass

def play_human_vs_random():
    game = ChessGame()
    human = HumanPlayer()
    ai = RandomAgent()

    session = GameSession(white_player=human, black_player=ai)
    session.run()
    print("Game over:", game.result())

if __name__ == "__main__":
    play_human_vs_random()