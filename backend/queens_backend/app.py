from flask import Flask, request, jsonify
from flask_cors import CORS
from .database import Database
from .validator import SolutionValidator
import time

app = Flask(__name__)
CORS(app)
db = Database()
validator = SolutionValidator()

@app.route('/')
def home():
    return "Flask backend is running. Use the API endpoints."

@app.route('/api/register', methods=['POST'])
def register_player():
    """Register a new player"""
    data = request.json
    username = data.get('username')
    
    if not username:
        return jsonify({'success': False, 'message': 'Username is required'}), 400

    query = "INSERT IGNORE INTO players (username) VALUES (%s)"
    db.execute_query(query, (username,))
    return jsonify({'success': True, 'message': 'Player registered successfully'})

@app.route('/api/validate', methods=['POST'])
def validate_solution():
    """Validate and store a solution"""
    data = request.json
    username = data.get('username')
    board_state = data.get('board')

    # Debug: Print the received data
    print(f"Received username: {username}")
    print(f"Received board state: {board_state}")

    if not username or not board_state:
        return jsonify({'success': False, 'message': 'Username and board state are required'}), 400

    # Validate the solution
    is_valid = validator.is_valid_solution(board_state)
    print(f"Validation result: {is_valid}")  # Debug log

    if not is_valid:
        return jsonify({'success': False, 'message': 'Invalid solution'}), 400

    # Get player ID
    player_query = "SELECT id FROM players WHERE username = %s"
    player_result = db.execute_query(player_query, (username,))
    print(f"Player query result: {player_result}")  # Debug log

    if not player_result:
        return jsonify({'success': False, 'message': 'Player not found'}), 404

    player_id = player_result[0]['id']

    # Store the solution
    solution_query = """
    INSERT INTO solutions (board_state, is_found, found_by, found_at)
    VALUES (%s, %s, %s, NOW())
    """
    try:
        db.execute_query(solution_query, (board_state, True, player_id))
        print(f"Solution stored for player ID {player_id}")  # Debug log
    except Exception as e:
        print(f"Error storing solution: {e}")  # Debug log
        return jsonify({'success': False, 'message': 'Error storing solution'}), 500

    # Update player's score
    update_score_query = "UPDATE players SET score = score + 1 WHERE id = %s"
    try:
        db.execute_query(update_score_query, (player_id,))
        print(f"Player score updated for player ID {player_id}")  # Debug log
    except Exception as e:
        print(f"Error updating player score: {e}")  # Debug log
        return jsonify({'success': False, 'message': 'Error updating player score'}), 500

    return jsonify({'success': True, 'message': 'Solution stored successfully'})

@app.route('/api/performance', methods=['POST'])
def record_performance():
    """Record algorithm performance metrics"""
    data = request.json
    algorithm_type = data.get('algorithm_type')
    execution_time = data.get('execution_time')
    total_solutions = data.get('total_solutions')

    if not algorithm_type or execution_time is None or total_solutions is None:
        return jsonify({'success': False, 'message': 'All performance metrics are required'}), 400

    query = """
    INSERT INTO performance_metrics (algorithm_type, execution_time, total_solutions)
    VALUES (%s, %s, %s)
    """
    db.execute_query(query, (algorithm_type, execution_time, total_solutions))

    return jsonify({'success': True, 'message': 'Performance metrics recorded successfully'})

@app.route('/api/solutions', methods=['GET'])
def get_solutions():
    """Retrieve all stored solutions"""
    query = "SELECT * FROM solutions"
    results = db.execute_query(query)
    print(f"Solutions retrieved: {results}")  # Debug log
    return jsonify({'solutions': results})

if __name__ == '__main__':
    app.run(debug=True)