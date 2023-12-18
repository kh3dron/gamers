import numpy as np


class agent_Random:
    def __init__(self, passAt=0.5):
        self.passAt = passAt

    def turn(self, game):
        grid_size = game.board_size**2
        options = np.argwhere(game.get_possible_moves() == 1)

        if (len(options) / grid_size) < self.passAt:
            return (-1, -1)
        else:
            random_index = np.random.choice(len(options))
            return options[random_index]
