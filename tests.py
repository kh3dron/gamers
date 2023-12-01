import unittest
from game import Go

class TestGoGame(unittest.TestCase):

    def test_is_empty(self):
        self.game = Go(9)
        self.assertTrue(self.game.is_empty(0, 0))
        self.game.board[0, 0] = 1
        self.assertFalse(self.game.is_empty(0, 0))
        
    def test_place_stone(self):
        self.game = Go(9)
        self.game.place_stone(0, 0)
        self.assertEqual(self.game.board[0, 0], 1)
        self.assertEqual(len(self.game.moves), 1)
        
    def test_place_stone_occupied(self):
        self.game = Go(9)
        self.game.place_stone(0, 0)
        with self.assertRaises(Exception):
            self.game.place_stone(0, 0)

    def test_pass_turn(self):
        self.game = Go(9)
        self.game.place_stone(0, 0) #black
        self.game.pass_turn() #white
        self.assertEqual(self.game.player, 1)
        self.assertEqual(self.game.moves[-1], (-1, -1))

    def test_double_pass(self):
        self.game = Go(9)
        
        self.game.pass_turn()
        self.game.pass_turn()
        self.assertTrue(self.game.ended)
        

if __name__ == '__main__':
    unittest.main()
