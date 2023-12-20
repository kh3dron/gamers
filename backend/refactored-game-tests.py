import numpy as np
import unittest
from game import Go

GAME_SIZE = 19

class TestGo(unittest.TestCase):
    def test_init(self):
        self.game = Go(GAME_SIZE)

        self.assertTrue(self.game.board.shape == (GAME_SIZE, GAME_SIZE, 17))
        self.assertTrue(self.game.board[:, :, 16].all() == 1)
        self.assertTrue(self.game.board[:, :, 0:15].all() == 0)

    def test_place_stone(self):
        self.game = Go(GAME_SIZE)
        self.game.place_stone(3, 3)

        self.assertTrue(self.game.board[3, 3, 1] == 1)
        self.assertTrue(self.game.board[:, :, 0].all() == 0)
        self.assertTrue(self.game.board[:, :, 16].all() == 0)
        self.assertEqual(self.game.moves, [(3, 3)])

    def test_place_many_stones(self):
        self.game = Go(GAME_SIZE)   # B0, W0
        self.game.place_stone(3, 3) # W1, B1, W0, B0
        self.game.place_stone(4, 4) # B2, W2, B1, W1, B0, W0
        self.game.place_stone(5, 5) # W3, B3, W2, B2, W1, B1, W0, B0

        self.assertTrue(self.game.board[3, 3, 5] == 1)
        self.assertTrue(self.game.board[4, 4, 2] == 1)
        self.assertTrue(self.game.board[5, 5, 1] == 1)
        self.assertEqual(self.game.moves, [(3, 3), (4, 4), (5, 5)])
        self.assertTrue(self.game.board[:, :, 16].all() == 0)

if __name__ == "__main__":
    unittest.main()
