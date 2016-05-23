from random import randint

class RandomPlayer():
    """Player that chooses a move randomly."""
    def move(self, game, legal_moves, time_left):
        if not legal_moves: return (-1,-1)
        return legal_moves[randint(0,len(legal_moves)-1)]

class HumanPlayer():
    """Player that chooses a move according to
    user's input."""
    def move(self, game, legal_moves, time_left):
        print('\t'.join(['[%d] %s'%(i,str(move)) for i,move in enumerate(legal_moves)] ))

        valid_choice = False
        while not valid_choice:
            try:
                index = int(raw_input('Select move index:'))
                valid_choice = 0 <= index < len(legal_moves)

                if not valid_choice:
                    print('Illegal move! Try again.')

            except ValueError:
                print('Invalid index! Try again.')
        return legal_moves[index]

class OpenMoveEvalFn():

    def score(self, game, maximizing_player):
        if maximizing_player:
            eval_fn = game.get_legal_moves().__len__()
        else:
            eval_fn = game.get_opponent_moves().__len__()
        return eval_fn

class CustomEvalFn():

    def score(self, game, maximizing_player):
        if maximizing_player:
            eval_fn = game.get_legal_moves().__len__()
        else:
            eval_fn = game.get_opponent_moves().__len__()
        return eval_fn

class CustomPlayer():

    def __init__(self, search_depth=4, eval_fn=OpenMoveEvalFn()):
        self.eval_fn = eval_fn
        self.search_depth = search_depth
        self.is_player1 = False

    def move(self, game, legal_moves, time_left):
        #print legal_moves

        # always try to occupy middle
        if (2, 2) in legal_moves:
            return 2, 2

        self.is_player1 = game.get_active_player() is game.__player_1__

        if self.is_player1:
            # reflect player  2's move
            reflect_move = self.reflective_move(game.get_last_move_for_player(game.__player_2__), legal_moves)
            if reflect_move != -1:
                #print "player 1 reflect_move"
                return reflect_move
        else:
            reflect_move = self.reflective_move(game.get_last_move_for_player(game.__player_1__), legal_moves)
            if reflect_move != -1:
                #print "player 2 reflect_move"
                return reflect_move
            avoid_reflection_move = self.non_reflective_move(legal_moves)
            if avoid_reflection_move != -1:
                #print " player 2 avoid_reflection_move"
                return avoid_reflection_move

        #best_move, utility = self.minimax(game,  time_left, depth=self.search_depth)
        # you will eventually replace minimax with alpha-beta
        #print "alpha beta move"
        best_move, utility = self.alphabeta(game,  time_left, depth=self.search_depth)
        return best_move, utility

    def non_reflective_move(self, legal_moves):
        if (0, 1) in legal_moves:
            return 0, 1
        elif (1, 0) in legal_moves:
            return 1, 0
        elif (0, 3) in legal_moves:
            return 0, 3
        elif (3, 0) in legal_moves:
            return 3, 0
        elif (1, 4) in legal_moves:
            return 1, 4
        elif (4, 1) in legal_moves:
            return 4, 1
        elif (3, 4) in legal_moves:
            return 3, 4
        elif (4, 3) in legal_moves:
            return 4, 3
        else:
            return -1

    def reflective_move(self, lastmove, legal_moves):
        if lastmove[0] is 0:
            x = 4
        elif lastmove[0] is 1:
            x = 3
        elif  lastmove[0] is 4:
            x = 0
        elif  lastmove[0] is 3:
            x = 1
        else:
            x = 2

        if lastmove[1] is 0:
            y = 4
        elif lastmove[1] is 1:
            y = 3
        elif lastmove[1] is 4:
            y = 0
        elif  lastmove[1] is 3:
            y = 1
        else:
            y = 2

        #print lastmove
        reflectmove = x, y

        if reflectmove in legal_moves:
            return reflectmove
        else:
            return -1

    def utility(self, game, maximizing_player):

        if game.is_winner(self):
            return float("inf")

        if game.is_opponent_winner(self):
            return float("-inf")

        return self.eval_fn.score(game, maximizing_player)

    def minimax(self, game, timeleft, depth=float("inf"), maximizing_player=True):
        moves = game.get_legal_moves()
        best_move = moves[0]
        best_score = float('-inf')
        for move in moves:
            gamestate = game.forecast_move(move)
            score = self.minimax_maxvalue(gamestate, depth, timeleft, maximizing_player)
            if score > best_score:
                best_move = move
                best_score = score
        return best_move

    def minimax_maxvalue(self, gamestate, depth, timeleft, maximizing_player):
        if depth == 0 or timeleft() < 500 or gamestate.is_winner(self) or gamestate.is_opponent_winner(self):
            return self.utility(gamestate, maximizing_player)

        moves = gamestate.get_legal_moves()
        best_score = float('-inf')
        for move in moves:
            gamestate = gamestate.forecast_move(move)
            score = self.minimax_minvalue(gamestate, depth - 1, timeleft, False)
            if score > best_score:
                best_score = score
        return best_score


    def minimax_minvalue(self, gamestate, depth, timeleft, maximizing_player):
        if depth == 0 or timeleft() < 500 or gamestate.is_winner(self) or gamestate.is_opponent_winner(self):
            return self.utility(gamestate, maximizing_player)

        moves = gamestate.get_legal_moves()
        best_score = float('inf')
        for move in moves:
            gamestate = gamestate.forecast_move(move)
            score = self.minimax_maxvalue(gamestate, depth - 1, timeleft, True)
            if score < best_score:
                best_score = score
        return best_score

    def alphabeta(self, game, timeleft, depth=float("inf"), alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        moves = game.get_legal_moves()
        best_move = moves[0]
        best_score = float('-inf')
        for move in moves:
            gamestate = game.forecast_move(move)
            score = self.alphabeta_maxvalue(gamestate, depth, timeleft, alpha, beta, maximizing_player)
            if score > best_score:
                best_move = move
                best_score = score
        return best_move

    def alphabeta_maxvalue(self, gamestate, depth, timeleft, alpha, beta, maximizing_player):
        if depth == 0 or timeleft() < 500 or gamestate.is_winner(self) or gamestate.is_opponent_winner(self):
            return self.utility(gamestate, maximizing_player)

        moves = gamestate.get_legal_moves()
        for move in moves:
            gamestate = gamestate.forecast_move(move)
            score = self.alphabeta_minvalue(gamestate, depth - 1, timeleft, alpha, beta, False)
            if score >= beta:
                return score
            alpha = max(alpha, score)
        return score

    def alphabeta_minvalue(self, gamestate, depth, timeleft, alpha, beta, maximizing_player):
        if depth == 0 or timeleft() < 500 or gamestate.is_winner(self) or gamestate.is_opponent_winner(self):
            return self.utility(gamestate, maximizing_player)

        moves = gamestate.get_legal_moves()
        #moves = gamestate.get_opponent_moves()
        for move in moves:
            gamestate = gamestate.forecast_move(move)
            score = self.alphabeta_minvalue(gamestate, depth - 1, timeleft, alpha, beta, True)
            if score <= alpha:
                return score
            beta = min(beta, score)
        return score