import numpy as np
import unittest
from game import Go


class TestGo(unittest.TestCase):

    def test_full_stack(self):
        self.game = Go(9)
        
        self.assertTrue(self.game.board.shape == (9, 9, 17))
        self.assertTrue(self.game.board[:, :, 16].all() == 1)
        self.assertTrue(self.game.board[:, :, 0:15].all() == 0)
        print(self.game.board)

        self.game.place_stone(0, 0)






if __name__ == "__main__":
    unittest.main()
