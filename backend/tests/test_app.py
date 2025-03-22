import unittest
import json
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class TestApp(unittest.TestCase):
    """Test cases for the Flask application."""
    
    def setUp(self):
        """Set up test client before each test."""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_home_endpoint(self):
        """Test the home endpoint responds correctly."""
        response = self.app.get('/')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertIn('message', data)
        self.assertIn('model_loaded', data)
    
    def test_analyze_no_text(self):
        """Test analyze endpoint with missing text."""
        response = self.app.post('/api/analyze', 
                                json={})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['status'], 'error')
        self.assertIn('message', data)
    
    def test_analyze_empty_text(self):
        """Test analyze endpoint with empty text."""
        response = self.app.post('/api/analyze', 
                                json={'text': ''})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['status'], 'error')
        self.assertIn('message', data)
    
    def test_analyze_with_text(self):
        """Test analyze endpoint with valid text.
        
        Note: This test will be skipped if model is not loaded.
        """
        # Skip test if model is not loaded
        response = self.app.get('/')
        data = json.loads(response.data)
        if not data.get('model_loaded'):
            self.skipTest("Model not loaded, skipping test")
        
        # Test with sample text
        sample_text = "Breaking news: Scientists discover new renewable energy source."
        response = self.app.post('/api/analyze', 
                                json={'text': sample_text})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertIn('prediction', data)
        self.assertIn('confidence', data)
        self.assertTrue(0 <= data['confidence'] <= 1)
        self.assertIn(data['prediction'], ['REAL', 'FAKE'])

if __name__ == '__main__':
    unittest.main() 