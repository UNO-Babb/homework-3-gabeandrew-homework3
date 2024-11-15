from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

# Path to the file where scores and game state will be saved
SAVE_FILE = 'game_state.json'

# Function to load game state from file
def load_game_state():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            return json.load(f)
    return {'high_score': 0, 'current_score': 0, 'platform_pos': 150, 'balloon_pos': {'x': 200, 'y': 50}}

# Function to save game state to file
def save_game_state(state):
    with open(SAVE_FILE, 'w') as f:
        json.dump(state, f)

@app.route('/')
def index():
    # Load the initial game state (high score, current score, positions)
    game_state = load_game_state()
    return render_template('index.html', game_state=game_state)

@app.route('/get_high_score')
def get_high_score():
    game_state = load_game_state()
    return jsonify({'high_score': game_state['high_score']})

@app.route('/save_game', methods=['POST'])
def save_game():
    data = request.json
    game_state = {
        'high_score': max(data['current_score'], data['high_score']),
        'current_score': data['current_score'],
        'platform_pos': data['platform_pos'],
        'balloon_pos': data['balloon_pos']
    }
    save_game_state(game_state)
    return jsonify({'message': 'Game saved successfully'})

if __name__ == '__main__':
    app.run(debug=True)

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Balloon Bounce Game</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: black;
            color: white;
        }
        canvas {
            border: 2px solid white;
        }
        #pauseButton {
            position: absolute;
            top: 20px;
            right: 20px;
            padding: 10px;
            background: gray;
            color: white;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <canvas id="gameCanvas"></canvas>
    <button id="pauseButton">Pause</button>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const pauseButton = document.getElementById("pauseButton");

        let gameState = {{ game_state|tojson }};
        let platformWidth = 90;
        let balloonRadius = platformWidth / 3;
        let platformHeight = 20;
        let spikesHeight = 10;
        let balloonSpeedY = 2;
        let balloonSpeedX = 2;
        let gravity = 0.05;
        let isPaused = false;
        let intervalId;

        // Set canvas size
        canvas.width = 400;
        canvas.height = 400;

        let platformPos = gameState.platform_pos || 150;
        let balloonPos = gameState.balloon_pos || { x: 200, y: 50 };
        let currentScore = gameState.current_score || 0;

        // Function to draw game elements
        function drawGame() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Draw spikes
            ctx.fillStyle = 'gray';
            for (let i = 0; i < 10; i++) {
                ctx.fillRect(i * 40, canvas.height - spikesHeight, 40, spikesHeight);
            }

            // Draw platform
            ctx.fillStyle = 'white';
            ctx.fillRect(platformPos, canvas.height - platformHeight - spikesHeight, platformWidth, platformHeight);

            // Draw balloon
            ctx.fillStyle = 'red';
            ctx.beginPath();
            ctx.arc(balloonPos.x, balloonPos.y, balloonRadius, 0, Math.PI * 2, false);
            ctx.fill();

            // Draw score
            ctx.fillStyle = 'white';
            ctx.font = "16px Arial";
            ctx.fillText(`Score: ${currentScore}`, 10, 20);
            ctx.fillText(`High Score: ${gameState.high_score}`, 10, 40);

            // Check for game over condition
            if (balloonPos.y + balloonRadius > canvas.height - spikesHeight) {
                gameOver();
            }

            // Balloon physics
            balloonPos.y += balloonSpeedY;
            balloonPos.x += balloonSpeedX;
            balloonSpeedY += gravity;

            // Bounce balloon if it hits platform
            if (balloonPos.y + balloonRadius > canvas.height - spikesHeight - platformHeight &&
                balloonPos.x > platformPos && balloonPos.x < platformPos + platformWidth) {
                balloonSpeedY = -balloonSpeedY;
                currentScore++;
            }

            // Ballon bouncing off sides
            if (balloonPos.x - balloonRadius <= 0 || balloonPos.x + balloonRadius >= canvas.width) {
                balloonSpeedX = -balloonSpeedX;
            }
        }

        // Function to update the game
        function updateGame() {
            if (isPaused) return;
            drawGame();
        }

        // Handle left/right movement
        document.addEventListener("keydown", (event) => {
            if (event.key === "ArrowLeft" && platformPos > 0) {
                platformPos -= 10;
            }
            if (event.key === "ArrowRight" && platformPos < canvas.width - platformWidth) {
                platformPos += 10;
            }
        });

        // Handle pause/resume
        pauseButton.addEventListener("click", () => {
            isPaused = !isPaused;
            if (isPaused) {
                saveGameState();
            } else {
                intervalId = setInterval(updateGame, 1000 / 60);
            }
        });

        // Save game state to backend
        function saveGameState() {
            fetch('/save_game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    current_score: currentScore,
                    high_score: gameState.high_score,
                    platform_pos: platformPos,
                    balloon_pos: balloonPos
                })
            }).then(response => response.json())
              .then(data => {
                  alert(data.message);
              });
        }

        // Start the game
        intervalId = setInterval(updateGame, 1000 / 60);

        // Game Over function
        function gameOver() {
            clearInterval(intervalId);
            if (currentScore > gameState.high_score) {
                gameState.high_score = currentScore;
            }
            alert("Game Over! Your Score: " + currentScore);
            saveGameState();
        }

    </script>
</body>
</html>
