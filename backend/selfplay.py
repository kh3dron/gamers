from game import Go
from agent_Random import agent_Random
import numpy as np

board_size = 9
game = Go(board_size)
rando1 = agent_Random(0.5)
rando2 = agent_Random(0.5)

white_wins = 0
black_wins = 0

# play 500 games
for i in range(200):
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

    #with open("random_v_random_1000.txt", "a") as f:
    #    f.write(str(game.moves) + "\n")

    if i % 10 == 0:
        print((str(i) + " games played"))

    if game.get_winner() == 1:
        black_wins += 1
    else:
        white_wins += 1

black_win_rate = black_wins / (black_wins + white_wins)
white_win_rate = white_wins / (black_wins + white_wins)

print("Black wins: " + str(black_wins))
print("White wins: " + str(white_wins))
print("Black win rate: " + str(black_win_rate))
print("White win rate: " + str(white_win_rate))