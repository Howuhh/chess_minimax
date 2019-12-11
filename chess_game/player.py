from random import choice
from itertools import zip_longest

from chess import Board, Move
# from copy import deepcopy

try:
    from board import turn_side, eval_board_state
    from config import BOARD_SCORES
except ModuleNotFoundError:
    from .board import turn_side, eval_board_state
    from .config import BOARD_SCORES


class Player:
    def __init__(self, player: bool, solver: str=None):
        self.player = player
        self.solver = solver

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
    def __init__(self, player):
        super().__init__(player, "minimax")

    def move(self, board: Board) -> str:
        pass


if __name__ == "__main__":
    test_board = Board()
    test_bot = HumanPlayer(player=True)

    print(test_bot.move(test_board))
    print(test_bot.solver)