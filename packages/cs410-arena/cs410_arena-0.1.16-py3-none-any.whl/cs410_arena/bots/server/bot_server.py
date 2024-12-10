from flask import Flask, request, jsonify
import os
import pyspiel
import logging

def create_bot_server(bot_class, name):
    """Factory function to create a Flask server for any bot"""
    app = Flask(__name__)
    logging.basicConfig(level=logging.DEBUG)  # Set the logging level
    app.logger.setLevel(logging.DEBUG)  # Ensure Flask app logs at DEBUG level

    bot = bot_class(name)
    game = pyspiel.load_game("go", {"board_size": 19})

    @app.route('/get_move', methods=['POST'])
    def get_move():
        app.logger.debug("Received request at /get_move")
        serialized_state = request.json.get('game_state', None)
        app.logger.debug(f"Serialized state: {serialized_state}")
        
        if serialized_state is None:
            return jsonify({'error': 'No game state provided'}), 400
        
        try:
            game_state = game.deserialize_state(serialized_state)
            app.logger.debug(f"Deserialized game state: {game_state}")
            move = bot.select_move(game_state)
            app.logger.debug(f"Selected move: {move}")
            return jsonify({'move': move.to_dict()})
        except Exception as e:
            app.logger.error(f"Error processing /get_move: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/setup', methods=['POST'])
    def setup():
        app.logger.debug("Received request at /setup")
        try:
            player_data = request.json
            app.logger.debug(f"Player data: {player_data}")
            bot.setup(player_data['player'])
            return jsonify({'status': 'ready'})
        except Exception as e:
            app.logger.error(f"Error in /setup: {e}")
            return jsonify({'error': str(e)}), 500

    return app

def run_bot_server(bot_class, name="Bot"):
    """Convenience function to create and run a bot server"""
    app = create_bot_server(bot_class, name)
    port = int(os.environ.get('BOT_PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
