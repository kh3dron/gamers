from dlgo import agent
from dlgo import goboard

from dlgo import gotypes
from dlgo.agent.naive import RandomBot
from dlgo.agent.minimax import MinimaxAgent

from dlgo.utils import print_board, print_move
import time

import pandas as pd

BOARD_SIZE = 9
REPS = 2
GAME_COUNT = 0

# More models can be dropped in here as name:object pairs
models = {
    "Random": RandomBot(),
    "Minimax1": MinimaxAgent(depth=1),
    "Minimax2": MinimaxAgent(depth=2)
}

results = pd.DataFrame(0, index=models.keys(), columns=models.keys(), dtype=float)

def play(m1, n1, m2, n2):

    clock = 0
    times = [0, 0]
    moves = [0, 0]
    wins = [0, 0]

    for e in range(REPS):
        global GAME_COUNT
        GAME_COUNT += 1
        print("    [->] Playing game ", GAME_COUNT, " of ", total_games, ": ", n1, " against ", n2)

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

    results.loc[n1, n2] = wins[1]/REPS
    results.loc[n2, n1] = 1-(wins[1]/REPS)
    print("[!] ", n1, " beats ", n2, " in ", wins[0], " of ", REPS, " games")

total_games = int((len(models) **2 )*REPS)

for e in models.keys():
    for f in models.keys():
        play(models[e], e, models[f], f)


# minimax<3 and random agents never score enough points to overcome the Komi advantage of 6.5, resulting in complete white victory. 

# CSV Structure:
# Columns: model playing white
# Rows: model playing black
# Value: Black's win rate

results = results.round(2)
results.to_csv("tournament_results.csv")

# TODO: add measurements for time to make move and moves per game