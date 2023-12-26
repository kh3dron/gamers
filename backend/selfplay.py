from game import Go
from agent_Random import agent_Random
import numpy as np

board_size = 9
game = Go(board_size)
rando1 = agent_Random(0.5)
rando2 = agent_Random(0.5)

# play 500 games
for i in range(1000):
    game = Go(board_size)
    rando1 = agent_Random(0.5)
    rando2 = agent_Random(0.5)
    while not game.ended:
        if game.player == 1:
            t = rando1.turn(game)
            game.place_stone(t[0], t[1])
        else:
            t = rando2.turn(game)
            game.place_stone(t[0], t[1])
        game.crunch_board_state()

    with open("random_v_random_1000.txt", "a") as f:
        f.write(str(game.moves) + "\n")

    if i % 10 == 0:
        print((str(i) + " games played"))