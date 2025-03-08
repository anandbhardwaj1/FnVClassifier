import unittest
import json
import base64
import os
from app import app
from io import BytesIO

class QualityControlTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
    def test_pass_condition(self):
        """Test when bad quality percentage is <= 20% (should PASS)"""
        # Use a sample image that represents good quality (prepare this image)
        test_image_path = "/temp_image.jpg"
        
        if os.path.exists(test_image_path):
            with open(test_image_path, "rb") as img_file:
                img_data = img_file.read()
                
                print("imggg", im)
                # Create test request with the image
                response = self.app.post(
                    '/analyze',
                    data={'image': (img_data, 'good_quality.jpg')},
                    content_type='multipart/form-data'
                )
                
                # Check response
                result = json.loads(response.data)
                percentage = int(result.get('Percentage', '0').replace('%', ''))
                
                # Test pass condition
                self.assertLessEqual(percentage, 20)
                self.assertEqual(response.status_code, 200)
                
    def test_fail_condition(self):
        """Test when bad quality percentage is > 20% (should FAIL)"""
        # Use a sample image that represents poor quality (prepare this image)
        test_image_path = "t"
        
        if os.path.exists(test_image_path):
            with open(test_image_path, "rb") as img_file:
                img_data = img_file.read()
                
                # Create test request with the image
                response = self.app.post(
                    '/analyze',
                    data={'image': (img_data, 'poor_quality.jpg')},
                    content_type='multipart/form-data'
                )
                
                # Check response
                result = json.loads(response.data)
                percentage = int(result.get('Percentage', '0').replace('%', ''))
                
                # Test fail condition
                self.assertGreater(percentage, 20)
                self.assertEqual(response.status_code, 200)
    

# Mock test to simulate LLM responses for testing frontend logic
class MockLLMTests(unittest.TestCase):
    def test_pass_threshold(self):
        """Test the exact 20% threshold (should PASS)"""
        # Mock data with exactly 20% bad quality (pass condition)
        mock_data = {
            "Item": "Mixed Fruit Basket",
            "Percentage": "20%",
            "Judgement": ["Some minor quality issues observed"],
            "Insights": ["Fruits are generally in good condition"],
            "ShelfLife": "5 days"
        }
        
        # The pass condition is percentage <= 20%
        percentage = int(mock_data["Percentage"].replace('%', ''))
        is_passed = percentage <= 20
        self.assertTrue(is_passed)
        
    def test_fail_threshold(self):
        """Test just above threshold (should FAIL)"""
        # Mock data with 21% bad quality (fail condition)
        mock_data = {
            "Item": "Mixed Fruit Basket",
            "Percentage": "21%",
            "Judgement": ["Significant quality issues observed"],
            "Insights": ["Some fruits show signs of damage"],
            "ShelfLife": "3 days"
        }
        
        # The fail condition is percentage > 20%
        percentage = int(mock_data["Percentage"].replace('%', ''))
        is_passed = percentage <= 20
        self.assertFalse(is_passed)

if __name__ == '__main__':
    # Create test_images directory if it doesn't exist
    os.makedirs("test_images", exist_ok=True)
    unittest.main() 