import chess

from random import random

try:
    from config import BOARD_SCORES, END_SCORES
except ModuleNotFoundError:
    from .config import BOARD_SCORES, END_SCORES


def print_board(board):
    return board._repr_svg_()


def turn_side(board):
    side = "White" if board.turn == True else "Black"
    
    return side

# TODO: wierd mutable defualt arg!! remove it to class
def game_score(board, player, end_scores_policy=END_SCORES, board_scores_policy=BOARD_SCORES):
    # TODO: add claim_draw -> mb slow
    score = None

    if check_tie(board):
        score = end_scores_policy["TIE"]
    elif check_win(board, player):
        score = end_scores_policy["WIN"]
    elif check_win(board, not player):
        score = end_scores_policy["LOSE"]
    else:
        score = eval_board_state(board, player, board_scores_policy)

    return score


def game_over(board, claim_draw=False):
    if board.is_game_over(claim_draw=claim_draw):
        return True

    return False


def check_win(board, player):
    if board.is_checkmate() and board.turn == (not player):
        return True

    return False


def check_tie(board, claim_draw=False):
    tie = (board.is_stalemate() or
            board.is_fivefold_repetition() or
            board.is_insufficient_material())

    if claim_draw:
        tie = tie or board.can_claim_draw()

    if tie:
        return True

    return False


def eval_board_state(board, player: bool, board_scores_policy: dict):
    total_score = random()

    for piece, score in board_scores_policy.items():
        piece = getattr(chess, piece)

        true_score = len(board.pieces(piece, player)) * score
        false_score = len(board.pieces(piece, not player)) * score * -1

        total_score += (true_score + false_score)

    return total_score


if __name__ == "__main__":
    test_board = chess.Board()

    print(eval_board_state(test_board, True, BOARD_SCORES))
    print(game_score(test_board, True))