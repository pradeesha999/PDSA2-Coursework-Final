document.addEventListener('DOMContentLoaded', function () {
    initializeBoard();

    let queensPlaced = 0; // Tracks the number of queens placed
    let boardState = Array(8).fill().map(() => Array(8).fill(0)); // 8x8 board state

    function initializeBoard() {
        const board = document.getElementById('board');
        board.innerHTML = ''; // Clear the board

        for (let i = 0; i < 8; i++) {
            for (let j = 0; j < 8; j++) {
                const square = document.createElement('div');
                square.className = `square ${(i + j) % 2 === 0 ? 'white' : 'black'}`;
                square.dataset.row = i;
                square.dataset.col = j;

                // Add click event listener
                square.addEventListener('click', handleSquareClick);

                board.appendChild(square);
            }
        }
    }

    function handleSquareClick(event) {
        const square = event.target;
        const row = parseInt(square.dataset.row);
        const col = parseInt(square.dataset.col);

        if (!square.classList.contains('has-queen')) {
            if (queensPlaced < 8) {
                square.classList.add('has-queen'); // Add queen
                boardState[row][col] = 1; // Update board state
                queensPlaced++;
            }
        } else {
            square.classList.remove('has-queen'); // Remove queen
            boardState[row][col] = 0; // Update board state
            queensPlaced--;
        }

        // Update the queen counter
        document.getElementById('queenCount').textContent = queensPlaced;

        // Debug: Log the current board state and queen count
        console.log('Current board state:', boardState);
        console.log('Queens placed:', queensPlaced);
    }

    class QueensGame {
        constructor() {
            this.board = document.getElementById('board');
            this.queenCounter = document.getElementById('queenCount');
            this.usernameInput = document.getElementById('username');
            this.queensPlaced = 0;
            this.boardState = Array(8).fill().map(() => Array(8).fill(0));
            initializeBoard();
            this.initializeControls();
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

            // Debug: Log the number of queens placed
            console.log('Queens placed during validation:', queensPlaced);

            if (queensPlaced !== 8) {
                alert('Please place exactly 8 queens on the board.');
                return;
            }

            const boardString = this.boardState.map(row => row.join(',')).join(';');

            // Debug: Log the board state being sent
            console.log('Sending board state:', boardString);

            const response = await fetch('http://localhost:5000/api/validate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, board: boardString })
            });

            const data = await response.json();
            if (data.success) {
                alert('Valid solution! Solution stored successfully.');
            } else {
                alert(data.message || 'Invalid solution.');
            }
        }

        resetBoard() {
            this.queensPlaced = 0;
            this.boardState = Array(8).fill().map(() => Array(8).fill(0));
            this.queenCounter.textContent = '0';
            document.querySelectorAll('.square').forEach(square => {
                square.classList.remove('has-queen');
            });
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