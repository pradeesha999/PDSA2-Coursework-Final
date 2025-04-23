import unittest
from backend.queens_backend.app import app
import json

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.valid_solution = "0,0,0,0,1,0,0,0;0,0,0,0,0,0,1,0;0,0,0,1,0,0,0,0;0,0,0,0,0,0,0,1;0,1,0,0,0,0,0,0;0,0,0,0,0,1,0,0;1,0,0,0,0,0,0,0;0,0,1,0,0,0,0,0"

    def test_solve_sequential(self):
        response = self.app.post('/api/solve',
                               json={'type': 'sequential'})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['solutions_count'], 92)

    def test_solve_threaded(self):
        response = self.app.post('/api/solve',
                               json={'type': 'threaded'})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        # Each solution should be counted only once
        self.assertEqual(data['solutions_count'], 92)

    def test_submit_solution(self):
        # First, ensure the user exists
        self.app.post('/api/register',
                     json={'username': 'testuser'})
        
        # Then submit the solution
        response = self.app.post('/api/submit',
                               json={
                                   'username': 'testuser',
                                   'board_state': self.valid_solution
                               })
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def tearDown(self):
        # Clean up test data
        with app.app_context():
            from backend.queens_backend.database import Database
            db = Database()
            db.execute_query("DELETE FROM players WHERE username = 'testuser'")