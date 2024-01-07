from dlgo import agent
from dlgo import goboard

from dlgo import gotypes
from dlgo.agent.naive import RandomBot
from dlgo.agent.minimax import MinimaxAgent

from dlgo.utils import print_board, print_move
import time

import pandas as pd

BOARD_SIZE = 9
REPS = 1

model_pool = [RandomBot(), MinimaxAgent(depth=1), MinimaxAgent(depth=2)]
model_names = ["Random", "Minimax1", "Minimax2"]

results = pd.DataFrame(0, index=model_names, columns=model_names)

def play(m1, n1, m2, n2):
    print("Playing ", n1, " against ", n2, "for ", REPS, " games")

    clock = 0
    times = [0, 0]
    moves = [0, 0]
    wins = [0, 0]

    for e in range(REPS):

        board_size = BOARD_SIZE
        game = goboard.GameState.new_game(board_size)
        bots = {
            gotypes.Player.black: m1,
            gotypes.Player.white: m2,
        }

        while not game.is_over():

            t1 = time.time_ns()
            bot_move = bots[game.next_player].select_move(game)
            t2 = time.time_ns()
            times[clock] += t2-t1
            moves[clock] += 1

            if clock == 1:
                clock = 0
            else:
                clock = 1

            game = game.apply_move(bot_move)
        
        if game.winner() == gotypes.Player.black:
            wins[0] += 1
        else:
            wins[1] += 1

        results.loc[n1, n2] = wins[0]/REPS
        results.loc[n2, n1] = 0

# play all models against each other, store the results in a matrix

for e in range(len(model_pool)):
    for f in range(len(model_pool[e:])):
        play(model_pool[e], model_names[e], model_pool[f], model_names[f])

results.to_csv("tournament_results.csv")