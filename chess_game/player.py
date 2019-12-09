from random import choice

from chess import Board


class Player:
    def __init__(self, player, solver):
        self.player = player

        if solver not in ("random", "minimax", "human"):
            raise ValueError("Unknown solver!")

        self.solver = solver

    def _human_move(self):
        pass

    def _random_move(self, board: Board) -> str:
        assert board.turn == self.player, "Not bot turn to move!"
        
        moves = list(board.legal_moves)
        move = choice(moves).uci()

        return move

    
    def _minimax_move(self, board, depth, player):
        pass


if __name__ == "__main__":
    test_board = Board()
    test_bot = Bot(player=True)

    print(test_bot.random_move(test_board))