import pandas as pd

from chess import Board 

from itertools import count
from time import sleep
from random import choice
from tqdm.notebook import tqdm

from IPython.display import display, clear_output

try:
    from board import game_over, check_tie, check_win
except ModuleNotFoundError:
    from .board import game_over, check_tie, check_win


class Game:
    def __init__(self, board: Board=None):
        # for games with specific starting point
        if board:
            self.board = board
        else:
            self.board = Board()

    def _game(self, white_p, black_p, visual=False):
        board = self.board.copy()
        result = None
        
        try:
            for i in count():
                if visual:
                    display(board)
                    sleep(1)

                if game_over(board, claim_draw=True):
                    break

                if board.turn:
                    move = white_p.move(board)
                else:
                    move = black_p.move(board)

                board.push_uci(move)
                if visual:
                    clear_output(wait=True)
        except KeyboardInterrupt:
            print("Game stopped!")
            
        if check_tie(board, claim_draw=True):
            result = -1
        else:
            result = int(check_win(board, True))
            
        return {"white": white_p.solver, 
                "black": black_p.solver, 
                "FEN": board.fen(), "last_move": board.peek(), 
                "moves_history": [move.uci() for move in board.move_stack],
                "moves": i, "result": result}

    def start_game(self, p1_cls, p2_cls, visual=False):
        goes_first = choice([True, False])
        
        if goes_first:
            result = self._game(p1_cls(True), p2_cls(False), visual)
        else:
            result = self._game(p2_cls(True), p1_cls(False), visual)
                
        return result

    def start_games(self, p1_cls, p2_cls, n=10):
        results = {}

        for i in tqdm(range(n)):
            result = self.start_game(p1_cls, p2_cls)
            results[i] = result

        return pd.DataFrame.from_dict(results, orient="index")