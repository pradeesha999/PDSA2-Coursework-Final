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
def register_user():
    """Register a new user"""
    data = request.json
    username = data.get('username')

    print(f"Registering username: {username}")  # Debug log

    if not username:
        return jsonify({'success': False, 'message': 'Username is required'}), 400

    # Check if the user already exists
    user_query = "SELECT id FROM players WHERE username = %s"
    user_result = db.execute_query(user_query, (username,))
    print(f"User query result: {user_result}")  # Debug log

    if user_result:
        return jsonify({'success': False, 'message': 'Username already exists'}), 400

    # Insert the new user
    insert_query = "INSERT INTO players (username, score) VALUES (%s, 0)"
    try:
        db.execute_query(insert_query, (username,))
        print(f"User {username} registered successfully")  # Debug log
        return jsonify({'success': True, 'message': 'User registered successfully'})
    except Exception as e:
        print(f"Error registering user: {e}")  # Debug log
        return jsonify({'success': False, 'message': 'Error registering user'}), 500

@app.route('/api/validate', methods=['POST'])
def validate_solution():
    """Validate and store a solution"""
    data = request.json
    username = data.get('username')
    board_state = data.get('board')

    print(f"Received username: {username}")  # Debug log
    print(f"Received board state: {board_state}")  # Debug log

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
        print(f"Player not found for username: {username}")  # Debug log
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