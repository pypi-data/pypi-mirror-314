from flask import Flask, request, jsonify
import os
import pyspiel

def create_bot_server(bot_class, name):
    """Factory function to create a Flask server for any bot"""
    app = Flask(__name__)
    bot = bot_class(name)
    game = pyspiel.load_game("go", {"board_size": 19})
    
    print(game.new_initial_state())

    @app.route('/get_move', methods=['POST'])
    def get_move():
        serialized_state = request.json['game_state']
        game_state = game.deserialize_state(serialized_state)
        move = bot.select_move(game_state)
        return jsonify({'move': move.to_dict()})
        
    @app.route('/setup', methods=['POST'])
    def setup():
        player_data = request.json
        bot.setup(player_data['player'])
        return jsonify({'status': 'ready'})

    return app

def run_bot_server(bot_class, name="Bot"):
    """Convenience function to create and run a bot server"""
    print(f"Starting a game of Go (board size {19}x{19})")
    print("Initial State:")
    game = pyspiel.load_game("go", {"board_size": 19})
    print(game.new_initial_state())
    
    app = create_bot_server(bot_class, name)
    port = int(os.environ.get('BOT_PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
