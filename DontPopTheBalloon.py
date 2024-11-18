from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

# File to store the game state
GAME_STATE_FILE = 'game_data/game_state.json'

# Function to read the game state from a file
def load_game_state():
    if os.path.exists(GAME_STATE_FILE):
        with open(GAME_STATE_FILE, 'r') as f:
            return json.load(f)
    return {
        "high_score": 0,
        "current_score": 0,
        "balloon_position": {"x": 250, "y": 50},
        "platform_position": {"x": 200, "y": 450},
        "game_running": True
    }

# Function to save the game state to a file
def save_game_state(state):
    with open(GAME_STATE_FILE, 'w') as f:
        json.dump(state, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game_state', methods=['GET'])
def get_game_state():
    state = load_game_state()
    return jsonify(state)

@app.route('/save_game', methods=['POST'])
def save_game():
    state = request.json
    save_game_state(state)
    return jsonify({"status": "success"})

@app.route('/pause_game', methods=['POST'])
def pause_game():
    state = load_game_state()
    state['game_running'] = False
    save_game_state(state)
    return jsonify({"status": "paused"})

@app.route('/resume_game', methods=['POST'])
def resume_game():
    state = load_game_state()
    state['game_running'] = True
    save_game_state(state)
    return jsonify({"status": "resumed"})

if __name__ == '__main__':
    app.run(debug=True)
