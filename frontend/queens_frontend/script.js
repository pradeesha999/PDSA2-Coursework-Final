document.addEventListener('DOMContentLoaded', function () {
    class QueensGame {
        constructor() {
            this.board = document.getElementById('board');
            this.queenCounter = document.getElementById('queenCount');
            this.usernameInput = document.getElementById('username');
            this.queensPlaced = 0;
            this.boardState = Array(8).fill().map(() => Array(8).fill(0));

            // Initialize the board and controls
            this.initializeBoard();
            this.initializeControls();
        }

        initializeBoard() {
            console.log('Initializing the board...'); // Debug log
            this.board.innerHTML = ''; // Clear the board (if not already cleared)

            for (let row = 0; row < 8; row++) {
                for (let col = 0; col < 8; col++) {
                    const square = document.createElement('div');
                    square.className = `square ${(row + col) % 2 === 0 ? 'white' : 'black'}`;
                    square.dataset.row = row;
                    square.dataset.col = col;

                    // Add click event listener and bind the QueensGame instance
                    square.addEventListener('click', this.handleSquareClick.bind(this));

                    this.board.appendChild(square);
                }
            }
        }

        handleSquareClick(event) {
            const square = event.target;
            const row = parseInt(square.dataset.row);
            const col = parseInt(square.dataset.col);

            if (!square.classList.contains('has-queen')) {
                if (this.queensPlaced < 8) {
                    square.classList.add('has-queen'); // Add queen
                    this.boardState[row][col] = 1; // Update board state
                    this.queensPlaced++; // Increment queen counter
                } else {
                    alert('You can only place 8 queens on the board.');
                }
            } else {
                square.classList.remove('has-queen'); // Remove queen
                this.boardState[row][col] = 0; // Update board state
                this.queensPlaced--; // Decrement queen counter
            }

            // Update the queen counter display
            this.queenCounter.textContent = this.queensPlaced;

            // Debug: Log the current board state and queen count
            console.log('Current board state:', this.boardState);
            console.log('Queens placed:', this.queensPlaced);
        }

        resetBoard() {
            console.log('Resetting the board...'); // Debug log

            // Reset the board state and queen counter
            this.queensPlaced = 0;
            this.boardState = Array(8).fill().map(() => Array(8).fill(0));
            this.queenCounter.textContent = '0';

            // Clear and reinitialize the chessboard
            this.initializeBoard();
        }

        initializeControls() {
            document.getElementById('registerBtn').addEventListener('click', () => this.registerPlayer());
            document.getElementById('validateBtn').addEventListener('click', () => this.validateSolution());
            document.getElementById('resetBtn').addEventListener('click', () => this.resetBoard());
        }

        async registerPlayer() {
            const username = this.usernameInput.value.trim();
            if (!username) {
                alert('Please enter a username.');
                return;
            }

            const response = await fetch('http://localhost:5000/api/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username })
            });

            const data = await response.json();
            if (data.success) {
                alert('Player registered successfully!');
            } else {
                alert(data.message || 'Error registering player.');
            }
        }

        async validateSolution() {
            const username = this.usernameInput.value.trim();
            if (!username) {
                alert('Please enter your username.');
                return;
            }

            console.log('Queens placed during validation:', this.queensPlaced);

            if (this.queensPlaced !== 8) {
                alert('Please place exactly 8 queens on the board.');
                return;
            }

            const boardString = this.boardState.map(row => row.join(',')).join(';');
            console.log('Sending board state:', boardString); // Debug log

            try {
                const response = await fetch('http://localhost:5000/api/validate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, board: boardString })
                });

                const data = await response.json();
                if (data.success) {
                    alert('Valid solution! Solution stored successfully.');
                    fetchSolutions();
                    this.resetBoard();
                } else {
                    alert(data.message || 'Invalid solution.');
                }
            } catch (error) {
                console.error('Error validating solution:', error);
                alert('An error occurred while validating the solution.');
            }
        }
    }

    // Initialize the game
    new QueensGame();
});

async function fetchSolutions() {
    try {
        const response = await fetch('http://localhost:5000/api/solutions');
        const data = await response.json();

        console.log('Solutions data:', data); // Debug log

        const leaderboardList = document.getElementById('leaderboardList');
        leaderboardList.innerHTML = '';

        if (data.solutions && data.solutions.length > 0) {
            const playerScores = {};

            // Aggregate scores by player
            data.solutions.forEach(solution => {
                const playerId = solution.found_by;
                if (!playerScores[playerId]) {
                    playerScores[playerId] = 0;
                }
                playerScores[playerId]++;
            });

            // Sort players by score
            const sortedPlayers = Object.entries(playerScores).sort((a, b) => b[1] - a[1]);

            // Display leaderboard
            sortedPlayers.forEach(([playerId, score]) => {
                const listItem = document.createElement('li');
                listItem.textContent = `Player ID: ${playerId}, Solutions: ${score}`;
                leaderboardList.appendChild(listItem);
            });
        } else {
            leaderboardList.innerHTML = '<li>No solutions found</li>';
        }
    } catch (error) {
        console.error('Error fetching solutions:', error);
    }
}

// Call fetchSolutions on page load
document.addEventListener('DOMContentLoaded', fetchSolutions);