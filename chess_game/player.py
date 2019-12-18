import logging as log

from random import choice
from math import inf
from time import time
from itertools import zip_longest

from chess import Board, Move
# from copy import deepcopy

from abc import ABC, abstractmethod

try:
    from board import turn_side, eval_board_state, game_over, game_score, sorted_moves
    from config import BOARD_SCORES, END_SCORES, PIECES
except ModuleNotFoundError:
    from .board import turn_side, eval_board_state, game_over, game_score, sorted_moves
    from .config import BOARD_SCORES, END_SCORES, PIECES

log.basicConfig(level=log.INFO, 
                    format='%(levelname)s - %(asctime)s - %(message)s',
                    datefmt='%H:%M:%S') 


class Player(ABC):
    def __init__(self, player: bool, solver: str=None):
        self.player = player
        self.solver = solver

    @abstractmethod
    def move(self):
        pass


class HumanPlayer(Player):
    def __init__(self, player: bool):
        super().__init__(player, "human")

    def _get_move(self, board: Board) -> str:
        uci = input(f"({turn_side(board)}) Your turn! Choose move (in uci): ")

        # check legal uci move
        try:
            Move.from_uci(uci)
        except ValueError:
            uci = None
        return uci

    def _print_moves(self, moves):
        iters = [iter(moves)] * 4
        iters = zip_longest(*iters)

        for group in iters:
            print(" | ".join(move for move in group if move is not None))
     
    def move(self, board: Board) -> str:
        assert board.turn == self.player, "Not your turn to move!"
        
        legal_moves = [move.uci() for move in board.legal_moves]

        move = self._get_move(board)

        while move is None:
            print("Invalid uci move! Try again.",)
            move = self._get_move(board)

        while (move not in legal_moves):
            print("Not a legal move! Avaliable moves:\n")
            self._print_moves(legal_moves)
            move = self._get_move(board)
        
        return move


class RandomPlayer(Player):
    def __init__(self, player: bool):
        super().__init__(player, "random")

    def move(self, board: Board) -> str:
        assert board.turn == self.player, "Not bot turn to move!"
        
        moves = list(board.legal_moves)
        move = choice(moves).uci()

        return move


class GreedyPlayer(Player):
    def __init__(self, player: bool):
        super().__init__(player, "greedy")

    def move(self, board: Board) -> str:
        moves = list(board.legal_moves)
        
        for move in moves:
            test_board = board.copy()

            test_board.push(move)
            move.score = eval_board_state(test_board, self.player, BOARD_SCORES)
        
        moves = sorted(moves, key=lambda move: move.score, reverse=True)

        return moves[0].uci()


class MiniMaxPlayer(Player):
    def __init__(self, player, depth=3, verbose=False):
        super().__init__(player, "minimax")
        # TODO: problem for game func with accept classes - how to change depth
        self.depth = depth
        self.verbose = verbose

    def _minimax(self, board: Board, player: bool, depth: int, alpha: float=-inf, beta: float=inf) -> str:
        # base case
        if depth == 0 or game_over(board):
            return [game_score(board, self.player, END_SCORES, BOARD_SCORES), None]

        # first move for white
        if len(board.move_stack) == 0:
            white_opening = choice(("e2e4", "d2d4", "c2c4", "g1f3"))
            return white_opening

        moves = sorted_moves(board)

        if board.turn == player:
            maxScore, bestMove = -inf, None

            for move, piece in moves:
                test_board = board.copy()
                test_board.push(move)

                score = self._minimax(test_board, not player, depth - 1, alpha, beta)
                
                if self.verbose:
                    log.info(f"{turn_side(test_board)}, M{len(moves)}, D{depth}, {PIECES[piece]}:{move} - SCORE: {score}")

                alpha = max(alpha, score[0])
                if beta <= alpha:
                    break

                if score[0] >= maxScore:
                    maxScore = score[0]
                    bestMove = move

            return [maxScore, bestMove]
        else:
            minScore, bestMove = inf, None

            for move, piece in moves:
                test_board = board.copy()
                test_board.push(move)

                score = self._minimax(test_board, player, depth - 1, alpha, beta)

                if self.verbose:
                    log.info(f"{turn_side(test_board)}, M{len(moves)}, D{depth}, {PIECES[piece]}:{move} - SCORE: {score}")
                
                beta = min(beta, score[0])
                if beta <= alpha:
                    break

                if score[0] <= minScore:
                    minScore = score[0]
                    bestMove = move

            return [minScore, bestMove]

    def move(self, board: Board) -> str:
        best_move = self._minimax(board, self.player, self.depth)

        return best_move[1].uci()


if __name__ == "__main__":
    test_board = Board()
    test_bot = MiniMaxPlayer(player=True, verbose=False)

    start_time = time()
    print(test_bot._minimax(test_board, True, 5))
    print(time() - start_time)
    