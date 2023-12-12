from game import Go
from agent_Random import agent_Random
import numpy as np

board_size = 3
game = Go(board_size)
rando = agent_Random(0.5)

print("Welcome to Go!")

while not game.ended:
    game.show()
    print("Player {}'s turn".format(game.player))
    if game.player == 1:
        user_input = input(
            "Play -1 -1 to pass. Enter row and column (separated by a space): "
        )

        if user_input == "-1 -1":
            print("Player {} passed".format(game.player))
            game.pass_turn()
        else:
            i, j = map(int, user_input.split())
            if i < 0 or i >= board_size or j < 0 or j >= board_size:
                print("Invalid move: ({}, {}) off board".format(i, j))
            elif not game.is_empty(i, j):
                print("Invalid move: ({}, {}) occupied".format(i, j))
            else:
                game.place_stone(i, j)
        print()
        game.process_captures(2)
    else:
        t = rando.turn(game)
        if t[0] == -1 and t[1] == -1:
            print("Rando played: Pass")
            game.pass_turn()
        else:
            print("Rando played: ", t)
            game.place_stone(t[0], t[1])
        game.process_captures(1)

print("Game over")

print("Winner: ", game.get_winner())