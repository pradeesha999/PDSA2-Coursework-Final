from flask import Flask, request, jsonify
from flask_cors import CORS
from .database import Database
from .eight_queens_solver import QueensSolver
from .validator import SolutionValidator

app = Flask(__name__)
CORS(app)
db = Database()
solver = QueensSolver()
validator = SolutionValidator()

@app.route('/api/solve', methods=['POST'])
def solve_puzzle():
    algorithm_type = request.json.get('type', 'sequential')
    
    if algorithm_type == 'sequential':
        board = [[0 for _ in range(8)] for _ in range(8)]
        solutions = solver.solve_sequential(board)
    else:
        solutions = solver.solve_threaded()
    
    # Ensure unique solutions only
    unique_solutions = list({str(sol) for sol in solutions})
    
    return jsonify({
        'success': True,
        'solutions_count': len(unique_solutions)
    })

@app.route('/api/submit', methods=['POST'])
def submit_solution():
    data = request.json
    username = data.get('username')
    board_state = data.get('board_state')
    
    if not username or not board_state:
        return jsonify({'success': False, 'message': 'Missing data'})
    
    if not validator.is_valid_solution(board_state):
        return jsonify({'success': False, 'message': 'Invalid solution'})
    
    # Check if solution already exists
    existing = db.execute_query(
        "SELECT id FROM solutions WHERE board_state = %s AND is_found = TRUE",
        (board_state,)
    )
    
    if existing:
        return jsonify({
            'success': False,
            'message': 'Solution already found'
        })
    
    # Get or create player
    player = db.execute_query(
        "SELECT id FROM players WHERE username = %s",
        (username,)
    )
    
    if not player:
        return jsonify({
            'success': False,
            'message': 'Player not found'
        })
    
    player_id = player[0]['id']
    
    # Save the solution
    db.execute_query(
        "INSERT INTO solutions (board_state, is_found, found_by) VALUES (%s, TRUE, %s)",
        (board_state, player_id)
    )
    
    return jsonify({'success': True})

@app.route('/api/register', methods=['POST'])
def register_player():
    username = request.json.get('username')
    if not username:
        return jsonify({'success': False, 'message': 'Username required'})
        
    db.execute_query(
        "INSERT INTO players (username) VALUES (%s)",
        (username,)
    )
    
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)