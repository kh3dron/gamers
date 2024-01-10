from dlgo import agent
from dlgo import goboard

from dlgo import gotypes
from dlgo.agent.naive import RandomBot
from dlgo.agent.minimax import MinimaxAgent

from dlgo.utils import print_board, print_move, view_boardtiles
import time

def main():

    reps = 1

    clock = 0
    names = ["Random", "Minimax"]
    times = [0, 0]
    moves = [0, 0]
    wins = [0, 0]

    for e in range(reps):

        board_size = 9
        game = goboard.GameState.new_game(board_size)
        bots = {
            gotypes.Player.black: RandomBot(),
            gotypes.Player.white: MinimaxAgent(depth=2),
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

            #print_move(game.next_player, bot_move)
            game = game.apply_move(bot_move)
            #print(chr(27) + "[2J")
            #print_board(game.board)
            print(view_boardtiles(game.board))
        
        if game.winner() == gotypes.Player.black:
            wins[0] += 1
        else:
            wins[1] += 1

        print("Game ", e, "completed, winner: ", game.winner())


    print("Elapsed simulation seconds: ", sum(times)/10e9)
    for e in [0, 1]:
        print(names[e], "made", moves[e], " moves, average of ", ((times[e]/10e9)/moves[e]), " seconds per move")

    print("White win ratio: ", wins[1]/reps)


if __name__ == "__main__":
    main()
