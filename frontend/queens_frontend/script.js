class ChessBoard {
    constructor() {
        this.board = Array(8).fill().map(() => Array(8).fill(0));
        this.element = document.getElementById('chessboard');
        this.queensCount = 0;
        this.createBoard();
    }

    createBoard() {
        this.element.innerHTML = '';
        for (let i = 0; i < 8; i++) {
            for (let j = 0; j < 8; j++) {
                const cell = document.createElement('div');
                cell.className = `cell ${(i + j) % 2 ? 'black' : 'white'}`;
                cell.dataset.row = i;
                cell.dataset.col = j;
                cell.addEventListener('click', () => this.toggleQueen(i, j));
                if (this.board[i][j]) {
                    cell.classList.add('queen');
                }
                this.element.appendChild(cell);
            }
        }
        this.updateQueensCount();
    }

    toggleQueen(row, col) {
        if (!this.board[row][col] && this.queensCount >= 8) {
            alert('Maximum 8 queens allowed!');
            return;
        }
        this.board[row][col] = 1 - this.board[row][col];
        this.queensCount += this.board[row][col] ? 1 : -1;
        this.createBoard();
    }

    updateQueensCount() {
        document.getElementById('queens-count').textContent = this.queensCount;
    }

    getBoardState() {
        return this.board.map(row => row.join(',')).join(';');
    }

    clear() {
        this.board = Array(8).fill().map(() => Array(8).fill(0));
        this.queensCount = 0;
        this.createBoard();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const chessboard = new ChessBoard();
    const API_URL = 'http://localhost:5000/api';

    document.getElementById('solve-sequential').addEventListener('click', async () => {
        const response = await fetch(`${API_URL}/solve`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({type: 'sequential'})
        });
        const data = await response.json();
        updateMetrics(data);
    });

    document.getElementById('solve-threaded').addEventListener('click', async () => {
        const response = await fetch(`${API_URL}/solve`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({type: 'threaded'})
        });
        const data = await response.json();
        updateMetrics(data);
    });

    document.getElementById('submit-solution').addEventListener('click', async () => {
        const username = document.getElementById('username').value;
        if (!username) {
            alert('Please enter your username');
            return;
        }

        const response = await fetch(`${API_URL}/submit`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                username: username,
                board_state: chessboard.getBoardState()
            })
        });
        const data = await response.json();
        alert(data.success ? 'Solution submitted successfully!' : data.message);
    });

    function updateMetrics(data) {
        document.getElementById('solutions-count').textContent = data.solutions_count;
        document.getElementById('execution-time').textContent = data.execution_time.toFixed(4);
    }
});