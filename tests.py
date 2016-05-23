from isolation import Board
from isolation_player import *

# test to make sure evaluation function works.
if __name__ == "__main__":
    sample_board = Board(RandomPlayer(),RandomPlayer())
    # setting up the board as though we've been playing
    sample_board.move_count = 3
    sample_board.__active_player__ = 0 # player 1 = 0, player 2 = 1
    # 1st board = 16 moves
    sample_board.__board_state__ = [
                [0,2,0,0,0],
                [0,0,0,0,0],
                [0,0,1,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0]]
    sample_board.__last_player_move__ = [(2,2),(0,1)]

    # player 1 should have 16 moves available,
    # so board gets a score of 16
    h = OpenMoveEvalFn()
    print('This board has a score of %s.'%(h.score(sample_board, True)))

# test to make sure AI does better than random.
if __name__ == "__main__":
    r = RandomPlayer()
    h = HumanPlayer()
    c = CustomPlayer(search_depth=4)
    t = CustomPlayer(search_depth=4)
    #game = Board(h,r, 3, 2)
    game = Board(r,c, 5, 5)
    #e = OpenMoveEvalFn()
    #score = e.score(game)
    game.play_isolation(time_limit=50000)

