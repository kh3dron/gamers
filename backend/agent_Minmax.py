# INCOMPLETE

import numpy as np


class agent_Minmax:
    def __init__(self, depth=1):
        self.depth = depth

    def search(game, level):

        if level == 1: 
            # return highest score
            options = np.argwhere(game.get_possible_moves() == 1)

            best_move = []
            best_score = -999

            for e in options: 
                imagined = game
                imagined.place_stone(e)
                score = imagined.g




            return 
        elif level > 1: 
            # return lowest score of search
            return
        

        return

#returns tuple of coordinates
    def turn(self, game):

        

        return (-1, -1)