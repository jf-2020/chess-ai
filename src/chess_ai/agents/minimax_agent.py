import math
import chess

from chess_ai.core.player import Player

############################
# BASIC EVALUATION HELPERS #
############################

# Centipawn values (standard-ish)
PIECE_VALUES = {
    chess.PAWN:   100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK:   500,
    chess.QUEEN:  900,
    chess.KING:   0,   # king value handled via mate, not material
}

MATE_SCORE = 100_000 # "infinite" score in Centipawns

def evaluate_board(board: chess.Board) -> int:
    """
    Evaluation from the perspective of the side to move.
    Positive = good for the side to move.
    Negative = good for the opponent.
    """

    # Only treat checkmate specially
    if board.is_checkmate():
        # side to move is checkmated → terrible
        return -MATE_SCORE

    # Otherwise, just use material (even if it's stalemate-ish/illegal)
    score = 0
    for piece_type, value in PIECE_VALUES.items():
        score += value * (
            len(board.pieces(piece_type, chess.WHITE))
            - len(board.pieces(piece_type, chess.BLACK))
        )

    # Normalize for side to move
    return score if board.turn == chess.WHITE else -score

###############
# CORE SEARCH #
###############

def negamax(
    board: chess.Board,
    depth: int,
    alpha: int,
    beta: int,
    use_alpha_beta: bool,
    use_quiescence: bool,
) -> int:
    """
    Negamax search with optional alpha-beta pruning.

    Returns an evaluation from the perspective of the side to move
    at 'board'.
    """

    # Depth or terminal node -> static evaluation
    if depth == 0 or board.is_game_over():
        if use_quiescence and not board.is_game_over():
            return quiescence(board, alpha, beta)
        return evaluate_board(board)

    best_value = -math.inf

    for move in board.legal_moves:
        board.push(move)
        value = -negamax(
            board,
            depth - 1,
            -beta,
            -alpha,
            use_alpha_beta,
            use_quiescence,
        )
        board.pop()

        if value > best_value:
            best_value = value

        if use_alpha_beta:
            if value > alpha:
                alpha = value
            if alpha >= beta:
                break  # alpha-beta cutoff

    return best_value


def quiescence(board: chess.Board, alpha: int, beta: int) -> int:
    """
    Simple quiescence search stub.

    For now, this is extremely basic: it just evaluates the current board.
    Later, you can extend it to:
      - stand pat
      - consider only capture moves
      - extend noisy positions
    """

    stand_pat = evaluate_board(board)

    if stand_pat >= beta:
        return beta
    if stand_pat > alpha:
        alpha = stand_pat

    # Basic stub: we don't yet search captures, but the structure is here.
    # You can later add:
    #   for move in board.legal_moves:
    #       if board.is_capture(move):
    #           ...
    #
    # For now, just return the static eval.
    return alpha

#################
# MINIMAX AGENT #
#################

class MinimaxAgent(Player):
    """
    Classical search-based agent using negamax with optional alpha-beta
    pruning and quiescence search.

    The evaluation is purely material-based for now and is always
    from the perspective of the side to move.
    """

    def __init__(
        self,
        depth: int = 2,
        use_alpha_beta: bool = True,
        use_quiescence: bool = False,
    ):
        """
        Parameters
        ----------
        depth : int
            Search depth in plies (half-moves).
        use_alpha_beta : bool
            Whether to enable alpha-beta pruning.
        use_quiescence : bool
            Whether to use the (very simple) quiescence stub at depth=0.
        """
        self.depth = depth
        self.use_alpha_beta = use_alpha_beta
        self.use_quiescence = use_quiescence

    def choose_move(self, game):
        """
        Choose the best move for the current position using negamax search.

        Returns
        -------
        move : chess.Move or None
            move: the chosen move (or None if no legal moves)
        """
        board = game.board

        legal_moves = list(board.legal_moves)
        if not legal_moves:
            # No legal moves (checkmate or stalemate)
            # Evaluate the position directly.
            value = evaluate_board(board)
            return None, value

        best_move = None
        best_value = -math.inf

        alpha = -math.inf
        beta = math.inf

        for move in legal_moves:
            board.push(move)
            value = -negamax(
                board,
                self.depth - 1,
                -beta,
                -alpha,
                self.use_alpha_beta,
                self.use_quiescence,
            )
            board.pop()

            print("DEBUG:", move.uci(), value)  # <--- add this temporarily

            if value > best_value:
                best_value = value
                best_move = move

            if self.use_alpha_beta and value > alpha:
                alpha = value

        return best_move