import numpy as np
import unittest
from game import Go


class TestGoGame(unittest.TestCase):
    ### Board creation and state ###

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

    ### Taking Turns ###

    def test_pass_turn(self):
        self.game = Go(9)
        self.game.place_stone(0, 0)  # black
        self.game.pass_turn()  # white
        self.assertEqual(self.game.player, 1)
        self.assertEqual(self.game.moves[-1], (-1, -1))

    def test_double_pass(self):
        self.game = Go(9)
        self.game.pass_turn()
        self.game.pass_turn()
        self.assertTrue(self.game.ended)

    ### Groups ###

    def test_groups_small(self):
        self.game = Go(9)
        self.game.board[0, 0] = 1
        self.game.board[0, 4] = 1
        self.game.board[6, 6] = 1
        self.game.board[6, 7] = 1
        groups = self.game.get_groups(1)

        expected_groups = np.array(
            [
                [1, 0, 0, 0, 2, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 3, 3, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )

        self.assertTrue((groups == expected_groups).all())

    def test_groups_medium(self):
            self.game = Go(9)
            self.game.board[3, 5] = 1
            self.game.board[5, 5] = 1
            self.game.board[5, 6] = 1
            self.game.board[6, 6] = 1
            self.game.board[6, 7] = 1
            groups = self.game.get_groups(1)

            expected_groups = np.array(
                [
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 2, 2, 0, 0],
                    [0, 0, 0, 0, 0, 0, 2, 2, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                ]
            )

            self.assertTrue((groups == expected_groups).all())

    def test_groups_medium_mixed(self):
            self.game = Go(9)
            self.game.board[3, 5] = 1
            self.game.board[5, 5] = 1
            self.game.board[5, 6] = 1
            self.game.board[6, 6] = 1
            self.game.board[6, 7] = 1
            self.game.board[0, 0] = 2 # Black stones should be ignored
            self.game.board[0, 4] = 2
            groups = self.game.get_groups(1)

            expected_groups = np.array(
                [
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 2, 2, 0, 0],
                    [0, 0, 0, 0, 0, 0, 2, 2, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                ]
            )

            self.assertTrue((groups == expected_groups).all())

    def test_groups_medium_mixed(self):
            self.game = Go(9)
            self.game.board = np.array(
                [
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 2, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 2, 0, 0, 0],
                    [0, 0, 2, 0, 2, 1, 1, 0, 0],
                    [0, 0, 2, 0, 0, 0, 1, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                ]
            )
            groups = self.game.get_groups(1)

            expected_groups = np.array(
                [
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 2, 2, 0, 0],
                    [0, 0, 0, 0, 0, 0, 2, 2, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                ]
            )

            self.game.show()
            self.assertTrue((groups == expected_groups).all())

    ### Liberties ###

    def test_liberties_small(self):
        self.game = Go(9)
        self.game.board[0, 0] = 1
        self.game.board[0, 4] = 1
        self.game.board[6, 6] = 1
        self.game.board[6, 7] = 1

        liberties = self.game.get_liberties(1)

        expected_liberties = np.array(
            [
                [
                    [0, 1, 0, 0, 0, 0, 0, 0, 0],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                ],
                [
                    [0, 0, 0, 1, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                ],
                [
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 1, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, 1, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                ],
            ]
        )

        self.assertTrue((liberties == expected_liberties).all())

    def test_liberties_medium(self):
        self.game = Go(9)
        self.game.board[3, 5] = 1
        self.game.board[5, 5] = 1
        self.game.board[5, 6] = 1
        self.game.board[6, 6] = 1
        self.game.board[6, 7] = 1
        liberties = self.game.get_liberties(1)

        expected_liberties = np.array(
            [
                [
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                ],
                [
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 1, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, 1, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, 1, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                ],
            ]
        )

        self.assertTrue((liberties == expected_liberties).all())

    ### Captures ###


    # def test_capture(self):
    #     self.game = Go(9)
    #     self.game.board[4, 4] = 1
    #     self.game.board[3, 4] = 2
    #     self.game.board[5, 4] = 2
    #     self.game.board[4, 3] = 2
    #     self.game.board[4, 5] = 2

    #     expected_board = np.array(
    #         [
    #             [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #             [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #             [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #             [0, 0, 0, 0, 2, 0, 0, 0, 0],
    #             [0, 0, 0, 2, 1, 2, 0, 0, 0],
    #             [0, 0, 0, 0, 2, 0, 0, 0, 0],
    #             [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #             [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #             [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         ]
    #     )

    #     self.assertTrue((self.game.board == expected_board).all())

    #     self.game.process_captures(2)
        
    #     print(self.game.board)

    #     expected_board = np.array(
    #         [
    #             [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #             [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #             [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #             [0, 0, 0, 0, 2, 0, 0, 0, 0],
    #             [0, 0, 0, 2, 0, 2, 0, 0, 0],
    #             [0, 0, 0, 0, 2, 0, 0, 0, 0],
    #             [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #             [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #             [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         ]
    #     )

    #     self.assertTrue((self.game.board == expected_board).all())


if __name__ == "__main__":
    unittest.main()
