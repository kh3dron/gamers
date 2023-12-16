from flask import Flask, request, jsonify
from game import Go
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

game = Go(9)


@app.route('/place_stone', methods=['PUT'])
def place_stone():
    try:
        move = request.json.get('move')
        game.place_stone(move["row"], move["col"])
        return jsonify(game.drawable())

    except Exception as e:
        print("Error placing stone:", e)
        return jsonify({'error': 'An error occurred while placing the stone.'}), 500


@app.route('/get_board', methods=['GET'])
def get_game_state():
    return jsonify(game.drawable())

@app.route('/reset', methods=['GET'])
def reset():
    game = Go(9)
    return jsonify(game.drawable())


if __name__ == '__main__':
    app.run(port=3001, debug=True)
