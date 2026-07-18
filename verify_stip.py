import unittest
import os
import sqlite3
from app import app, calculate_tipi

class STIPVerificationTests(unittest.TestCase):
    def setUp(self):
        # Configure app for testing
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        
    def test_tipi_calculation(self):
        # High Priority Check
        score, cat = calculate_tipi(
            population=120000, 
            signal_strength=1, 
            distance=9.8, 
            internet_users=25, 
            complaints=150, 
            fiber="No", 
            network_type="2G"
        )
        self.assertGreaterEqual(score, 75.0)
        self.assertEqual(cat, "High")
        
        # Low Priority Check
        score_low, cat_low = calculate_tipi(
            population=24000, 
            signal_strength=4, 
            distance=6.2, 
            internet_users=80, 
            complaints=20, 
            fiber="Yes", 
            network_type="5G"
        )
        self.assertLess(score_low, 45.0)
        self.assertEqual(cat_low, "Low")

    def test_public_routes(self):
        # Welcome Page
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Smart Telecom Infrastructure Planner", response.data)
        
        # Login Page
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_protected_route_redirect(self):
        # Accessing dashboard without login should redirect
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertIn(b"Please log in to access this page.", response.data)

    def test_login_flow(self):
        # Log in with correct credentials (mocked admin)
        response = self.client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Logged in successfully", response.data)
        self.assertIn(b"Total Areas", response.data)

if __name__ == '__main__':
    unittest.main()
