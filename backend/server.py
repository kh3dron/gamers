from flask import Flask, request, jsonify
from flask_cors import CORS

from game import Go
from agent_Random import agent_Random

import time


BOARD_SIZE = 9
game = Go(BOARD_SIZE)
agent_Random = agent_Random()


app = Flask(__name__)
CORS(app)


@app.route('/place_stone', methods=['PUT'])
def place_stone():
    try:
        move = request.json.get('move')
        game.place_stone(move["row"], move["col"])
        return jsonify(game.drawable())

    except Exception as e:
        print("Error placing stone:", e)
        return jsonify(game.drawable())


@app.route('/get_board', methods=['GET'])
def get_game_state():
    return jsonify(game.drawable())

@app.route('/reset', methods=['GET'])
def reset():
    global game
    game = Go(BOARD_SIZE)
    return jsonify(game.drawable())

@app.route('/gamestats', methods=['GET'])
def placed_stones():
    return game.stone_scores()

@app.route('/agent_random', methods=['GET'])
def agent_random():
    print("Agent Random")
    try:
        sleep_time = 0.5
        time.sleep(sleep_time)
        move = agent_Random.turn(game)
        game.place_stone(move[0], move[1])
        return jsonify(game.drawable())

    except Exception as e:
        print("Agent Random Error:", e)
        return jsonify(game.drawable())


if __name__ == '__main__':
    app.run(port=3001, debug=True)
