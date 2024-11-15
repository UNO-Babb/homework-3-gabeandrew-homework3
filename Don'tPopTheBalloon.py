flask_balloon_game/
│
├── app.py                  # Flask backend
├── static/
│   └── style.css           # CSS for styling (optional)
│   └── game.js             # JavaScript file for game logic
├── templates/
│   └── index.html          # HTML file to render the game
└── README.md

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Balloon Bounce Game</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    </head>
    <body>
        <h1>Balloon Bounce Game</h1>
        <canvas id="gameCanvas"></canvas>
        <script src="{{ url_for('static', filename='game.js') }}"></script>
    </body>
    </html>

body {
    text-align: center;
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f3f3f3;
}

canvas {
    border: 2px solid black;
    background-color: #87CEEB;
    display: block;
    margin: 0 auto;
}

h1 {
    font-size: 2em;
}

// Game setup
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const canvasWidth = 800;
const canvasHeight = 600;
canvas.width = canvasWidth;
canvas.height = canvasHeight;

// Game Variables
let platformWidth = 100;
let platformHeight = 20;
let platformX = (canvasWidth - platformWidth) / 2;
let platformSpeed = 7;
let balloonRadius = 20;
let balloonX = Math.random() * (canvasWidth - balloonRadius * 2);
let balloonY = 0;
let balloonSpeedY = 2;
let spikesHeight = 50;
let gameOver = false;
let score = 0;
let speedIncreaseInterval = 20; // Increase speed every 20 seconds
let lastSpeedIncreaseTime = 0;
let currentTime = 0;

// Handle user input
let keys = { left: false, right: false };

document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') {
        keys.left = true;
    }
    if (e.key === 'ArrowRight') {
        keys.right = true;
    }
});

document.addEventListener('keyup', (e) => {
    if (e.key === 'ArrowLeft') {
        keys.left = false;
    }
    if (e.key === 'ArrowRight') {
        keys.right = false;
    }
});

// Function to draw the game
function drawGame() {
    ctx.clearRect(0, 0, canvasWidth, canvasHeight);

    if (gameOver) {
        ctx.fillStyle = 'red';
        ctx.font = '40px Arial';
        ctx.fillText('Game Over', canvasWidth / 3, canvasHeight / 2);
        ctx.fillText('Score: ' + score, canvasWidth / 3, canvasHeight / 2 + 50);
        return;
    }

    // Draw platform
    ctx.fillStyle = '#32CD32';
    ctx.fillRect(platformX, canvasHeight - platformHeight - spikesHeight, platformWidth, platformHeight);

    // Draw spikes
    ctx.fillStyle = '#FF0000';
    ctx.fillRect(0, canvasHeight - spikesHeight, canvasWidth, spikesHeight);

    // Draw balloon
    ctx.beginPath();
    ctx.arc(balloonX, balloonY, balloonRadius, 0, Math.PI * 2);
    ctx.fillStyle = '#FFD700';
    ctx.fill();
    ctx.stroke();

    // Update balloon position
    balloonY += balloonSpeedY;

    // Balloon hits the platform and bounces back
    if (
        balloonY + balloonRadius >= canvasHeight - spikesHeight - platformHeight &&
        balloonX >= platformX &&
        balloonX <= platformX + platformWidth
    ) {
        balloonSpeedY = -Math.abs(balloonSpeedY); // Bounce up
        score += 1;
    }

    // Balloon falls below the platform (game over)
    if (balloonY + balloonRadius >= canvasHeight - spikesHeight) {
        gameOver = true;
    }

    // Check for speed increase
    currentTime = Date.now();
    if (currentTime - lastSpeedIncreaseTime >= 20000) {
        balloonSpeedY += 0.2;  // Increase the falling speed
        lastSpeedIncreaseTime = currentTime;
    }

    // Move the platform based on input
    if (keys.left && platformX > 0) {
        platformX -= platformSpeed;
    }
    if (keys.right && platformX < canvasWidth - platformWidth) {
        platformX += platformSpeed;
    }

    // Request next frame
    requestAnimationFrame(drawGame);
}

// Start the game
drawGame();


pip install flask

python app.py
