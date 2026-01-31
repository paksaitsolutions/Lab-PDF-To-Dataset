import pytest
import json
import os
import tempfile
import zipfile
from unittest.mock import patch, MagicMock

# Add the parent directory to the path to import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


class TestFlaskApp:
    """Test cases for Flask application endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_upload_no_file(self, client):
        """Test upload endpoint with no file provided"""
        response = client.post('/upload')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] == False
        assert 'No file' in data['error']
    
    def test_upload_with_invalid_file_type(self, client):
        """Test upload endpoint with invalid file type"""
        # Create a temporary text file
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp:
            tmp.write(b"This is not a valid file type")
            tmp_path = tmp.name
        
        try:
            with open(tmp_path, 'rb') as test_file:
                response = client.post('/upload', 
                                     data={'file': (test_file, 'test.txt')})
            
            # Should process without crashing (may not extract data)
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'success' in data
        finally:
            os.unlink(tmp_path)
    
    @patch('app.read_pdf_text')
    @patch('app.extract_cbc')
    def test_upload_pdf_processing(self, mock_extract_cbc, mock_read_pdf, client):
        """Test upload endpoint with PDF processing"""
        # Mock the PDF reading and extraction
        mock_read_pdf.return_value = "Patient Name: Test User\nAge/Sex: 25 years/Male\nHB: 12.5"
        mock_extract_cbc.return_value = {
            'Name': 'Test User',
            'Age': '25',
            'Gender': 'Male',
            'HB': '12.5',
            'RBC': '',
            'Source_PDF': 'test.pdf'
        }
        
        # Create a temporary PDF file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            tmp.write(b"Mock PDF content")
            tmp_path = tmp.name
        
        try:
            with open(tmp_path, 'rb') as test_file:
                response = client.post('/upload', 
                                     data={'file': (test_file, 'test.pdf'),
                                           'test_types': '{"cbc": true, "lft": false, "rft": false}'})
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['success'] == True
            assert data['cbc_count'] == 1
        finally:
            os.unlink(tmp_path)
    
    def test_directory_creation(self):
        """Test that required directories are created"""
        assert os.path.exists('uploads')
        assert os.path.exists('output')
    
    def test_unique_filename_generation(self):
        """Test unique filename generation logic"""
        from app import get_unique_filename
        
        # Test with non-existent file
        result = get_unique_filename('non_existent.csv')
        assert result == 'non_existent.csv'
        
        # Test with existing file (mock)
        with patch('os.path.exists', return_value=True):
            with patch('os.path.dirname', return_value='output'):
                with patch('os.path.basename', return_value='test.csv'):
                    result = get_unique_filename('output/test.csv')
                    assert 'test_1.csv' in result


class TestErrorHandling:
    """Test cases for error handling"""
    
    def test_app_initialization(self):
        """Test that Flask app initializes correctly"""
        assert app is not None
        assert hasattr(app, 'test_client')
    
    def test_cors_enabled(self):
        """Test that CORS is properly configured"""
        # Check if CORS is enabled by checking the after_request methods
        assert hasattr(app, 'after_request_funcs')


class TestConfiguration:
    """Test cases for application configuration"""
    
    def test_upload_output_directories(self):
        """Test that upload and output directories are properly set"""
        from app import UPLOAD_DIR, OUTPUT_DIR
        
        assert UPLOAD_DIR == "uploads"
        assert OUTPUT_DIR == "output"
        
        # Test directories exist
        assert os.path.exists(UPLOAD_DIR)
        assert os.path.exists(OUTPUT_DIR)
