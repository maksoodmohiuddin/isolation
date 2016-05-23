from copy import deepcopy
from time import time, sleep

class Board:
    BLANK = 0

    def __init__(self, player_1, player_2, width=5, height=5):
        self.width=width
        self.height=height
        self.__board_state__ = [ [Board.BLANK for i in range(0, width)] for j in range(0, height)]
        self.__last_player_move__ = {player_1:(-1,-1), player_2:(-1,-1)}
        self.__player_symbols__ = {player_1:1, player_2:2}
        self.move_count = 0
        self.__active_player__ = player_1
        self.__inactive_player__ = player_2
        self.__player_1__ = player_1
        self.__player_2__ = player_2

    def get_state(self):
        return deepcopy(self.__board_state__)

    def __apply_move__(self, move):
        row,col = move
        self.__last_player_move__[self.__active_player__] = move
        self.__board_state__[row][col] = self.__player_symbols__[self.__active_player__]
        tmp = self.__active_player__
        self.__active_player__ = self.__inactive_player__
        self.__inactive_player__ = tmp
        self.move_count = self.move_count + 1

    def copy(self):
        b = Board(self.__player_1__, self.__player_2__, width=self.width, height=self.height)
        for key, value in self.__last_player_move__.items():
            b.__last_player_move__[key] = value
        for key, value in self.__player_symbols__.items():
            b.__player_symbols__[key] = value
        b.move_count = self.move_count
        b.__active_player__ = self.__active_player__
        b.__inactive_player__ = self.__inactive_player__
        b.__board_state__ = self.get_state()
        return b

    def forecast_move(self, move):
        new_board = self.copy()
        new_board.__apply_move__(move)
        return new_board

    def get_active_player(self):
        return self.__active_player__

    def is_winner(self, player):
        return not self.get_legal_moves() and player== self.__inactive_player__

    def is_opponent_winner(self, player):
        return not self.get_legal_moves() and player== self.__active_player__

    def get_opponent_moves(self):
        return self.__get_moves__(self.__last_player_move__[self.__inactive_player__])

    def get_legal_moves(self):
        return self.__get_moves__(self.__last_player_move__[self.__active_player__])

    def __get_moves__(self, move):
        if self.move_count < 2:
            return self.get_first_moves()

        r, c = move

        directions = [ (-1, -1), (-1, 0), (-1, 1),
                        (0, -1),          (0,  1),
                        (1, -1), (1,  0), (1,  1)]

        fringe = [((r+dr,c+dc), (dr,dc)) for dr, dc in directions
                if self.move_is_legal(r+dr, c+dc)]

        valid_moves = []

        while fringe:
            move, delta = fringe.pop()

            r, c = move
            dr, dc = delta

            if self.move_is_legal(r,c):
                new_move = ((r+dr, c+dc), (dr,dc))
                fringe.append(new_move)
                valid_moves.append(move)

        return valid_moves

    def get_first_moves(self):
        return [ (i,j) for i in range(0,self.height) for j in range(0,self.width) if self.__board_state__[i][j] == Board.BLANK]

    def move_is_legal(self, row, col):
        return 0 <= row < self.height and \
               0 <= col < self.width  and \
                self.__board_state__[row][col] == Board.BLANK

    def get_blank_spaces(self):
        return self.get_player_locations(Board.BLANK)

    def get_player_locations(self, player):
        if player == 0:
            return [ (i,j) for j in range(0, self.width) for i in range(0,self.height) if self.__board_state__[i][j] == player]
        return [ (i,j) for j in range(0, self.width) for i in range(0,self.height) if self.__board_state__[i][j] == self.__player_symbols__[player]]

    def get_last_move_for_player(self, player):
        return self.__last_player_move__[player]

    def print_board(self):

        p1_r, p1_c = self.__last_player_move__[self.__player_1__]
        p2_r, p2_c = self.__last_player_move__[self.__player_2__]

        b = self.__board_state__

        out = ''

        for i in range(0, len(b)):
            for j in range(0, len(b[i])):

                if not b[i][j]:
                    out += '0'

                elif i == p1_r and j == p1_c:
                    out += '1'
                elif i == p2_r and j == p2_c:
                    out += '2'
                else:
                    out += 'X'

                out += ' | '
            out += '\n\r'

        return out

    def play_isolation(self, time_limit=500, debug=True):

        curr_time_millis = lambda : int(round(time() * 1000))

        def handler (signum, frame):
            raise Exception("Move timed out")

        while True:

            if debug:
                print('#'*20)
                print(self.print_board())
                print('#'*20)

            legal_player_moves =  self.get_legal_moves()

            # signal.signal(signal.SIGALRM, handler)
            # signal.alarm(time_limit/1000)

            move_start = curr_time_millis()

            time_left = lambda : time_limit - (curr_time_millis() - move_start)
            curr_move = (-1, -1)

            try:
                curr_move = self.__active_player__.move(self, legal_player_moves, time_left)
            except Exception as e:
                print(e)
                pass

            if time_left() <= 0:
                print("%s ran out of time. %s wins."%(str(self.__active_player__), str(self.__inactive_player__)))
                return  self.__inactive_player__, self, "%s ran out of time"%str(self.__active_player__)

            if not curr_move in legal_player_moves:
                print("Illegal move at %d,%d."%curr_move)
                print("Player %s wins."%str(self.__player_symbols__[self.__inactive_player__]))
                return self.__inactive_player__, self, "%s had no valid move"%str(self.__active_player__)

            self.__apply_move__(curr_move)


if __name__ == '__main__':

    print("Starting game:")

    from isolation_player import RandomPlayer
    from isolation_player import HumanPlayer

    board = Board(RandomPlayer(), HumanPlayer())
    board.play_isolation()