import logging
from flask import Flask, send_from_directory, render_template
from flask_cors import CORS
from tsp_backend.tsp_routes import tsp_bp  # Import the blueprint
from tic_tac_toe_backend.tic_tac_toe_routes import tic_tac_toe_bp
from KnightProbBackend.KnightTourRoute import knight_blueprint
from toh_backend.toh_routes import toh_bp  # Added Tower of Hanoi blueprint
import toh_db  # Added for Tower of Hanoi database

# Configure centralized logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize the Flask app
app = Flask(__name__)
app = Flask(__name__, template_folder='../frontend')

# Register blueprints
app.register_blueprint(tsp_bp, url_prefix='/api')
app.register_blueprint(tic_tac_toe_bp, url_prefix='/tic_tac_toe')
app.register_blueprint(knight_blueprint, url_prefix='/knight')
app.register_blueprint(toh_bp, url_prefix='/tower_of_hanoi')  # Added Tower of Hanoi blueprint

# Configure CORS for all routes
CORS(app, resources={
    r"/api/*": {"origins": "*"},
    r"/tic_tac_toe/*": {"origins": "*"},
    r"/knight/*": {"origins": "*"},
    r"/tower_of_hanoi/*": {"origins": "*"}  # Added CORS for Tower of Hanoi
})

print(app.url_map)

# Serve home.html as the main entry point
@app.route('/')
def home():
    return send_from_directory('../frontend', 'home.html')

# Serve other static files from the frontend directory
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('../frontend', filename)

# Added Tower of Hanoi index route
@app.route('/tower_of_hanoi')
def index():
    logger.info("Serving index page")
    return render_template('tower_of_hanoi.html')

# Added Tower of Hanoi static file route
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('../frontend/tower_of_hanoi_frontend/static', path)

# Added error handler
@app.errorhandler(Exception)
def handle_error(error):
    logger.error(f"Unhandled error: {str(error)}")
    return {'error': 'Internal server error'}, 500

# Main entry point for the Flask app
if __name__ == '__main__':
    try:
        toh_db.init_db()  # Added Tower of Hanoi database initialization
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise
    logger.info("Starting the Flask application...")
    app.run(debug=True, use_reloader=False)