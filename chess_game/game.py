from chess import Board 

from itertools import count

from IPython.display import display, clear_output

try:
    from board import game_over, check_tie, check_win
except ModuleNotFoundError:
    from .board import game_over, check_win, check_win


class Game:
    def __init__(self, with_human: bool, board: Board=None):
        # for games with specific starting point
        if board:
            self.board = board
        else:
            self.board = Board()

    def _play_game(self, white_p, black_p, visual=False):
        board = self.board.copy()
        result = None
        
        try:
            for i in count():
                if visual:
                    display(board)

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
            
        if check_tie(board):
            result = -1
        else:
            result = int(check_win(board, True))
            
        return {"white": white_p.solver, 
                "black": black_p.solver, 
                "moves": i, "result": result}

    def play_games(self, p1_cls, p2_cls, n=10):
        results = {}
        
        for i in tqdm(range(n)):
            goes_first = choice([True, False])
            
            if goes_first:
                result = play_game(p1_cls(True), p2_cls(False))
            else:
                result = play_game(p2_cls(True), p1_cls(False))
                
            results[i] = result
            
        return pd.DataFrame.from_dict(results, orient="index")

    def start_game(self, p1, p2, visual=True,):
        pass
    
        # if human:
        #     human_side = bool(input("Please, choose side (1 or 0): "))

        #     p1 = 

        #     result = self._play_game(p1, p2, visual=True)
        # else:
        #     pass

        # return result
